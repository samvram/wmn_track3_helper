from datetime import datetime
from topologyHelper import topologyHelper
"""
Import the custom class for processing data,
"""

# Create an object of the class to begin
th = topologyHelper(freq=10)

# Provide the directory in which the data is present
file_list = th.getFileList('data')

# Get time of occurence of various events
event_times = th.getEvents()
print('From the mentioned events type the event for which you want to observe:')
for key in event_times.keys():
    print(key)

event = input('Enter the event:')

while event not in event_times.keys():
    event = input('Enter the event name correct:')

print('Thank you! We are processing the request')

# Instead if you want to parse all, you can use,
topology_info_list = []
fileName = []
for file in file_list:
    file_time = datetime.strptime(file['file_name'][0:-3], '%Y-%m-%d_%H_%M_%S.%f')
    if file_time <event_times[event]['End'] and file_time > event_times[event]['Start']:
        topology_info = th.parseFile(file)
        try:
            topology_info_list.append(topology_info['Topology'])
        except KeyError:
            continue
        fname = (file['file_name'])[11:-8]
        fname = fname.replace('_', ":")
        fileName.append(fname)
    if file_time > event_times[event]['End']:
        break

# Enter the list of nodes for Observation
list_of_nodes_to_Show = ['63']

# A flow topology
th.flowTopology(topology_info_list, fileName, event=event, plotSarath=True, node_name=True, node_to_show=list_of_nodes_to_Show)
