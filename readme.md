# Better Data

This repository contains the solution to the BD coding challenge for a python and pandas role.  

We can differentiate two parts in this repo:
- Jupyter Notebook
- The rest of the files

## Jupyter Notebook

A jupyter notebook has been created with the whole thought process, and the solution to the problem. It also contains ideas that are not part of the final solution but that help us understand better the problem.

### Install

It requires only two dependencies, jupyter notebook and pandas. These are already included in Anaconda. Alternatively, we can use pip or miniconda to download them:

```
conda install pandas
conda install jupyter
```
or

```
pip install pandas
pip install jupyter
```


### Start

```jupyter notebook```

## The rest of the repository

The rest of the repository contains the same code as the jupyter, but better organized, refactored and with tests. 

For example, we can change what we consider an address, or a name, by editting a setting in main.py, and the program will not break (as long as it is part of the columns of the csv, of course).

### Install

Same as before, but this time we only need pandas.
```
pip install pandas
``` 
### Start

```python main.py```

### Test

There are 6 unittests, that can be run like this:

```python -m unittest discover -s test/ -v```
