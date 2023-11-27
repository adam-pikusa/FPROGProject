import argparse
import os.path

def read_file(file_path: str) -> list:
    with open(file_path, 'r') as file_handle:
       return [line.strip() for line in file_handle.readlines()]

def tokenize_string(string: str) -> list:
    return [part.strip('"!.?').lower() for part in string.split(' ')]

def filter_words_by_terms(words: list, term_list: list) -> list:
    return list(filter(lambda word: any(term in word for term in term_list), words))

def count_occurences(words: list, term_list: list) -> int:  
    return len(filter_words_by_terms(words, term_list))

def countchapterwords(words: list) -> int:
    length = 0
    for word in words:
            length += len(word)
    return length        

def calculate_term_density(words: list, term_list: list) -> float: 
    return (count_occurences(words,term_list)/countchapterwords(words))*100

def group_lines_based_on_delimiting_line_pattern(lines: list, delimiting_line_pattern: str) -> dict:
    result = {}
    chapterindex = 0

    current_group = None
    for line in lines:
        if line.startswith(delimiting_line_pattern):
            current_group = line[len(delimiting_line_pattern):]
            chapterindex +=1
            result[chapterindex] = []
            continue  
        if current_group == None: 
            continue
    
        result[chapterindex].append(line)
        
    return result

def chunk_collection(col, n):
    for i in range(0, len(col), n):
        yield col[i:i + n]

def map_function(war_terms, peace_terms):
    def inner_map_function(chapters):
        return [
                (chapter[0], [
                    calculate_term_density([tokenize_string(line) for line in chapter[1]], war_terms),
                    calculate_term_density([tokenize_string(line) for line in chapter[1]], peace_terms) ]) 
                    for chapter in chapters]
    return inner_map_function

def shuffle_function(map_result):
    return chunk_collection(sum(map_result, []), 5)

def reduce_function(chapters_with_densities):
    cds = list(chapters_with_densities)
    return [('CHAPTER ' + str(c) + (': war-related' if d[0] > d[1] else ': peace-related')) for c, d in cds] 

def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error(f"The file {arg} does not exist.")
    if not arg.lower().endswith('.txt'):
        parser.error(f"The file {arg} is not a .txt file.")
    return arg


def main():
    
    msg = "A simple tokenizer for categorizing chapters from Tolsoty's War and Peace into either war or peace related chapters."
 
    # Initialize parser
    parser = argparse.ArgumentParser(
                    prog='FPROG-Tokenizer',
                    description= msg,
                    epilog='Made by Adam Pikusa and Florian Kretz')
    
    # Adding optional argument
    parser.add_argument("-o", "--Output", help = "Output filepath" , required= True)
    parser.add_argument("-i", "--Input", type=lambda x: is_valid_file(parser, x), help = "Input filepath", required= True)
    parser.add_argument("-t1", "--Termlist1", type=lambda x: is_valid_file(parser, x), help = "Peace Termlist", required= True)
    parser.add_argument("-t2", "--Termlist2", type=lambda x: is_valid_file(parser, x), help = "War Termlist", required= True)
    
    # Read arguments from command line
    args = parser.parse_args()
 
    peace_terms = read_file(args.Termlist1)
    war_terms = read_file(args.Termlist2)
    war_and_peace = read_file(args.Input)

    chapters_start_at = war_and_peace.index('CHAPTER 1')
    chapters_end_at = war_and_peace.index('*** END OF THE PROJECT GUTENBERG EBOOK, WAR AND PEACE ***')

    chapters = group_lines_based_on_delimiting_line_pattern(war_and_peace[chapters_start_at:chapters_end_at], 'CHAPTER ')
    chunks = list(chunk_collection(list(chapters.items()), 5))

    map_result = map(map_function(war_terms, peace_terms), chunks)
    shuffle_result = shuffle_function(map_result)
    result = map(reduce_function, shuffle_result)

    with open(args.Output, 'w+') as file:
        for i in sum(result, []):
            file.write(i)
            file.write('\n')
  
if __name__ == '__main__':
    main()