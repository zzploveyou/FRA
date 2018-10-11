# coding:utf-8
import os
import sys

from Bio import Entrez  # Active only when "query item" is specified.

import medline as Medline  # from Bio import Medline


def get_retmax(term, email):
    """
    get papers number of the term.

    Parameters
    ----------
    term: str
        search term in [PubMed](https://www.ncbi.nlm.nih.gov/pubmed/)
    email: str
        email that needed for query from PubMed.

    Returns
    -------
    papers number that related with the input term.

    """
    Entrez.email = email
    handle = Entrez.egquery(term=term)
    record = Entrez.read(handle)
    for row in record["eGQueryResult"]:
        if row["DbName"] == "pubmed":
            return int(row["Count"])


def get_idlist(term, email, retmax=1000):
    """
    get PMID idlist of the term.

    Parameters
    ----------
    term: str
        search term in [PubMed](https://www.ncbi.nlm.nih.gov/pubmed/)
    email: str
        email that needed for query from PubMed.
    retmax: int
        the limit of query idlist.

    Returns
    -------
    idlist: list
        idlist of papers.
    """
    Entrez.email = email
    handle = Entrez.esearch(db="pubmed", term=term, retmax=retmax)
    record = Entrez.read(handle)
    idlist = record["IdList"]
    handle.close()
    return idlist


def get_medline(idlist):
    """
    get medline content from idlist.
    sometimes, large idlist will get HTTP error.

    Parameters
    ----------
    idlist: list
        idlist of PMID.
    
    Returns
    -------
        medline content of PMID from idlist.
    """
    try:
        handle = Entrez.efetch(
            db="pubmed", id=idlist, rettype="medline", retmode="text")
        return handle.read()
        handle.close()
    except Exception as e:
        sys.exit("{}".format(e))


def PMID_DP_AB(medlinefile,
               term="",
               max_num=0,
               email="test1@mail.nankai.edu.cn"):
    """
    parse PMID, DP, AB information from medlinefile.
    if specify term, then get file from online.
    you should specify email as identification for PubMed.

    ---------
    Attention
        when specify term,
        if number of related papers is too large, will cause HTTP error.
        you can specify max_num to download. 
        For example: retmax=10000, max_num=1000

    Parameters
    ----------
    medlinefile: str
        PubMed medline result file.
    term: str
        default: ''
        specify term for PubMed querying.
    max_num: int
        default: 0
    email: str
        default: 'test1@mail.nankai.edu.cn'

    Returns
    -------
        iter of (PMID, DP, AB).
    """
    if term != "":
        retmax = 0
        if max_num != 0:
            retmax = int(max_num)
        else:
            # online searching and download, parse MEDLINE.
            retmax = get_retmax(term=term, email=email)
            print("[+] Found {} papers related to '{}'.".format(retmax, term))
        # get idlist
        idlist = get_idlist(term=term, email=email, retmax=retmax)
        # get medline content
        content = get_medline(idlist)
        if medlinefile is not None:
            print("[+] Write to local medline file >>> {}".format(medlinefile))
            with open(medlinefile, 'w') as f:
                f.write(content)
    # parse from local MEDLINE file.
    if os.path.exists(medlinefile):
        with open(medlinefile, 'r') as handle:
            print(
                "[+] Parse from local medline file <<< {}".format(medlinefile))
            records = Medline.parse(handle)
            for record in records:
                yield (record.get("PMID", "?"), record.get("DP", ""),
                       record.get("TI", "?") + record.get("AB", ""))
    else:
        sys.exit("Not found: {}".format(medlinefile))
