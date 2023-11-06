def read_file(file_path: str) -> list:
    with open(file_path, 'r') as file_handle:
       return file_handle.readlines() 

def main():
    print(read_file('war_and_peace.txt'))

if __name__ == '__main__':
    main()