
VALID_MODELS = ['gpt-4o', 'groq/llama3-8b-8192', 'o3-mini']

SYSTEM_PROMPT_COF = "You are a helpfull scientist. Answer very accurate. If you are not sure, say this in the answer. What are the organic linkers of the Covalent Organic Framworks (COFs) (as described in the article)? First ask yourself how many COFs are described in the paper. Give for every MOF the synthesis conditions.{SHOT}\n {RULES}"

RULES = '''
The given text is a research article about Covalent Organic Frameworks (COFs). I want to know the chemical building blocks, or linkers, that make the COF.
1) It may happen that the paper describes more than one synthesis of a COFs. For every COF find the linkers.
2) Give the output in a json object. Use the exact format as the provided examples. 
Additionaly, I want you to follow these rules:
3) Give only the json object, do not give any other text!
4)Try to keep the string short . Exclude comments out of the json output . Return one json object .
5) If there are any abbreviation of chemicals, give both strings in the approriate format!
Extract the following information, if one of the conditions is not given, return the STRING None:
reaction: = {'COFF1': {'name': 'Name of the COF ' as STRING,
                   'linkers': 'Full Name of the linkers' as LIST of STRINGs,
                   'linkers_abbreviation': 'Abbreviation of the linkers if given' as LIST of STRINGs, return None if not given
                   'linkage_type': 'Linkage type of COF if given', as STRING, return None if not given
                   }
'''