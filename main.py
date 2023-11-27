import argparse
import os.path
# 2) Read files: 
# Create a function that reads a file and 
# returns its content as a vector of strings. 
# The function should be implemented using functional programming, 
# immutability, and lambdas where possible.
def read_file(file_path: str) -> list:
    with open(file_path, 'r') as file_handle:
       return [line.strip() for line in file_handle.readlines()]

# 3) Tokenize the text: 
# Create a function to tokenize a string into words. 
# This function should use functional programming techniques 
# and lambdas for string manipulation and splitting.
def tokenize_string(string: str) -> list:
    return [part.strip('"!.?').lower() for part in string.split(' ')]

# 4) Filter words: 
# Create a function to filter words from a list based on another list. 
# This function should use functional programming techniques, 
# such as higher-order functions and lambdas, to perform filtering.
def filter_words_by_terms(words: list, term_list: list) -> list:
    return list(filter(lambda word: any(term in word for term in term_list), words))

# 5) Count occurrences: 
# Create a function to count the occurrences of words in a list. 
# This function should use the map-reduce philosophy and 
# functional programming techniques to count word occurrences 
# in a parallelizable and efficient manner.
def count_occurences(words: list, term_list: list) -> int:  
    return len(filter_words_by_terms(words, term_list))

# 6) Calculate term density: 
# Create a function to calculate the density of terms in a text, 
# based on the occurrences of words and their relative distances 
# to the next word of the same category. 
# This function should use functional programming techniques and 
# the map-reduce philosophy for parallelization and efficiency.
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
        if line.startswith("*** END OF THE PROJECT GUTENBERG EBOOK, WAR AND PEACE ***"):
            break        
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
    
    # 7) Read input files and tokenize: 
    # Read the input files (book, war terms, and peace terms) 
    # and tokenize their contents into words using the 
    # functions created in steps 2 and 3.
    

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
    #peace_terms = read_file('peace_terms.txt')
    #war_terms = read_file('war_terms.txt')

    chapters = group_lines_based_on_delimiting_line_pattern(read_file(args.Input), 'CHAPTER ')
    chunks = list(chunk_collection(list(chapters.items()), 5))

    map_result = map(map_function(war_terms, peace_terms), chunks)
    shuffle_result = shuffle_function(map_result)
    result = map(reduce_function, shuffle_result)

    with open('output.txt', 'w+') as file:
        for i in sum(result, []):
            file.write(i)
            file.write('\n')
  
if __name__ == '__main__':
    main()