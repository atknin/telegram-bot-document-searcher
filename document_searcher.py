#!/usr/bin/env python3
from time import sleep
from typing import List

class DocumentSearcher():
    '''
    Searches words from the user_input in the files in the documents_dir
    
    Args:
        documents_dir (str): a directory where are the files to search
        user_input (List[str]): list of the words a user typed

    Returns:
        List[str]: list of the filenames to return to the user
    
    '''
    def __init__(self,
                 documents_dir: str ='documents', 
                 user_input: List[str] = []) -> List[str]:
        print(f"{documents_dir} {user_input}")
        
    def search(self):
        '''
        Generator - searches keywords in documents and yields progress values
        
        Yields:
            int: progress value
        '''
        print('search method')
        for i in range(2):
            sleep(2)
            print(f'Yielding value {i}')
            yield (i + 1) * 33
        
def main():
    ds = DocumentSearcher()
    print('End')


if __name__ == "__main__":
    main()
