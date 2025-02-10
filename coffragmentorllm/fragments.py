from typing import List
from .chemical import Chemical
import math
from rdkit import Chem
from rdkit.Chem import Draw
import matplotlib.pyplot as plt

class LinkerCollection():
    def __init__(self, linkers:List[str]):
        self.linkers = [Chemical(linker) for linker in linkers]

    def __iter__(self):
        return iter(self.linkers)
        
    def __repr__(self):
        return f"LinkerCollection({self.linkers})"
    
    def display(self, cols = 2, figsize = (10,10)):
        linkers = [linker.smiles_pc for linker in self.linkers]

    
        num_molecules = len(linkers)
        rows = math.ceil(num_molecules / cols)
        
        fig, axes = plt.subplots(rows, cols, figsize=figsize)
    
        if rows == 1 and cols == 1:
            axes = [axes]
        elif rows == 1 or cols == 1:
            axes = list(axes)
        else:
            axes = axes.flatten()
    
        for i, smiles in enumerate(linkers):

            if smiles is None or not isinstance(smiles, str) or smiles.strip() == "":

                axes[i].text(0.5, 0.5, "None or empty SMILES", fontsize=12,
                            horizontalalignment='center',
                            verticalalignment='center',
                            wrap=True)
            else:
                mol = Chem.MolFromSmiles(smiles)
                if mol is None:

                    axes[i].text(0.5, 0.5, smiles, fontsize=12,
                                horizontalalignment='center',
                                verticalalignment='center',
                                wrap=True)
                else:
                    img = Draw.MolToImage(mol)
                    axes[i].imshow(img)
            axes[i].axis("off")  
        
        for j in range(num_molecules, len(axes)):
            axes[j].axis("off")
        
        plt.tight_layout()
        plt.show()

            

class FragmentResult():
    def __init__(self, name:str, linkers:List[str], linkers_abbr: List[str], linkage: str):
        self.name = name
        self.linkers = LinkerCollection(linkers)
        self.linkers_abbr = linkers_abbr
        self.linkage = linkage

class FailedFragmentResult():
    def __init__(self, raw_extraction):
        self.raw_extraction = raw_extraction