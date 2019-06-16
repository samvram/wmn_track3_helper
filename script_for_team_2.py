# -*- coding: utf-8 -*-
from TopologyHelper import TopologyHelper
import pickle as pk
import multiprocessing as mp
import numpy as np


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


def read_networkx_data(parsed_filename_path, networkx_path):
    """

    :param parsed_filename_path: The path to the parsed file name list
    :param networkx_path: The path to the list of networkx graphs
    :return: It returns the list of file names and the list of networkx graphs
    """
    with open(parsed_filename_path, 'rb') as f:
        file_name = pk.load(f)
    with open(networkx_path, 'rb') as f:
        networkx_list = pk.load(f)
    return file_name, networkx_list


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


def node_link_num(th_object, start, end, file_name, node1, node2, path):
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
    links_num = th_object.get_node_links_num(start, end, file_name, [node1, node2])
    with open(save_path, "w+") as f:
        f.write("Time,No_Link\n")
        for k in file_name:
            f.write(str(k)[11:-7] + "," + str(links_num[k]) + "\n")
    print(node1 + " " + node2 + " link number exported")


def get_down_times(th_object, start, end, path, export_all_down=False):
    """
    This function is use to get the link-down profile for th topology_info list passed

    :param th_object: The object of the TopologyHelper class
    :param start: start index of the analysis
    :param end: end index of the analysis
    :param path: The path to the file where the results will be saved. It should include the file name too
    :param export_all_down: If false then the data regarding the link between the nodes which are always down is not
    written to the csv file. By default it is false
    :return:
    """
    c = th_object.get_down_time(start, end)
    nodes = list(th_object.node_loc.keys())
    with open(path, 'w') as f:
        f.write("Node1,Node2,Link down time (seconds)\n")
        for i in range(0, len(nodes)):
            node1 = nodes[i]
            for j in range(i, len(nodes)):
                node2 = nodes[j]
                if node1 != node2:
                    if not export_all_down:
                        if c[node1][node2] != (end - start + 1):
                            f.write(node1 + "," + node2 + "," + str(c[node1][node2]) + "\n")
                    else:
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


def node_link_num_data(th_object, start, end, file_name):
    """
    This function uses node_link_num() function to obtain link etx information between different nodes vs. time.

    :param th_object: The object of the TopologyHelper class
    :param start: start index of the analysis
    :param end: end index of the analysis
    :param file_name: the relevant list of file names.
    :return:
    """
    # close
    node_link_num(th_object, start, end, file_name, "20", "10", "extracted_data/Link_number/")
    node_link_num(th_object, start, end, file_name, "20", "30", "extracted_data/Link_number/")
    node_link_num(th_object, start, end, file_name, "22", "11", "extracted_data/Link_number/")
    node_link_num(th_object, start, end, file_name, "22", "31", "extracted_data/Link_number/")
    node_link_num(th_object, start, end, file_name, "22", "10", "extracted_data/Link_number/")
    node_link_num(th_object, start, end, file_name, "20", "31", "extracted_data/Link_number/")
    node_link_num(th_object, start, end, file_name, "20", "31", "extracted_data/Link_number/")

    # far side
    node_link_num(th_object, start, end, file_name, "20", "70", "extracted_data/Link_number/")
    node_link_num(th_object, start, end, file_name, "20", "90", "extracted_data/Link_number/")
    node_link_num(th_object, start, end, file_name, "22", "71", "extracted_data/Link_number/")
    node_link_num(th_object, start, end, file_name, "20", "91", "extracted_data/Link_number/")
    node_link_num(th_object, start, end, file_name, "22", "70", "extracted_data/Link_number/")
    node_link_num(th_object, start, end, file_name, "20", "91s", "extracted_data/Link_number/")


def get_total_link_num(th_object, start, end, filename, path):

    ln = th_object.get_link_nums(start, end, filename)
    with open(path, 'w') as f:
        f.write("Time,No_Link \n")
        for k, v in ln.items():
            f.write(str(k.date())+","+str(v)+"\n")


def testing(list):
    for i in list:
        print(i)


def get_cliques_data(th_object, start, end, filename, path, num):
    last = start
    delta = int((end + 1 - start) / num)
    points = []

    while last < end + 1:
        points.append(int(last))
        last += delta
    points.append(end)

    cliques_num = []
    max_cliques = []
    for i in range(num):
        cliques_num.append(mp.Manager().dict())
        max_cliques.append(mp.Manager().Value('i', 2))

    processes = []
    for i in range(num):
        p = mp.Process(target=th_object.get_cliques_data, args=(points[i], points[i+1], filename, cliques_num[i],
                                                                max_cliques[i]))
        processes.append(p)
        print('Starting process', i)
        p.start()
        print('Process', i, ' started')

    for i in processes:
        i.join()

    max_clique = 0
    for i in max_cliques:
        if i.value > max_clique:
            max_clique = i.value

    print('All processes are over')
    # cliques_num = dict()
    # max_clique = 0
    # th_object.get_cliques_data(start, end, filename, cliques_num, max_clique)
    # print('Starting the write operation')
    with open(path, 'w') as f:
        f.write("Time")
        for i in range(2, max_clique + 1):
            f.write(","+str(i))
        f.write("\n")
        for cc in cliques_num:
            for k, v in cc.items():
                # print('Key: ', k)
                # print('Value: ', v)
                f.write(str(k.time()))
                counter = 0
                for vv in v:
                    f.write("," + str(vv))
                    counter += 1
                while counter < max_clique + 1:
                    f.write(",0")
                    counter += 1
                f.write("\n")


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
    if eve == "all_events":
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


if __name__ == '__main__':
    # fileName1, topology_info_list = read_parsed_data('parsed_data/parsed_filenames_combined_data',
    #                                                 'parsed_data/parsed_topology_info_combined_data')

    fileName, networkx_data = read_parsed_data('parsed_data/parsed_filenames_combined_data', 'parsed_data/networkx_data')

    th = TopologyHelper(networkx_data, True, freq=10)    # Create an object of the class to begin

    start_index, end_index, event = get_event_user_input(th)

    get_cliques_data(th, start_index, end_index, fileName, "extracted_data/Cliques/"+event+".csv", 12)
    # get_down_times(th, start_index, end_index, "extracted_data/Down_Time_profile/"+event+".csv")
    # th.flow_topology(start_index, end_index, fileName[start_index:end_index+1], event=event,
    #                  node_name=True)
