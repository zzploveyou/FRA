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


def run(PATH,
        inputfile,
        outdir,
        term="",
        database="proteins.txt",
        max_num=0,
        email="test1@mail.nankai.edu.cn"):
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
            edge2weight, ECHARTS)
    print("[+] done.")


if __name__ == '__main__':
    PATH = os.path.dirname(os.path.realpath(__file__))
    parser = argparse.ArgumentParser(
        description="fast review algorithms[FRA] of human proteins network \
        towards MEDLINE file")
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
        help="specify database, proteins.txt / diseases.txt")
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
        version='%(prog)s 1.3 created by Zhang Zhaopeng')
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
