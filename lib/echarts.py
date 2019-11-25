# coding:utf-8
from shutil import copytree, rmtree
from .data import nodes_data, edges_data
from collections import defaultdict
import os
from json import dumps


def echarts(outdir, FRA_result_file, node2type, node2entry, node2weight,
            edge2weight, ECHARTS, stand_tag=False):
    if not (node2type and node2entry and node2weight):
        node2type, node2entry, node2weight = nodes_data(FRA_result_file)
    if edge2weight is None:
        edge2weight = edges_data(FRA_result_file)
    target_dir = os.path.join(outdir, "web")
    if os.path.exists(target_dir):
        rmtree(target_dir)
    copytree(ECHARTS, target_dir)
    # year -> node -> weight
    year2node2weight = defaultdict(dict)
    for node, y2weight in node2weight.items():
        for year, weight in y2weight.items():
            year2node2weight[year][node] = weight
    # year -> edge -> weight.
    year2edge2weight = defaultdict(dict)
    for edge, y2weight in edge2weight.items():
        for year, weight in y2weight.items():
            year2edge2weight[year][edge] = weight

    # year -> node -> degree
    year2node2degree = defaultdict(dict)
    for edge, y2weight in edge2weight.items():
        for y in y2weight.keys():
            if edge[0] not in year2node2degree[y]:
                year2node2degree[y][edge[0]] = 1
            else:
                year2node2degree[y][edge[0]] += 1
            if edge[1] not in year2node2degree[y]:
                year2node2degree[y][edge[1]] = 1
            else:
                year2node2degree[y][edge[1]] += 1
    
    # calculate final data.
    data_year = defaultdict(dict)
    for year, node2weight in year2node2weight.items():
        legend = set()
        for node in node2weight.keys():
            legend.add(node2type[node])
        legend = list(legend)
        data_year[year]["legend"] = legend
        categories = []
        for cat in legend:
            dic = {}
            dic['name'] = cat
            dic['keyword'] = {}
            dic['base'] = cat
            categories.append(dic)
        data_year[year]['categories'] = categories
        nodes = []
        min_w, max_w = 0, 0
        for node, weight in node2weight.items():
            dic = {}
            dic['name'] = node
            dic['value'] = weight
            min_w = min(min_w, weight)
            max_w = max(max_w, weight)
            dic['category'] = legend.index(node2type[node])
            nodes.append(dic)
        for dic in nodes:
            dic['symbolSize'] = int((dic['value'] - min_w) / (
                max_w - min_w) * 20 + 5)

        # sort by degree
        def degree(t):
            try:
                return year2node2degree[year][t['name']]
            except KeyError:
                # just one node in some year.
                return 0
        # nodes.sort(key=degree, reverse=True)
        # sort by value
        nodes.sort(key=lambda t: t['value'], reverse=True)

        # node -> idx
        node2idx = {}
        idx = 0
        for node in (dic['name'] for dic in nodes):
            node2idx[node] = idx
            idx += 1
        # change node to node+entryname
        for dic in nodes:
            if stand_tag is False:
                # just entry name
                dic['name'] = node2entry[dic['name']]
            else:
                # standard name + entry name
                dic['name'] += "\n{}".format(node2entry[dic['name']])
        # nodes list
        data_year[year]['nodes'] = nodes

        # links list
        links = []
        for edge, weight in edge2weight.items():
            if year in edge2weight[edge]:
                dic = {}
                dic['source'] = node2idx[edge[0]]
                dic['target'] = node2idx[edge[1]]
                dic['value'] = edge2weight[edge][year]
                links.append(dic)
        links.sort(key=lambda t: t['value'], reverse=True)
        data_year[year]['links'] = links
    # write to 
    with open(os.path.join(target_dir, "data.js"), 'w') as f:
        for year, dic in data_year.items():
            f.write("var data_{}={}\n".format(year, dumps(dic, indent=2)))
