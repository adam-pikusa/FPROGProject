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
def filter_words(words: list, term_list: list) -> list:
    return [word for word in words if word in term_list]

# 5) Count occurrences: 
# Create a function to count the occurrences of words in a list. 
# This function should use the map-reduce philosophy and 
# functional programming techniques to count word occurrences 
# in a parallelizable and efficient manner.
def count_occurences() -> int: return 0

# 6) Calculate term density: 
# Create a function to calculate the density of terms in a text, 
# based on the occurrences of words and their relative distances 
# to the next word of the same category. 
# This function should use functional programming techniques and 
# the map-reduce philosophy for parallelization and efficiency.
def calculate_term_density(): pass

def group_lines_based_on_delimiting_line_pattern(lines: list, delimiting_line_pattern: str) -> dict:
    result = {}

    current_group = None
    for line in lines:
        if line.startswith(delimiting_line_pattern):
            current_group = line[len(delimiting_line_pattern):]
            result[current_group] = []
            continue

        if current_group == None: 
            continue

        result[current_group].append(line)

    return result

def main():
    # 7) Read input files and tokenize: 
    # Read the input files (book, war terms, and peace terms) 
    # and tokenize their contents into words using the 
    # functions created in steps 2 and 3.
    peace_terms = read_file('peace_terms.txt')
    war_terms = read_file('war_terms.txt')

    # 8) Process chapters: 
    # Process each chapter in the book by 
    # calculating the density of war and peace terms 
    # using the functions created in steps 4, 5, and 6. 
    # Store the densities in separate vectors for further processing.
    chapters = group_lines_based_on_delimiting_line_pattern(read_file('war_and_peace.txt'), 'CHAPTER ')

    # 9) Categorize chapters:
    # Iterate through the chapters, and for each chapter, 
    # compare the war density to the peace density to 
    # determine if it's war-related or peace-related. 
    # Store the results in a vector.

    # 10) Print results: 
    # Iterate through the results vector and print 
    # each chapter's categorization as war-related or peace-related.
    
    for chapter, chapter_lines in chapters.items():
        print('CHAPTER ID', chapter)
        print('TOKENIZED CHAPTER LINES')
        print([tokenize_string(line) for line in chapter_lines])

if __name__ == '__main__':
    main()