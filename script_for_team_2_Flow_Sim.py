# -*- coding: utf-8 -*-
"""
Wireless Mesh Networks - Track III Analysis
-Samvram Sahu
"""

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
for file in file_list[1:1000]:
    topology_info_list.append(th.parseFile(file)['Topology'])
    fname = (file['file_name'])[11:-8]
    fname = fname.replace('_', ":")
    fileName.append(fname)


# Represent the topology only uncomment the below
# topology = topology_info('Topology')
# th.representTopology(topology)
th.get_link_nums(topology_info_list, fileName)

# A flow topology
th.flowTopology(topology_info_list,fileName,"Hi there!", True, True)


