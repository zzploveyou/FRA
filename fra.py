#!/usr/bin/python
# coding:utf-8
"""
fast review algorithm of human proteins network
towards PubMed papers.

Author: Zhaopeng Zhang
Email : zhangzhaopeng@mail.nankai.edu.cn
"""
import argparse
import os
import sys

# from lib.gephi import gephi9
from lib.data import edges_data, nodes_data
from lib.echarts import echarts
from lib.gephi import gephi8
from lib.pubmed import PMID_DP_AB
from lib.search import find_proteins
from tools import integrate_associated_entries, reduce_from_resultcsv


def run(PATH,
        inputfile,
        outdir,
        term="",
        database="proteins.txt",
        max_num=0,
        email="test1@mail.nankai.edu.cn",
        stand_tag=False):
    """input pubmed_result.txt, output results to outdir."""
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    pmid_dp_ab = PMID_DP_AB(
        medlinefile=inputfile, term=term, max_num=max_num, email=email)
    """find proteins,write to FRA_result_file"""
    FRA_result_file = os.path.join(outdir, "FRA_result.csv")
    ECHARTS = os.path.join(PATH, "echarts-example")
    FRA_DATABASE = os.path.join(PATH, database)
    EXCLUDE_FILE = os.path.join(PATH, "exclude_names.txt")
    print("FRA database: {}".format(FRA_DATABASE))
    print("exclude name list: {}".format(EXCLUDE_FILE))
    find_proteins(pmid_dp_ab, FRA_result_file, FRA_DATABASE, EXCLUDE_FILE)
    """extract information of nodes, edges"""
    node2type, node2entry, node2weight = nodes_data(FRA_result_file)
    edge2weight = edges_data(FRA_result_file)
    """gephi output file."""
    gephi8(outdir, FRA_result_file, node2type, node2entry, node2weight,
           edge2weight)
    # gephi9(outdir, FRA_result_file, node2type, node2entry, node2weight,
    #        edge2weight)
    """echarts"""
    echarts(outdir, FRA_result_file, node2type, node2entry, node2weight,
            edge2weight, ECHARTS, stand_tag)
    """fra-tools"""
    manual_dir = os.path.join(outdir, "manual")
    if not os.path.exists(manual_dir):
        os.makedirs(manual_dir)
    integrate_associated_entries(
        entry_name="test",
        FRA_result_csvfile=FRA_result_file,
        output_csv=os.path.join(manual_dir, "result.csv"))
    reduce_from_resultcsv(
        resultcsv=os.path.join(manual_dir, "result.csv"),
        medlinefile=inputfile,
        result_readable=os.path.join(manual_dir, "FRA_readable.txt"),
        result_medline=os.path.join(manual_dir, "FRA_medline.txt"))
    print("[+] done.")


if __name__ == '__main__':
    PATH = os.path.dirname(os.path.realpath(__file__))
    parser = argparse.ArgumentParser(
        description="""
        fast review algorithms[FRA] of human proteins network towards MEDLINE file.
        
        For Example:
            python fra.py -o test/ -m test/pubmed_result.txt
            python fra.py -d diseases.txt -o test/ -m test/pubmed_result.txt
            python fra.py -t 'nankai[Title/Abstract]' -o outdir/ -m outdir/pubmed_result.txt""",
        formatter_class=argparse.RawTextHelpFormatter)
    required = parser.add_argument_group('required arguments')
    required.add_argument(
        "-m",
        dest="medfile",
        type=str,
        help="specify MEDLINE file.",
        required=True)
    required.add_argument(
        "-o",
        dest="outdir",
        type=str,
        help="specify output dir.",
        required=True)
    parser.add_argument(
        '-t',
        '--term',
        type=str,
        default="",
        help="specify term for PubMed querying.")
    parser.add_argument(
        '-d',
        '--database',
        type=str,
        default="proteins.txt",
        help="specify database: proteins.txt(default) / diseases.txt")
    parser.add_argument(
        '-n',
        dest="NUM",
        type=int,
        default=0,
        help="specify download num, download all if not specified.")
    parser.add_argument(
        '--email',
        default="test.mail.nankai.edu.cn",
        help="Email for indentification for PubMed.")
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 1.4 created by Zhang Zhaopeng')
    args = parser.parse_args()
    if args.medfile and args.outdir:
        run(PATH,
            args.medfile,
            args.outdir,
            term=args.term,
            database=args.database,
            max_num=args.NUM,
            email=args.email)
    else:
        sys.exit("python2 {} -h".format(__file__))
