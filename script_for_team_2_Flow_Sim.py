# -*- coding: utf-8 -*-
"""
Wireless Mesh Networks - Track III Analysis
-Samvram Sahu
"""
from datetime import datetime
from topologyHelper import topologyHelper
"""
Import the custom class for processing data,
"""

# Create an object of the class to begin
th = topologyHelper(freq=10)

# Provide the directory in which the data is present
file_list = th.getFileList('../team-10-data-total/')

# Parse a file only
topology_info = th.parseFile(file_list[0])

# Instead if you want to parse all, you can use,
topology_info_list = []
fileName = []
for file in file_list[0:500]:
    r = th.parseFile(file)
    try:
        tmp = (r[0])['Topology']
        topology_info_list.append(tmp)
        t = r[1]
        fileName.append(t)
    except KeyError:
        continue



links_num = dict.fromkeys(fileName, 0)
links_num = th.get_link_nums(topology_info_list, links_num, fileName)
with open("total_no_link_vs_t.csv", "w+") as f:
    f.write("Time,No_Link\n")
    for k in fileName:
        f.write(str(k)[11:-5]+","+str(links_num[k])+"\n")



# th.flowTopology(topology_info_list, fileName, "Hi there!", True, True)

def all_data():
    # close
    links_num = dict.fromkeys(fileName, 0)
    links_num = th.get_node_links_num(topology_info_list, links_num, fileName, ["20", "10"])
    with open("20_10_vs_t.csv", "w+") as f:
        f.write("Time,No_Link\n")
        for k in fileName:
            f.write(str(k)[11:-5] + "," + str(links_num[k]) + "\n")

    links_num = dict.fromkeys(fileName, 0)
    links_num = th.get_node_links_num(topology_info_list, links_num, fileName, ["20", "30"])
    with open("20_30_vs_t.csv", "w+") as f:
        f.write("Time,No_Link\n")
        for k in fileName:
            f.write(str(k)[11:-5] + "," + str(links_num[k]) + "\n")

    links_num = dict.fromkeys(fileName, 0)
    links_num = th.get_node_links_num(topology_info_list, links_num, fileName, ["22", "11"])
    with open("22_11_vs_t.csv", "w+") as f:
        f.write("Time,No_Link\n")
        for k in fileName:
            f.write(str(k)[11:-5] + "," + str(links_num[k]) + "\n")

    links_num = dict.fromkeys(fileName, 0)
    links_num = th.get_node_links_num(topology_info_list, links_num, fileName, ["22", "31"])
    with open("22_31_vs_t.csv", "w+") as f:
        f.write("Time,No_Link\n")
        for k in fileName:
            f.write(str(k)[11:-5] + "," + str(links_num[k]) + "\n")

    links_num = dict.fromkeys(fileName, 0)
    links_num = th.get_node_links_num(topology_info_list, links_num, fileName, ["22", "10"])
    with open("22_10_vs_t.csv", "w+") as f:
        f.write("Time,No_Link\n")
        for k in fileName:
            f.write(str(k)[11:-5] + "," + str(links_num[k]) + "\n")

    links_num = dict.fromkeys(fileName, 0)
    links_num = th.get_node_links_num(topology_info_list, links_num, fileName, ["20", "31"])
    with open("20_31_vs_t.csv", "w+") as f:
        f.write("Time,No_Link\n")
        for k in fileName:
            f.write(str(k)[11:-5] + "," + str(links_num[k]) + "\n")


    # far side

    links_num = dict.fromkeys(fileName, 0)
    links_num = th.get_node_links_num(topology_info_list, links_num, fileName, ["20", "70"])
    with open("20_70_vs_t.csv", "w+") as f:
        f.write("Time,No_Link\n")
        for k in fileName:
            f.write(str(k)[11:-5] + "," + str(links_num[k]) + "\n")

    links_num = dict.fromkeys(fileName, 0)
    links_num = th.get_node_links_num(topology_info_list, links_num, fileName, ["20", "90"])
    with open("20_90_vs_t.csv", "w+") as f:
        f.write("Time,No_Link\n")
        for k in fileName:
            f.write(str(k)[11:-5] + "," + str(links_num[k]) + "\n")


    links_num = dict.fromkeys(fileName, 0)
    links_num = th.get_node_links_num(topology_info_list, links_num, fileName, ["22", "71"])
    with open("22_71_vs_t.csv", "w+") as f:
        f.write("Time,No_Link\n")
        for k in fileName:
            f.write(str(k)[11:-5] + "," + str(links_num[k]) + "\n")

    links_num = dict.fromkeys(fileName, 0)
    links_num = th.get_node_links_num(topology_info_list, links_num, fileName, ["22", "91"])
    with open("22_91_vs_t.csv", "w+") as f:
        f.write("Time,No_Link\n")
        for k in fileName:
            f.write(str(k)[11:-5] + "," + str(links_num[k]) + "\n")

    links_num = dict.fromkeys(fileName, 0)
    links_num = th.get_node_links_num(topology_info_list, links_num, fileName, ["22", "70"])
    with open("22_70_vs_t.csv", "w+") as f:
        f.write("Time,No_Link\n")
        for k in fileName:
            f.write(str(k)[11:-5] + "," + str(links_num[k]) + "\n")

    links_num = dict.fromkeys(fileName, 0)
    links_num = th.get_node_links_num(topology_info_list, links_num, fileName, ["20", "71"])
    with open("20_71_vs_t.csv", "w+") as f:
        f.write("Time,No_Link\n")
        for k in fileName:
            f.write(str(k)[11:-5] + "," + str(links_num[k]) + "\n")

all_data()