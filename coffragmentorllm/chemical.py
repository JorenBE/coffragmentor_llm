from rdkit import Chem
from rdkit.Chem import Draw
import matplotlib.pyplot as plt
import pubchempy as pcp
from typing import Union


class Chemical():
    def __init__(self, 
                 name:str):
        
        self.name = name
        
        self.smiles_pc = None
        self.iupac = None

        self.pubchem = None

        self.search_pubchem()
    
    def __repr__(self):
        return self.name

    def search_pubchem(self, return_single = True) -> Union[pcp.Compound, list]:
        try:
            res = pcp.get_compounds(self.name, namespace='name')
            if return_single and len(res) !=0:
                res = res[0]

                self.pubchem = res
                self.smiles_pc = res.isomeric_smiles
                self.iupac = res.iupac_name
            else:
                return res
        except:
            res = None
        return res
        
    def show_molecule(self):
        if self.smiles_pc is None:
            print(f'None to display for Chemical named {self.name}')
        else:
            m = Chem.MolFromSmiles(self.smiles_pc)
            img = Draw.MolToImage(m)

            plt.imshow(img)
            plt.axis("off")  # Remove axis for better visualization
            plt.show()