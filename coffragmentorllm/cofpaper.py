import os
import pymupdf

from .coffragmentor import COFExtractor
from .config import RULES

class PDFfile():
    def __init__(self, file:str, verbose = False) -> None:
        if not os.path.exists(file):
            raise FileExistsError(file)
        
        if not file.endswith('.pdf'):
            raise ValueError(f"Given file is not a .pdf ({file})")
        
        self.pages = None
        self.verbose = verbose
        self.file = file

        self.content = self.get_content()


    def get_content(self):
        if self.verbose:
            print(f'Extracting content from {self.file}...')
        self.pages = 0
        text = ""
        with pymupdf.open(self.file) as doc:
            for page in doc:
                self.pages += 1
                text += page.get_text()
        
        if self.verbose:
            print(f'Extracted text length: {len(text)}\nExtracted pages: {self.pages}')

        return text
    
class COFPaper(PDFfile):
    def __init__(self, file, verbose=False):
        super().__init__(file, verbose)

    def fragment(self, openai_key, rules = 'default'):
        extractor = COFExtractor(attempts=1,
                         openai_key= openai_key
                         )
        
        if rules == 'default':
            rules = RULES

        res= extractor(text = self.content, 
               rules=rules, 
               verbose = self.verbose
               )
        return res
       