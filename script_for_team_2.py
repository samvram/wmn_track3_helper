# -*- coding: utf-8 -*-
from TopologyHelper import TopologyHelper
import pickle as pk
import multiprocessing as mp
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from TCPDumpHelper import TCPDumpHelper


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
    This function reads the pickle parsed data and return the filename file and the extracted data.

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
    :param start: the start index of the analysis
    :param end: the end index of the analysis
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


def get_down_profile(th_object, start, end, filename, node1, node2, path):
    """
    This function is responsible for extracting the link profile between two nodes

    :param th_object: The object of the TopologyHelper class
    :param start: start index of the analysis
    :param end: end index of the analysis
    :param filename: the relevant list of file names.
    :param node1: One of the node of which the link is to be profiled.
    :param node2: One of the node of which the link is to be profiled.
    :param path: The path (including the file name) where the data will be saved as per the CSV format.
    :return:
    """
    res = th_object.get_down_profile(start, end, filename, node1, node2)
    with open(path, 'w') as f:
        f.write("Time,Link goes up(1) or down(0)?\n")
        for k, v in res.items():
            f.write(str(k)+","+str(v)+"\n")


def get_all_down_profile(th_object, start, end, filename, path):
    """
    This function extracts the link profile of various types of link

    :param th_object: The object of the TopologyHelper class
    :param start: start index of the analysis
    :param end: end index of the analysis
    :param file_name: the relevant list of file names.
    :param path: The path of the folder where the various file will be saved
    :return:
    """
    get_down_profile(th_object, start, end, filename, '20', '10', path+"_20_10.csv")
    get_down_profile(th_object, start, end, filename, '20', '30', path+"_20_30.csv")
    get_down_profile(th_object, start, end, filename, '22', '11', path+"_22_11.csv")
    get_down_profile(th_object, start, end, filename, '22', '31', path+"_22_31.csv")
    get_down_profile(th_object, start, end, filename, '22', '10', path+"_22_10.csv")
    get_down_profile(th_object, start, end, filename, '20', '31', path+"_20_31.csv")
    get_down_profile(th_object, start, end, filename, '20', '70', path+"_20_70.csv")
    get_down_profile(th_object, start, end, filename, '20', '90', path+"_20_90.csv")
    get_down_profile(th_object, start, end, filename, '22', '71', path+"_22_71.csv")
    get_down_profile(th_object, start, end, filename, '22', '91', path+"_22_91.csv")
    get_down_profile(th_object, start, end, filename, '22', '70', path+"_22_70.csv")
    get_down_profile(th_object, start, end, filename, '20', '91', path+"_20_91.csv")


def get_planar_data(th_object, start, end, filename, path):
    """
    This function gets the planarity data and stores it to the csv file.

    :param th_object: The object of the TopologyHelper class
    :param start: start index of the analysis
    :param end: end index of the analysis
    :param filename: the relevant list of file names.
    :param path: The path of the file to which the data will be written
    :return:
    """
    res = th_object.get_planarity(start, end, filename)
    with open(path, 'w') as f:
        f.write("Time, Planar(1) or not (0)\n")
        for k, v in res.items():
            f.write(str(k)+","+str(v)+"\n")


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
    """
    This function gets the total number of links existing in the network at every instant of time and save it to a file.

    :param th_object: The object of the TopologyHelper class
    :param start: start index of the analysis
    :param end: end index of the analysis
    :param filename: the relevant list of file names.
    :param path: The path (including the file name) of the csv file where the data will be stored.
    :return:
    """
    ln = th_object.get_link_nums(start, end, filename)
    with open(path, 'w') as f:
        f.write("Time,No_Link \n")
        for k, v in ln.items():
            f.write(str(k.date())+","+str(v)+"\n")


