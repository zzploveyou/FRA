# Run

## windows
```
GUI.exe
```

## linux
```bash

python 2.7

help:
    python fra.py -h

fra with local medline file:
    python fra.py -i test/pubmed_result.txt -o test

# This script can download medline file from input "term" if Bio package was installed.
# But, sometimes PubMed will restrict download from script.
# you will get HTTPError 403.
fra(download from term automatically):
    python fra.py -i test2/pubmed_result.txt -o test2 --term "PIM1"
```




Description of network weight
```
if two human proteins exists in the same paper,
then construct an edge between them with publish year label.

weight of a protein(node):
    Y = year
    N = number of papers those have mentioned the protein before Y.
    T = number of mentioned times of all proteins bofore Y.
    Define:
        Weight(protein, Y) = N(Y)/T(Y)
weight of a protein-pair(edge):
    Y = year
    N = number of papers those have mentioned the protein-pair before Y.
    T = number of mentioned times of all protein-pairs bofore Y.
    Define:
        Weight(protein-pair, Y) = N(Y)/T(Y)
```

# about Gephi
[download Gephi](https://gephi.org/users/download/)
```
before install gephi, you should install jdk.
gephi8.*.csv are for gephi0.8*
gephi9.*.csv are for gephi0.9*
```

# how to use Gephi

1. 
2.
3.
4.
5.
6.


# download MEDLINE manually

![download](download.jpg)



