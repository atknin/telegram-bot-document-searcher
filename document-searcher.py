#!/usr/bin/env python3

from typing import List

class DocumentSearcher():
    """
    Searches words from the user_input in files in the documents_dir
    
    Args:
        documents_dir (str): a directory where are the files to search
        user_input (List[str]): list of the words a user typed

    Returns:
        List[str]: list of the filenames to return to the user
    
    """
    def __init__(self,
                 documents_dir: str ='documents', 
                 user_input: List[str] = []) -> List[str]:
        """Constructor"""
        print(f"{documents_dir} {user_input}")
        
def main():
    ds = DocumentSearcher()
    print('End')


if __name__ == "__main__":
    main()
