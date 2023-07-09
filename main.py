from xml import *
from pathlib import Path


if not open('rootdir.txt'):
    rootdir = input('Informe o caminho: \n')
    with open('rootdir.text', 'w') as f:
        f.write(rootdir)

with open('rootdir.txt', 'r') as file:
    root = file.readline()
    