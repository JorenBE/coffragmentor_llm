# coffragmentor_llm

Extracting the linkers of COFs from the paper using Large Language Models, i.e. OpenAI's gpt-4o

## 💪 Getting Started

Reads the pdf file of a COF paper.
```python
paper = "path/to/paper.pdf"
cof = COFPaper(paper)
```

Fragment the COF. Returns a list of ```FragmentResult``` for every COF found in the paper. 

```python
OPENAI_KEY = "YOUR OPENAI KEY"
cof_fragments = cof.fragment(OPENAI_KEY)
```

Get the extracted data.

```python
cof_fragments[0].name
cof_fragments[0].linkers
cof_fragments[0].linkers_abbr
cof_fragments[0].linkage
```
You can search PubChem for the linkers. If the extracted name is not found in PubChem, None will be returned

```python
cof_fragments[0].linkers[0].search_pubchem()
```

If you are in a Jupyter notebook you can visualize the components. The molecule will only be displayed if it is found in PubChem.

individually
```python
cof_fragments[0].linkers[0].show_molecule()
```
or togheter
```python
cof_fragments[0].linkers.show_molecules()
```
