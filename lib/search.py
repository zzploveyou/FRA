import csv
import ahocorasick  # import ahocorasick


def actree(FRA_database, excludefile):
    """
    create actree for muti-string-search.

    Parameters
    ----------
    FRA_database: str
        database txt file of FRA.
    excludefile: str
        exclude names from excludefile,
        some words are not abbr of some proteins.

    Returns
    -------
    tree
        ahocorasick keywordTree.
    lower_name_dic: dict
        map of keyword to protein information.
    """
    exs = set()
    with open(excludefile, 'r') as f:
        for line in f:
            exs.add(line.strip().lower())
    tree = ahocorasick.KeywordTree()
    lower_name_dic = {}
    names, types = set(), ""
    entry_name = ""
    for line in open(FRA_database):
        if line.startswith("Entry:"):
            if entry_name != "":
                for name in names:
                    lower_name = name.lower()
                    if lower_name != "" and lower_name not in exs:
                        abb = min(names, key=len)
                        lower_name_dic[lower_name] = (entry_name, abb, types,
                                                      name)
                        tree.add(lower_name)
                names = set()
                types = ""
            entry = line[6:].strip()
            if entry != "":
                names.add(entry)
        if line.startswith("Name :"):
            ns = line[6:].strip().split(";")
            for name in ns:
                if name != "":
                    names.add(name)
            entry_name = ns[0]
        if line.startswith("Gene :"):
            gene = line[6:].strip()
            if gene != "N/A" and gene != "":
                names.add(gene)
        if line.startswith("Type :"):
            types = line[6:].strip()
    tree.make()
    return tree, lower_name_dic


def find_proteins(pmid_dp_ab, outputfile, FRA_database, excludefile):
    """
    search proteins in MEDLINE format file.

    Parameters
    ----------
    inputfile: pmid_dp_ab
        iter of (PMID, DP, AB).
        see Func: PMID_DP_AB.

    outputfile: str
        output filename, store PMID, PublishYear, Protein ...

    Returns
    -------
    None
    """
    fw = open(outputfile, 'w')
    writer = csv.writer(fw)
    writer.writerow([
        'PMID', 'PublishYear', 'ProteinType', 'Abb', 'EntryName',
        'NameInAbstract'
    ])
    # Aho-Corasick automaton algorithm
    tree, lower_name_dic = actree(FRA_database, excludefile)
    # parser of MEDLINE format file.
    p = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890-")
    for PMID, DP, AB in pmid_dp_ab:
        proteins = set()
        AB = AB.lower()
        for match in tree.findall_long(AB):
            if AB[match[0]:match[1]] not in proteins:
                # fake protein name, part of a string.
                if AB[match[0] - 1] not in p and AB[match[1]] not in p:
                    proteins.add(AB[match[0]:match[1]])
        for protein in proteins:
            entry_name, abb, types, name = lower_name_dic[protein]
            # if proteins exists in the paper.
            writer.writerow(
                [PMID, DP.split()[0], types, abb, entry_name, name])
    fw.close()
