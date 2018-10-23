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
th = topologyHelper()

# Provide the directory in which the data is present
file_list = th.getFileList('../10_10_10_22/track3_exp_data/data/')

# Parse a file only
topology_info = th.parseFile(file_list[1000])

# Instead if you want to parse all, you can use,
# topology_info_list = []
# for file in file_list:
#     topology_info_list.append(th.parseFile(file))

# Access the topology file
topology = topology_info['Topology']

# Represent the topology
th.representTopology(topology, (file_list[1000])['file_name'])

