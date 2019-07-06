#!/usr/bin/env python3

from typing import List

class DocumentSearcher():
    """
    Searches words from user_input in files in documents_dir
    
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