def get_degree_data(th_object, start, end, filename, path, plot_histogram=False, histo_path="untitled.csv",
                    histo_fig_path="untitled.png"):
    """
    This function is responsible for extracting the degree information and storing the data in csv file. It can get the
    histogram data and plot its heat map.

    :param th_object: The object of the TopologyHelper class
    :param start: start index of the analysis
    :param end: end index of the analysis
    :param filename: the relevant list of file names.
    :param path: The path (including the csv file ) where the degree information will be saved.
    :param plot_histogram: If true then the code for extracting the histogram and saving its data to the csv and the
                            heat map to png file
    :param histo_path: The path (including the full file name of CSV) where the histogram data will be saved
    :param histo_fig_path: The path (including the full file name of the PNG file) where the heat map will be saved
    :return:
    """

    ln = th_object.get_degree_data(start, end, filename)
    node_list = list(th_object.topology_graphs[0].nodes())
    with open(path, 'w') as f:
        f.write("Time")
        for k in node_list:
            f.write(","+str(k))
        f.write("\n")
        for k, v in ln.items():
            f.write(str(k))
            for n, d in v:
                f.write(","+str(d))
            f.write("\n")
    if plot_histogram:
        histo_start = 0
        histo_end = 33
        x = np.linspace(histo_start, histo_end, histo_end - histo_start + 1, dtype=int)
        y = np.linspace(1, end-start+1, end-start+1, dtype=int)
        x_meshed, y_meshed = np.meshgrid(x, y)
        z_meshed = np.array([])
        fig = plt.figure()
        ax = fig.add_subplot(111)
        for k, v in ln.items():
            y_tmp = []
            for n, d in v:
                y_tmp.append(d)
            hist, bins = np.histogram(y_tmp, bins=x)
            z_meshed = np.append(z_meshed, np.append(np.array(hist), 0))
        z_meshed = np.reshape(z_meshed, (len(y), len(x)))
        with open(histo_path, 'w') as f:
            f.write("Time")
            for item in x:
                f.write(","+str(item))
            f.write("\n")
            for i in range(start, end + 1):
                f.write(str(filename[i]))
                for item in z_meshed[i-start]:
                    f.write(","+str(item))
                f.write("\n")

        c = ax.pcolormesh(x_meshed, y_meshed, z_meshed, cmap='GnBu_r', vmax=15, vmin=0)
        fig.colorbar(c, ax=ax)
        ax.set_xlabel('Degree size')
        ax.set_ylabel('Time')
        ax.set_title(histo_path)
        fig.savefig(histo_fig_path)
        plt.show()


def get_cliques_data(th_object, start, end, filename, path, num):
    """
    This function is responsible for extracting the cliques information from the start till the end of a particular
    event. It uses multiprocessing to decrease the time spend on the task and collects data from different processes
    and writes it to the csv file.

    :param th_object: The object of the TopologyHelper class
    :param start: start index of the analysis
    :param end: end index of the analysis
    :param filename: the relevant list of file names.
    :param path: The path (including the file name) where the data will be saved as per the CSV format.
    :param num: The number of process the task will be divided into. (It is recommended to not to exceed the value 12)
    :return:
    """
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
    with open(path, 'w') as f:
        f.write("Time")
        for i in range(2, max_clique + 1):
            f.write(","+str(i))
        f.write("\n")
        for cc in cliques_num:
            for k, v in cc.items():
                f.write(str(k.time()))
                counter = 1
                for vv in v:
                    f.write("," + str(vv))
                    counter += 1
                while counter < max_clique:
                    f.write(",0")
                    counter += 1
                f.write("\n")


