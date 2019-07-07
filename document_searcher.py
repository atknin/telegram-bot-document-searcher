#!/usr/bin/env python3
import os
from time import sleep
from typing import List
import logging

from PIL import Image
import pytesseract

IMAGES = 'jpg', 'jpeg', 'png'
DOCX = 'docx'

PROGRESS_INTERVALS = 10

logger = logging.getLogger(__name__)

class FindInFile():
    '''
    Extracts text content of a file and searches for keywords
    
    Args:
        file_path (str): path to file
        keyword_list (List[str]): keyword list
        
    Returns:
        bool: whether keywords found
        
    '''
    def __init__(self, file_path: str, keyword_list = List[str]):
        self.file_path = file_name
        self.keyword_list = keyword_list
    def get_content(self):
        pass
    
    def find(self) -> bool:
        content = self.get_content()
        if not content: return False
        for word in self.keyword_list:
            if word not in content:
                return False
        logger.info(f"File {file_path} includes all keywords")
        return True

class FindInImage(FindInFile):
    def __init__(self, file_path: str, keyword_list = List[str]):
        super.__init__(file_path, keyword_list = [])
    
    def get_content(self) -> str:
        try:
            content = pytesseract.image_to_string(
                       Image.open(self.file_path), 
                       lang='rus')
        except Error as e:
            logger.info(f"Can't extract text from {file_path}")
            content = ''
        return content

class DocumentsSearcher():
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
        self.documents_dir = documents_dir
        self.user_input = user_input
        self.result_list = []
        print(f"{documents_dir} {user_input}")
        
    def search(self):
        '''
        Generator - searches keywords in documents and yields progress values
        
        Yields:
            int: progress value
        '''

        files_count = 0
        files_list = []
        for r, d, f in os.walk(documents_dir):
            print(f'file: {f}')
            files_list.append(f)
        files_count = len(files_list)
        progress_stage = progress_slice = files_count / PROGRESS_INTERVALS
        for counter, f in enumerate(files_list):
            result = None
            print(f'processing {f}')
            file_extension = f.split('.')[-1]
            if file_extension in IMAGES:
                result = FindInImage.find(f, self.user_input)
            elif file_extension in DOCX:
                result = FindInDocx.find(f, self.user_input)
            else:
                logger.info(f"file: {} is not supported")
            if result:
                self.result_list.append(f)
            
            if i > progress_stage:
                progress_stage = progress_stage + progress_slice
                yield int(i / files_count * 100) 

        
def main():
    ds = DocumentSearcher()

if __name__ == "__main__":
    main()
