#!/usr/bin/env python3
from os import walk, listdir
from os.path import isfile, join
from time import sleep
from typing import List
import logging

from PIL import Image
import pytesseract


IMAGES = 'jpg', 'jpeg', 'png'
DOCX = 'docx'

PROGRESS_INTERVALS = 10

logger = logging.getLogger(__name__)

class FindInFile(object):
    '''
    Extracts text content of a file and searches for keywords
    
    Args:
        file_path (str): path to file
        keyword_list (List[str]): keyword list
 
    '''
    def __init__(self, file_path: str, keyword_list: List[str] = []):
        self.file_path = file_path
        self.keyword_list = keyword_list
        
    def get_content(self):
        pass
    
    def find(self) -> bool:
        # before using specific method to extract content
        # first try to check cache
        cache_file = 'cache/' + self.file_path.split('/')[-1] + '.txt'
        if isfile(cache_file):
            with open(cache_file, 'r') as cf:
              content = cf.read()
        else:
            content = self.get_content().lower()

        logger.info(f"Content:\n{content}\n")
        if not content: return False
        # create cache file
        if not isfile(cache_file):
            with open(cache_file, 'w') as cf:
              cf.write(content)        
        
        for word in self.keyword_list:
            if word not in content:
                return False
        logger.info(f"File {self.file_path} includes all keywords")
        return True

class FindInImage(FindInFile):
    ''' Uses Tesseract to OCR text from image file '''
    def get_content(self) -> str:
        try:
            content = pytesseract.image_to_string(
                       Image.open(self.file_path), 
                       lang='rus')
        except Exception as e:
            logger.info(f"Can't OCR {self.file_path}")
            content = ''
        return content
        
class FindInDocx(FindInFile):
    ''' For now this class is just a stub '''
    def __init__(self, file_path: str, keyword_list = List[str]):
        super.__init__(file_path, keyword_list = [])
    
    def get_content(self) -> str:
        return ''

class DocumentsSearcher:
    '''
    Searches words from the user_input in the files in the documents_dir
    
    Args:
        documents_dir (str): a directory where the files to search are
        keyword_list (List[str]): list of the words user provided

    Returns:
        List[str]: list of the filenames to return to the user
    
    '''
    def __init__(self,
                 documents_dir: str='documents', 
                 keyword_list: List[str]=[]) -> List[str]:
        self.documents_dir = documents_dir
        self.keyword_list = keyword_list
        self.result_list = []
        
    def search(self):
        '''
        Generator - searches keywords in documents and yields progress values
        
        Yields:
            int: progress value
        '''
        logger.info('Search started')
        files_list = [join(self.documents_dir, f) for f in listdir(self.documents_dir) 
                      if isfile(join(self.documents_dir, f))]
        files_count = len(files_list)
        progress_stage = progress_slice = int(files_count / PROGRESS_INTERVALS)
        logger.info(f"Counters: files {files_count}, progress_slice {progress_stage} ")
        for counter, f in enumerate(files_list):
            result = None
            logger.info(f"{counter}, processing {f}")
            file_extension = f.split('.')[-1]
            if file_extension in IMAGES:
                result = FindInImage(f, self.keyword_list).find()
            elif file_extension in DOCX:
                result = FindInDocx(f, self.keyword_list).find()
            else:
                logger.info(f"file: {f} is not supported")
            if result:
                self.result_list.append(f)
            
            # Yield progress value when processed some amount of files
            if counter > progress_stage:
                progress_stage = progress_stage + progress_slice
                yield int(counter / files_count * 100) 
            if counter > 3: return

        
def main():
    pass

if __name__ == "__main__":
    main()
