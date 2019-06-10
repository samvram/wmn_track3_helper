# -*- coding: utf-8 -*-
from TopologyHelper import TopologyHelper
import pickle as pk


def read_parse_raw_data(path):
    """
    This function is use to read OLSRD files and parse them to get the relevant information

    :param path: The relative path of the OLSRD files are present
    :return: It returns the list of file names and the topology information
    """
    file_list = TopologyHelper.get_file_list(path)
    print("Reading "+str(len(file_list))+" files from "+path)
    topology_info = []
    file_name = []
    for file in file_list:
        try:
            r = TopologyHelper.parse_file(file)
            tmp = (r[0])['Topology']
            topology_info.append(tmp)
            t = r[1]
            file_name.append(t)
        except:
            continue
    print("Parsing completed")
    return file_name, topology_info


def read_parsed_data(parsed_filename_path, parsed_topology_data_path):
    """
    This function reads the already parsed data

    :param parsed_filename_path: The path to the parsed file name list
    :param parsed_topology_data_path: The path to the parsed topology information file
    :return: It returns the list of file names and the topology information
    """
    with open(parsed_filename_path, 'rb') as f:
        file_name = pk.load(f)
    with open(parsed_topology_data_path, 'rb') as f:
        topology_info = pk.load(f)
    return file_name, topology_info


def route_information(th_object, topology_info, file_name, node1, node2, path):
    """
    This functions gets the route information data and save it to a file to the path passed as path

    :param th_object: The object of the TopologyHelper class
    :param topology_info: the list containing the topology information
    :param file_name: the relevant list of file names.
    :param node1: the starting node of the route
    :param node2: the destination node of the route
    :param path: the path where to save the .csv file, it should be path to the directory and not to the file
    :return:
    """
    save_path = path + node1 + "_" + node2 + "_vs_t2.csv"
    route_data = th_object.get_node_len_etx(topology_info, node1, node2)
    with open(save_path, "w+") as f_name:
        f_name.write("Time,No_hopes,Cost\n")
        cc = 0
        for k in file_name:
            f_name.write(str(k)[11:-7] + "," + str(route_data[cc]['hopes_count']) + "," + str(route_data[cc]['cost']) +
                         "\n")
            cc += 1
    print(node1 + " " + node2 + " route information exported")


def node_link_num(th_object, topology_info, file_name, node1, node2, path):
    """
    This function gets the ETX information of the link between two nodes vs. time and write them to the file.

    :param th_object: The object of the TopologyHelper class
    :param topology_info: the list containing the topology information
    :param file_name: the relevant list of file names.
    :param node1: one of the two node between which the link profile is to be obtained
    :param node2: one of the two node between which the link profile is to be obtained
    :param path: the path where to save the .csv file, it should be path to the directory and not to the file
    :return:
    """
    save_path = path + node1 + "_" + node2 + "_vs_t.csv"
    links_num = th_object.get_node_links_num(topology_info, file_name, [node1, node2])
    with open(save_path, "w+") as f:
        f.write("Time,No_Link\n")
        for k in file_name:
            f.write(str(k)[11:-7] + "," + str(links_num[k]) + "\n")
    print(node1 + " " + node2 + " link number exported")


def get_down_times(th_object, topology_info, path):
    """
    This function is use to get the link-down profile for th topology_info list passed

    :param th_object: The object of the TopologyHelper class
    :param topology_info: the list containing the topology information
    :param path: The path to the file where the results will be saved. It should include the file name too
    :return:
    """
    c = th_object.get_down_time(topology_info)
    nodes = list(th_object.node_loc.keys())
    with open(path, 'w') as f:
        f.write("Node1,Node2,Link down time (seconds)\n")
        for i in range(0, len(nodes)):
            node1 = nodes[i]
            for j in range(i, len(nodes)):
                node2 = nodes[j]
                if node1 != node2:
                    f.write(node1 + "," + node2 + "," + str(c[node1][node2]) + "\n")


def node_route_data(th_object, topology_info, file_name):
    """
    This function uses route_information() function to obtain route information between different nodes

    :param th_object: The object of the TopologyHelper class
    :param topology_info: the list containing the topology information
    :param file_name: the relevant list of file names.
    :return:
    """
    route_information(th_object, topology_info, file_name, "20", "91", "extracted_data/Route_data/")
    route_information(th_object, topology_info, file_name, "22", "91", "extracted_data/Route_data/")
    route_information(th_object, topology_info, file_name, "22", "71", "extracted_data/Route_data/")


def node_link_num_data(th_object, topology_info, file_name):
    """
    This function uses node_link_num() function to obtain link etx information between different nodes vs. time.

    :param th_object: The object of the TopologyHelper class
    :param topology_info: the list containing the topology information
    :param file_name: the relevant list of file names.
    :return:
    """
    # close
    node_link_num(th_object, topology_info, file_name, "20", "10", "extracted_data/Link_number/")
    node_link_num(th_object, topology_info, file_name, "20", "30", "extracted_data/Link_number/")
    node_link_num(th_object, topology_info, file_name, "22", "11", "extracted_data/Link_number/")
    node_link_num(th_object, topology_info, file_name, "22", "31", "extracted_data/Link_number/")
    node_link_num(th_object, topology_info, file_name, "22", "10", "extracted_data/Link_number/")
    node_link_num(th_object, topology_info, file_name, "20", "31", "extracted_data/Link_number/")
    node_link_num(th_object, topology_info, file_name, "20", "31", "extracted_data/Link_number/")

    # far side
    node_link_num(th_object, topology_info, file_name, "20", "70", "extracted_data/Link_number/")
    node_link_num(th_object, topology_info, file_name, "20", "90", "extracted_data/Link_number/")
    node_link_num(th_object, topology_info, file_name, "22", "71", "extracted_data/Link_number/")
    node_link_num(th_object, topology_info, file_name, "20", "91", "extracted_data/Link_number/")
    node_link_num(th_object, topology_info, file_name, "22", "70", "extracted_data/Link_number/")
    node_link_num(th_object, topology_info, file_name, "20", "91s", "extracted_data/Link_number/")


def get_event_user_input(th_object):
    eve_times = th_object.get_events()

    print('From the mentioned events type the event for which you want to observe:')
    for key in eve_times.keys():
        print(key)

    eve = input('Enter the event:')

    while eve not in eve_times.keys():
        eve = input('Enter one of the above events name :')

    print('Thank you! We are processing the request')

    start_ind = -1
    end_ind = -1
    if eve == "no_event":
        start_ind = 0
        end_ind = len(fileName) - 1
        return start_ind, end_ind, eve

    for i in range(0, len(fileName)):
        if fileName[i] >= eve_times[eve]['Start'] and start_ind == -1:
            start_ind = i
        if fileName[i] > eve_times[eve]['End'] and end_ind == -1:
            end_ind = i
            break
    return start_ind, end_ind, eve


fileName, topology_info_list = read_parsed_data('parsed_data/parsed_filenames_combined_data',
                                                'parsed_data/parsed_topology_info_combined_data')

th = TopologyHelper(freq=10)    # Create an object of the class to begin

start_index, end_index, event = get_event_user_input(th)

node_route_data(th, topology_info_list[start_index:end_index+1], fileName[start_index:end_index+1])

th.flow_topology(topology_info_list[start_index:end_index+1], fileName[start_index:end_index+1], event=event, node_name=True)