def get_expression_for_cliques(path, save_fig_path="extracted_data/Cliques/curve_fit.png"):
    """
    This functions reads the data from a csv file which includes the data regarding the average number of cliques vs.
    size of cliques for different scenarios like TCP, Random etc. Every column represents the size of the cliques and
    row represent the situation like TCP, Random etc. It analyzes data for Stationary, Random and Group cases.

    :param path: The path of the CSV file from where the data has to be read
    :param save_fig_path: The path (including the file name) where the PNG file with the curve fit will be saved
    :return:
    """
    with open(path, 'r') as f:
        x = []
        grp = []
        rand = []
        stat = []
        for l in f:
            if "Clique size" in l:
                ind = l.split(',')
                for k in ind[1:]:
                    x.append(float(k))
                print(ind[0], end=":\t")
                print(x)
            if "GROUP_MOBILITY" in l:
                ind = l.split(',')
                for k in ind[1:]:
                    grp.append(float(k))
                print(ind[0], end=":\t")
                print(grp)
            if "RANDOM" in l:
                ind = l.split(',')
                for k in ind[1:]:
                    rand.append(float(k))
                print(ind[0], end=":\t")
                print(rand)
            if "Average Stationary" in l:
                ind = l.split(',')
                for k in ind[1:]:
                    stat.append(float(k))
                print(ind[0], end=":\t")
                print(stat)
        round_off = 6
        z_grp = np.polyfit(x, grp, 8).round(decimals=round_off)
        print("Group", end="\n\t")
        print(z_grp)
        f_grp = np.poly1d(z_grp)

        z_rand = np.polyfit(x, rand, 8).round(decimals=round_off)
        print("Random", end="\n\t")
        print(z_rand)
        f_rand = np.poly1d(z_rand)

        z_stat = np.polyfit(x, stat, 8).round(decimals=round_off)
        print("Stationary", end="\n\t")
        print(z_stat)
        f_stat = np.poly1d(z_stat)

        x_new = np.linspace(2, 14, 50)

        y_new_grp = f_grp(x_new)
        y_new_rand = f_rand(x_new)
        y_new_stat = f_stat(x_new)
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(x, grp, 'o', x_new, y_new_grp)
        ax.plot(x, rand, '+', x_new, y_new_rand)
        ax.plot(x, stat, '*', x_new, y_new_stat)
        ax.set_xlabel('Clique size')
        ax.set_ylabel('Average no. of cliques')
        ax.legend(("Group", "Group curve fit", "Random", "Random curve fit", "Stationary", "Stationary curve fit"))
        fig.savefig(save_fig_path)
        plt.show()


def get_event_user_input(th_object, filename):
    """
    This function is responsible for reading the input from the user and returning the proper values of the start and
    the end index.

    :param th_object: The object of the TopologyHelper class
    :param filename: the relevant list of file names.
    :return: It returns the start and end index along with the event name
    """
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
        end_ind = len(filename) - 1
        return start_ind, end_ind, eve

    for i in range(0, len(filename)):
        if filename[i] >= eve_times[eve]['Start'] and start_ind == -1:
            start_ind = i
        if filename[i] > eve_times[eve]['End'] and end_ind == -1:
            end_ind = i
            break
    return start_ind, end_ind, eve


if __name__ == '__main__':
    tcp_obj = TCPDumpHelper('../tcp_dump/N3_17')
    # tcp_obj.export_signal_strength('10.10.10.80', 'extracted_data/Signal_Strength/src_80.csv')
    # print('Completed')
    # tcp_obj.export_inter_arrival_time('extracted_data/Inter_Arrival_Time/all.csv')

    fileName, networkx_data = read_parsed_data('parsed_data/parsed_filenames_combined_data', 'parsed_data/networkx_data')

    th = TopologyHelper(networkx_data, True, freq=10)    # Create an object of the class to begin

    start_index, end_index, event = get_event_user_input(th, fileName)

    get_planar_data(th, start_index, end_index, fileName, "extracted_data/Planarity/"+event+".csv")

    # get_all_down_profile(th, start_index, end_index, fileName, "extracted_data/Down_Time_profile2/"+event)

    # get_expression_for_cliques("extracted_data/Cliques/combined.csv")
    # get_degree_data(th, start_index, end_index, fileName, "extracted_data/Degree_Distribution/"+event+".csv",
    #                 plot_histogram=True, histo_path="extracted_data/Degree_Distribution/"+event+"_histo.csv",
    #                 histo_fig_path="extracted_data/Degree_Distribution/figs/"+event+"_histo.png")
    #
    # get_cliques_data(th, start_index, end_index, fileName, "extracted_data/Cliques/"+event+".csv", 12)
    # get_down_times(th, start_index, end_index, "extracted_data/Down_Time_profile/"+event+".csv")
    # th.flow_topology(start_index, end_index, fileName[start_index:end_index+1], event=event,
    #                  node_name=True)
