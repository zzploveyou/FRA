"""
2018-09-19 by Zhaopeng Zhang

1. Search entry_name[Title/Abstract] in [PubMed](http://www.ncbi.nlm.nih.gov/pubmed/)
2. Run FRA(specify associated_entries database) to get associated_entries network.
3. Run this script to merge related associated_entries and reduce medline result.
    Func: integrate_associated_entries, 

"""
import csv
from collections import defaultdict
# from pyexcel.cookbook import merge_all_to_a_book
import lib.medline as Medline
import textwrap
import re


def integrate_associated_entries(entry_name,
                       FRA_result_csvfile="FRA_result.csv",
                       output_csv="result.csv"):
    """
    FRA_result_csvfile:
        PMID, Publish Year, ProteinType, Abb, EntryName, NameInAbstract
    
    Change FRA_result_csvfile into output_csv:
        Protein(Gene), associated_entries, PMIDs
        Protein(Gene), Proteins, PMIDs
    """
    results = defaultdict(list)
    f = open(FRA_result_csvfile)
    reader = csv.reader(f)
    n = 0
    for PMID, PY, TY, ABB, EN, ENA in reader:
        if n == 0:
            n = 1
        else:
            results[PMID].append(ENA)
    edges = defaultdict(list)
    for PMID, result in results.items():
        if len(result) >= 2:
            for i in result:
                # i is a associated_entries name, entry_name is your protein(gene)
                edges[(entry_name, i)].append(PMID)
    number_associated_entries = 0
    with open(output_csv, 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(['Entry', 'Associated-associated_entries', 'PMIDs'])
        for (i, j), ps in edges.items():
            number_associated_entries += 1
            writer.writerow([i, j, ", ".join(ps)])
    # convert csv into xlsx file.
    # xlsxfile = os.path.splitext(output_csv)[0] + ".xlsx"
    # merge_all_to_a_book([output_csv], xlsxfile)
    print("read from {}, write into {}".format(FRA_result_csvfile, output_csv))
    print("entry_name: {}, number of associated_entries: {}".format(
        entry_name, number_associated_entries))


def parser(medlinefile):
    with open(medlinefile, 'r') as handle:
        records = Medline.parse(handle)
        for record in records:
            yield (record.get("PMID", "?"), record.get("DP", ""),
                   record.get("TI", "?"), record.get("AB", ""))


def reduce_to_readable(medlinefile, pmids, resultfile="pubmed_result2.txt"):
    """change to readable txt."""
    num = 1
    with open(resultfile, 'w') as f:
        for pmid, dp, ti, ab in parser(medlinefile):
            ab = "\n".join(textwrap.wrap(ab, width=85))
            ti = "\n".join(textwrap.wrap(ti, width=85))
            if pmid in pmids:
                f.write("PMID: {}, {}\n{}. {}\n\n{}\n\n".format(
                    pmid, dp, num, ti, ab))
                num += 1


def reduce_to_medline(medlinefile, pmids, resultfile="pubmed_result3.txt"):
    """change to subset of MEDLINE text."""
    with open(resultfile, 'w') as f:
        f.write("\n")
        content = open(medlinefile).read()
        for paper in re.findall("PMID.*?\n\n|PMID.*?\n$", content, re.S):
            pmid = paper[6:paper.index("\n")]
            if pmid in pmids:
                f.write(paper)


def reduce_from_resultcsv(resultcsv="example/result.csv",
                          medlinefile="example/pubmed_result.txt",
                          result_readable="example/FRA_readable.txt",
                          result_medline="example/FRA_medline.txt"):
    pmids = set()
    with open(resultcsv) as f:
        reader = csv.reader(f)
        next(reader)
        for gene, associated_entries, pds in reader:
            for pmid in pds.split(","):
                pmids.add(pmid.strip())
    reduce_to_readable(medlinefile, pmids, result_readable)
    reduce_to_medline(medlinefile, pmids, result_medline)


if __name__ == '__main__':
    integrate_associated_entries(
        entry_name="test",
        FRA_result_csvfile="test/FRA_result.csv",
        output_csv="test/manual/result.csv")
    reduce_from_resultcsv(
        resultcsv="test/manual/result.csv",
        medlinefile="test/pubmed_result.txt",
        result_readable="test/manual/FRA_readable.txt",
        result_medline="test/manual/FRA_medline.txt")
