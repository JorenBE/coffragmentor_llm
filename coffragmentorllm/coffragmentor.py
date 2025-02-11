from typing import Any
from openai import OpenAI
from ast import literal_eval
from .fragments import FragmentResult, FailedFragmentResult
from .config import VALID_MODELS, SYSTEM_PROMPT_COF 


def clean_extraction(extracted_synthesis:str, verbose:bool = False):
    try:
        clean_string = extracted_synthesis.replace('\t', '').replace('\n', '').replace('json', '').replace('`', '').replace('null', 'None')
        clean_dict = literal_eval(clean_string)
        assert isinstance(clean_dict, dict)
        if verbose:
            print(f'Raw extraction succesfully formatted in Python dictionary (with keys: {list(clean_dict.keys())})')
        return (clean_dict, True)
    except:
        return (extracted_synthesis, False)
    
class COFExtractor():
    def __init__(self, 
                 model = 'gpt-4o',
                 attempts = 1,
                 openai_key = None, 
                 ):
        
        if model not in VALID_MODELS: 
            raise ValueError(f'Given model "{model}" not valid. Valid models: {VALID_MODELS}')

        self.model = model
        self.openai_key = openai_key

        if model == 'gpt-4o':
            if openai_key is None:
                raise ValueError(f'An open AI api key (not None) is needed to use "{model}"')
            else:
                self.client = OpenAI(api_key= self.openai_key)

        self.attempts = attempts
    
    def __call__(self, text:str, shot = 0, rules:str  = '', verbose:bool = False) -> Any:
        if shot == 0:
            shot = ''

        elif isinstance(shot, str): 
            shot = shot
        else:
            shot = ''
        
        if rules != '':
            rules = f"These are some extra rules you need to follow: {rules}"

        if self.model == 'gpt-4o':
            results = self.extract_gpt(text, shot, rules = rules, verbose = verbose)

        if self.model == 'groq/llama3-8b-8192':
            results = self.extract_groq(text, shot)
        return results
    

        
    def extract_gpt(self, text, shot, rules, verbose = False):
        system_prompt = SYSTEM_PROMPT_COF.format(
            SHOT = shot,
            RULES = rules
            )

        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text}
            ]

        current_attempt = 1

        while current_attempt <= self.attempts:
            if verbose:
                print(f'Current Attempt to extract data: {current_attempt} (max: {self.attempts})')
            completion = self.client.chat.completions.create(
                model=self.model,
                messages= messages,
                temperature = 0
            )
            
            extracted = completion.choices[0].message.content
            
            clean_dict, clean_status = clean_extraction(extracted, verbose=verbose)

            if clean_status:
                all_fragments = []
                for k, v in clean_dict.items():
                    res = FragmentResult(name = v['name'], linkers = v['linkers'], linkers_abbr = v['linkers_abbreviation'], linkage = v['linkage_type'])
                    all_fragments.append(res)
                return all_fragments

            else:
                current_attempt += 1

        return FailedFragmentResult(clean_dict['raw'])
    