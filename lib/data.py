# coding:utf-8
import csv
from collections import Counter, defaultdict
from itertools import combinations


def nodes_data(FRA_result_file):
    """
    extract node data from FRA_result_file.

    Returns
    -------
    node2type: dict
        node -> type
    node2entry: dict
        node -> entryname(label)
    node2weight: dict
        node -> weight(ref README.md)
    """
    year2totalnum = defaultdict(lambda: 0)
    node2YearNum = defaultdict(lambda: [])
    node2type = defaultdict(lambda: "")
    node2entry = defaultdict(lambda: "")
    f = open(FRA_result_file, 'r')
    reader = csv.reader(f)
    for line in reader:
        PMID, PublishYear, ProteinType, Abb, EntryName, NameInAbstract = line
        if PMID != "PMID":
            try:
                year = int(PublishYear)
                node = Abb
                if node not in node2entry:
                    node2entry[node] = EntryName
                if node not in node2type:
                    node2type[node] = ProteinType
                node2YearNum[node].append(year)
                year2totalnum[year] += 1
            except Exception as e:
                print("{}: {}".format(PMID, e))
    year2accnum = defaultdict(lambda: 0)
    acc = 0
    for y, n in sorted(year2totalnum.items(), key=lambda t: t[0]):
        year2accnum[y] = acc + n
        acc += n
    node2weight = defaultdict(lambda: {})
    for node in node2YearNum:
        exist_year = Counter(node2YearNum[node])
        for y, s in year2accnum.items():
            if y >= min(exist_year.keys()):
                node2weight[node][y] = sum(
                    [ne for ye, ne in exist_year.items() if ye <= y]) * 1.0 / s
    f.close()
    return node2type, node2entry, node2weight


def edges_data(FRA_result_file):
    """
    extract edge data from FRA_result_file.

    Returns
    -------
    edge2weight: dict
        edge -> weight(ref README.md)
    """
    edge2year = defaultdict(lambda: [])
    f = open(FRA_result_file, 'r')
    reader = csv.reader(f)
    nodes = set()
    tmp_PMID = ""
    tmp_DP = 0
    for items in reader:
        """
        'PMID', 'PublishYear', 'ProteinType',
        'Abb', 'EntryName', 'NameInAbstract'
        """
        if items[0] != "PMID":
            PMID, DP, TY, AB, EN, NA = items
            if PMID != tmp_PMID and tmp_PMID != "":
                # print tmp_PMID, tmp_DP, nodes
                for nodei, nodej in combinations(nodes, 2):
                    edge2year[tuple(sorted([nodei, nodej]))].append(
                        int(tmp_DP))
                nodes.clear()
            # else:
            nodes.add(AB)
            tmp_PMID = PMID
            tmp_DP = int(DP)
    # don't forget the last one
    for nodei, nodej in combinations(nodes, 2):
        edge2year[tuple(sorted([nodei, nodej]))].append(int(tmp_DP))
    year2num = defaultdict(lambda: 0)
    for edge, years in edge2year.items():
        for year in years:
            year2num[year] += 1
    year2accnum = defaultdict(lambda: 0)
    edge2weight = defaultdict(dict)
    acc = 0
    for y, n in sorted(year2num.items(), key=lambda t: t[0]):
        year2accnum[y] = acc + n
        acc += n
    for edge in edge2year:
        exist_year = Counter(edge2year[edge])
        for y, s in year2accnum.items():
            if y >= min(exist_year.keys()):
                edge2weight[edge][y] = sum(
                    [ne for ye, ne in exist_year.items() if ye <= y]) * 1.0 / s
    return edge2weight


if __name__ == '__main__':
    edge2weight = edges_data("../test/FRA_result.csv")
    print(edge2weight)
