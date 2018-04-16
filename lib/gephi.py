# coding:utf-8
import csv
import os
from .data import nodes_data, edges_data


def gephi8str(weightdic):
    """construct weight's string of gephi0.8* version dynamic network."""
    str1, str2 = "<", "<"
    start_year, end_year = min(weightdic.keys()), max(weightdic.keys())
    for year, weight in sorted(weightdic.items(), key=lambda t: t[0]):
        str1 += "[{},{},{}];".format(year - 0.5, year + 0.5, weight)
    str1 += ">"
    str2 = "<[{},{}]>".format(start_year - 0.5, end_year + 0.5)
    return str1, str2


def gephi8(outdir,
           FRA_result_file,
           node2type=None,
           node2entry=None,
           node2weight=None,
           edge2weight=None):
    """input FRA result file, output gephi8 nodes and edges csv file."""
    nodecsvfile = os.path.join(outdir, "gephi8.nodes.csv")
    edgecsvfile = os.path.join(outdir, "gephi8.edges.csv")
    gephi8_node(nodecsvfile, FRA_result_file, node2type, node2entry,
                node2weight)
    gephi8_edge(edgecsvfile, FRA_result_file, edge2weight)


def gephi8_node(nodecsvfile,
                FRA_result_file,
                node2type=None,
                node2entry=None,
                node2weight=None):
    """calculate dynamic weight of protein nodes."""
    f_node = open(nodecsvfile, 'w')
    f_node_writer = csv.writer(f_node)
    f_node_writer.writerow(['Id', 'Label', 'Type', 'score', 'Time Interval'])
    if not (node2type and node2entry and node2weight):
        node2type, node2entry, node2weight = nodes_data(FRA_result_file)
    for node in node2weight:
        str1, str2 = gephi8str(node2weight[node])
        f_node_writer.writerow(
            [node, node2entry[node], node2type[node], str1, str2])
    f_node.close()


def gephi8_edge(edgecsvfile, FRA_result_file, edge2weight=None):
    """calculate dynamic weight of protein edges."""
    f_edge = open(edgecsvfile, 'w')
    f_edge_writer = csv.writer(f_edge)
    f_edge_writer.writerow(['Source', 'Target', 'Type', 'Id', 'Weight'])
    if edge2weight is None:
        edge2weight = edges_data(FRA_result_file)
    for idx, edge in enumerate(edge2weight):
        str1, str2 = gephi8str(edge2weight[edge])
        f_edge_writer.writerow([edge[0], edge[1], 'Undirected', idx + 1, str1])
    f_edge.close()


def gephi9str(weightdic):
    """construct weight's string of gephi0.9* version dynamic network."""
    str1, str2 = "<", "<["
    for year, weight in sorted(weightdic.items(), key=lambda t: t[0]):
        str1 += "[{},{}];".format(year, weight)
        str2 += "{},".format(year)
    str1 += ">"
    str2 += "]>"
    return str1, str2


def gephi9(outdir,
           FRA_result_file,
           node2type=None,
           node2entry=None,
           node2weight=None,
           edge2weight=None):
    """input FRA result file, output gephi9 nodes and edges csv file."""
    nodecsvfile = os.path.join(outdir, "gephi9.nodes.csv")
    edgecsvfile = os.path.join(outdir, "gephi9.edges.csv")
    gephi9_node(nodecsvfile, FRA_result_file, node2type, node2entry,
                node2weight)
    gephi9_edge(edgecsvfile, FRA_result_file, edge2weight)


def gephi9_node(nodecsvfile,
                FRA_result_file,
                node2type=None,
                node2entry=None,
                node2weight=None):
    """calculate dynamic weight of protein nodes."""
    f_node = open(nodecsvfile, 'w')
    f_node_writer = csv.writer(f_node)
    f_node_writer.writerow(['Id', 'Label', 'Type', 'Timestamp', 'score'])
    if not (node2type and node2entry and node2weight):
        node2type, node2entry, node2weight = nodes_data(FRA_result_file)
    for node in node2weight:
        str1, str2 = gephi9str(node2weight[node])
        f_node_writer.writerow(
            [node, node2entry[node], node2type[node], str2, str1])


def gephi9_edge(edgecsvfile, FRA_result_file, edge2weight=None):
    """calculate dynamic weight of protein edges."""
    f_edge = open(edgecsvfile, 'w')
    f_edge_writer = csv.writer(f_edge)
    f_edge_writer.writerow(
        ['Source', 'Target', 'Type', 'Id', 'Timestamp', 'Weight'])
    if edge2weight is None:
        edge2weight = edges_data(FRA_result_file)
    for idx, edge in enumerate(edge2weight):
        str1, str2 = gephi9str(edge2weight[edge])
        f_edge_writer.writerow(
            [edge[0], edge[1], 'Undirected', idx + 1, str2, str1])
    f_edge.close()
