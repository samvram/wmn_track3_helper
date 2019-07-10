# -*- coding: utf-8 -*-
"""
Wireless Mesh Networks - Track III Analysis
-Samvram Sahu and Ankit Verma
"""
import os
from datetime import datetime
import pandas as pd
from io import StringIO
from vpython import *
import networkx as nx


class TopologyHelper:
    """
    A class to help in topology visualization of networks, from files obtained
    using OSLRD and TCP dump data
    """

    def __init__(self, list_of_topology, is_networkx, freq=10):
        """
        It initializes the TopologyHelper class.

        :param list_of_topology: list of topology or the list of networkx graph
        :param is_networkx: If true then arugment "list of topology" represents lits of networkx graph
        :param freq: The initial frequency of the animation
        """
        self.freq = freq
        self.i = 0
        self.animate = True
        self.time_of_events = dict()
        self.node_loc = {'10': vector(-32, 2 - 9, 0),
                         '11': vector(-28, 2 - 9, 0),
                         '12': vector(-35, -2 - 9, 0),
                         '20': vector(-22, 2 - 6, 0),
                         '21': vector(-18, 2 - 6, 0),
                         '22': vector(-20, -2 - 6, 0),
                         '40': vector(-12, 2 - 3, 0),
                         '41': vector(-8, 2 - 3, 0),
                         '42': vector(-10, -2 - 3, 0),
                         '50': vector(-2, 2, 0),
                         '51': vector(2, 2, 0),
                         '52': vector(0, -2, 0),
                         '54': vector(-3, -2, 0),
                         '70': vector(8, 2 - 3, 0),
                         '71': vector(12, 2 - 3, 0),
                         '72': vector(10, -2 - 3, 0),
                         '80': vector(18, 2 - 6, 0),
                         '81': vector(22, 2 - 6, 0),
                         '82': vector(20, -2 - 6, 0),
                         '100': vector(28, 2 - 9, 0),
                         '101': vector(32, 2 - 9, 0),
                         '102': vector(30, -2 - 9, 0),
                         '30': vector(-17, 2 - 4.5, 12),
                         '31': vector(-13, 2 - 4.5, 12),
                         '32': vector(-15, -2 - 4.5, 12),
                         '60': vector(-2, 2, 12),
                         '61': vector(2, 2, 12),
                         '62': vector(4, 2, 12),
                         '63': vector(0, -2, 12),
                         '90': vector(13, 2 - 4.5, 12),
                         '91': vector(17, 2 - 4.5, 12),
                         '92': vector(15, -2 - 4.5, 12),
                         '110': vector(-32, -2 - 9, 0),
                         '5': vector(15, 0 - 4.5, 3)}

        if is_networkx:
            # The passed data to the list_of_topolgy is list of networkx graphs
            self.topology_graphs = list_of_topology
        else:
            gh_temp = nx.Graph()

            gh_temp.add_nodes_from(list(self.node_loc.keys()))

            cost = dict()
            for node1 in self.node_loc.keys():
                cost[node1] = dict()
                for node2 in self.node_loc.keys():
                    cost[node1][node2] = 'INFINITE'

            self.topology_graphs = []
            for k in range(0, len(list_of_topology)):
                self.topology_graphs.append(gh_temp.copy())

                df = list_of_topology[k]

                for j in range(0, len(df)):
                    node1 = df['Dest. IP'][j].split('.')[-1]
                    node2 = df['Last hop IP'][j].split('.')[-1]
                    if node1 in self.node_loc.keys() and node2 in self.node_loc.keys():
                        cost[node1][node2] = df['Cost'][j]

                for node1 in self.node_loc.keys():
                    for node2 in self.node_loc.keys():
                        try:
                            self.topology_graphs[k].add_edge(node2, node1, cost=(float(cost[node1][node2]) +
                                                                                 float(cost[node2][node1]))/2)
                        except ValueError:
                            continue
                        finally:
                            cost[node1][node2] = 'INFINITE'
                            cost[node2][node1] = 'INFINITE'

        scene.bind('keydown', self.change_rate)
        scene.background = color.white
        scene.width = 1900
        scene.height = 950

        self.laptop_color = color.yellow
        self.router_color = color.red
        self.unique_color = color.green
        self.time_of_events['TCP'] = dict()
        self.time_of_events['TCP']['Start'] = datetime(2018, 10, 13, 13, 2)
        self.time_of_events['TCP']['End'] = datetime(2018, 10, 13, 14, 00)

        self.time_of_events['RAIN'] = dict()
        self.time_of_events['RAIN']['Start'] = datetime(2018, 10, 13, 14, 00)
        self.time_of_events['RAIN']['End'] = datetime(2018, 10, 13, 14, 56)

        self.time_of_events['UDP'] = dict()
        self.time_of_events['UDP']['Start'] = datetime(2018, 10, 13, 14, 56)
        self.time_of_events['UDP']['End'] = datetime(2018, 10, 13, 15, 23)

        self.time_of_events['PING'] = dict()
        self.time_of_events['PING']['Start'] = datetime(2018, 10, 13, 15, 23)
        self.time_of_events['PING']['End'] = datetime(2018, 10, 13, 15, 40)

        self.time_of_events['VoIP'] = dict()
        self.time_of_events['VoIP']['Start'] = datetime(2018, 10, 13, 15, 40)
        self.time_of_events['VoIP']['End'] = datetime(2018, 10, 13, 16, 21)

        self.time_of_events['FTP'] = dict()
        self.time_of_events['FTP']['Start'] = datetime(2018, 10, 13, 16, 21)
        self.time_of_events['FTP']['End'] = datetime(2018, 10, 13, 17, 12)

        self.time_of_events['GROUP_MOBILITY'] = dict()
        self.time_of_events['GROUP_MOBILITY']['Start'] = datetime(2018, 10, 13, 17, 12)
        self.time_of_events['GROUP_MOBILITY']['End'] = datetime(2018, 10, 13, 17, 52)  # datetime(2018, 10, 17, 52, 20)

        self.time_of_events['RANDOM'] = dict()
        self.time_of_events['RANDOM']['Start'] = datetime(2018, 10, 13, 17, 52)
        self.time_of_events['RANDOM']['End'] = datetime(2018, 10, 13, 18, 5)

        self.time_of_events["all_events"] = dict()
        self.time_of_events["all_events"]['Start'] = datetime(2018, 10, 13, 13, 2)
        self.time_of_events["all_events"]['End'] = datetime(2018, 10, 13, 18, 5)

        self.time_of_events["stationary"] = dict()
        self.time_of_events["stationary"]['Start'] = datetime(2018, 10, 13, 13, 2)
        self.time_of_events["stationary"]['End'] = datetime(2018, 10, 13, 17, 12)

    def get_events(self):
        """
        Function that provides time of each experiment.
        :return:  Dictionary of events ewith time
        """
        return self.time_of_events

    @staticmethod
    def get_file_list(directory_name=''):
        """
        This function gets the list of files present in the directory passed as argument

        :param directory_name: The directory from which files are to be displayed.
        :return: File List in the directory provided.
        """
        directory_path = os.getcwd()
        if directory_name != '':
            directory_path = os.path.join(os.getcwd(), directory_name)
        list_of_files = []
        for file in os.listdir(directory_path):
            file_dict = dict()
            file_dict['file_name'] = file
            file_dict['file_path'] = os.path.join(directory_path, file)
            list_of_files.append(file_dict)
        return list_of_files

    @staticmethod
    def parse_file(file_dict):
        """
        This function parses all the files passed as dictionary and retuns the parsed data.

        :param file_dict: The dictionary type file object, whose list is given by getFileList()
        :return: A dictionary consisting of all tabular data of OLSRD file
        """
        topology_info = dict()
        name = file_dict['file_name']
        k = datetime.strptime(name[0:-3], '%Y-%m-%d_%H_%M_%S.%f')
        with open(file_dict['file_path']) as f:
            f_read = f.read()
        tables = f_read.split('\n\n')
        for table in tables:
            try:
                t_name = table.split('\n')[0].split(': ')[1]
                table_data = StringIO(table[table.index('\n'):-1])
                topology_info[t_name] = pd.read_csv(table_data, index_col=False, delimiter='\t')
            except:
                continue
        return [topology_info, k]

    def change_rate(self, evt):
        """
        This function is for handling the events like key pressed etc.

        :param evt: the event happened
        :return: Doesn't return any value
        """

        key_event = evt.key
        if key_event == "up":
            self.freq += 10
        elif key_event == "down":
            self.freq -= 10

        if self.freq <= 0:
            self.freq = 1

        if key_event == "left":
            self.i -= 1
        elif key_event == "right":
            self.i += 1

        if self.i <= 0:
            self.i = 0

        if key_event == ' ':
            self.animate = not self.animate

    def get_node_len_etx(self, list_of_topology, start, end):
        """
        This function is used to get the total number of hop count and the ETX between start and the end node by using
        dijkstra's algorithm.

        :param list_of_topology: a list containing the topology information.
        :param start: A string containing the last octate of the IP address of the starting node
        :param end: A string containing the last octate of the IP address of the destination or end node
        :return: It returns a list of dictionary. Each dictionary corresponds to the topology list with hop count and
        net etx as its element
        """
        route_data = dict()
        self.i = 0
        while self.i < len(list_of_topology):
            df = list_of_topology[self.i]
            cost = dict()
            for node1 in self.node_loc.keys():
                cost[node1] = dict()
                for node2 in self.node_loc.keys():
                    cost[node1][node2] = 100000000
            for j in range(0, len(df)):
                node1 = df['Dest. IP'][j].split('.')[-1]
                node2 = df['Last hop IP'][j].split('.')[-1]
                if node1 in self.node_loc.keys() and node2 in self.node_loc.keys():
                    if df['Cost'][j] == 'INFINITE' or df['Cost'][j] == 'INFINIT':
                        cost[node1][node2] = 100000000
                    else:
                        cost[node1][node2] = float(df['Cost'][j])
            # cost = dict() # data for testing the algorithm
            # for i in range(0, 9):
            #     cost[i] = dict()
            #     for j in range(0, 9):
            #         cost[i][j] = 1000000000
            #
            # cost[0][1] = 4
            # cost[0][7] = 8
            # cost[1][2] = 8
            # cost[1][7] = 11
            # cost[1][0] = 4
            # cost[7][0] = 8
            # cost[7][1] = 11
            # cost[7][6] = 1
            # cost[7][8] = 7
            # cost[2][8] = 2
            # cost[2][3] = 7
            # cost[2][5] = 4
            # cost[2][1] = 8
            # cost[8][7] = 7
            # cost[8][6] = 6
            # cost[8][2] = 2
            # cost[6][7] = 1
            # cost[6][5] = 2
            # cost[6][8] = 6
            # cost[5][2] = 4
            # cost[5][6] = 2
            # cost[5][3] = 14
            # cost[3][2] = 7
            # cost[3][5] = 14
            #
            # self.node_loc = dict.fromkeys(list(range(0, 9)), 0)
            # run dijkstra's algorithm
            visited_done = []
            remaining_node = list(self.node_loc.keys())
            node_length = dict.fromkeys(list(self.node_loc.keys()), 100000000)

            node_length[start] = 0

            remaining_node.remove(start)
            visited_done.append(start)
            curr_min_ver = start

            prev_point = dict.fromkeys(list(self.node_loc.keys()))
            prev_point[start] = start

            for k in node_length.keys():
                if (k not in visited_done) and (cost[curr_min_ver][k] is not 100000000):
                    new_dist = node_length[curr_min_ver] + cost[curr_min_ver][k]
                    if node_length[k] > new_dist:
                        node_length[k] = new_dist
                        prev_point[k] = curr_min_ver

            while visited_done != list(self.node_loc.keys()):
                min_val = 100000000
                min_node = -1
                for i in node_length.keys():
                    if node_length[i] < min_val and i not in visited_done:
                        min_node = i
                        min_val = node_length[i]
                curr_min_ver = min_node
                if curr_min_ver != -1:
                    remaining_node.remove(curr_min_ver)
                    visited_done.append(curr_min_ver)

                    for k in node_length.keys():
                        if (k not in visited_done) and (cost[curr_min_ver][k] is not 100000000):
                            new_dist = node_length[curr_min_ver] + cost[curr_min_ver][k]
                            if node_length[k] > new_dist:
                                node_length[k] = new_dist
                                prev_point[k] = curr_min_ver
                else:
                    break

            route_data[self.i] = dict()
            if prev_point[end] is None:
                route_data[self.i]['hopes_count'] = -1
                route_data[self.i]['cost'] = -1
            else:
                curr = end
                hopes = 0
                while True:
                    curr = prev_point[curr]
                    hopes += 1
                    if curr == start:
                        break
                route_data[self.i]['hopes_count'] = hopes
                route_data[self.i]['cost'] = node_length[end]

            self.i += 1
        return route_data

    def get_down_time(self, start, end):
        """
        This function gets the link down time of ALL the links in the list_of_topology topology data.

        :param start: start index of the analysis
        :param end: end index of the analysis
        :return: it returns a dictionary. The dictionary is two dimension, each dimension is a node. Hence the
        dictionary essentially denote all the possible links. The value of each key is the number of seconds the link
        was down.
        """
        cost = dict()
        for node1 in self.node_loc.keys():
            cost[node1] = dict()
            for node2 in self.node_loc.keys():
                cost[node1][node2] = 'INFINITE'

        c = dict()
        nodes = list(self.node_loc.keys())
        for i in range(0, len(nodes)):
            node1 = nodes[i]
            c[node1] = dict()
            for j in range(i, len(nodes)):
                node2 = nodes[j]
                c[node1][node2] = end - start + 1

        for gh in self.topology_graphs[start:end + 1]:
            for i in range(0, len(nodes)):
                node1 = nodes[i]
                for j in range(i, len(nodes)):
                    node2 = nodes[j]
                    if (node1, node2) in gh.edges or (node2, node1) in gh.edges:
                        c[node1][node2] -= 1
        return c

    def get_link_avg_cost(self, start, end, file_name):
        """
        This functions gets the average cost of links in the network at different instants of time.

        :param start: start index of the analysis
        :param end: end index of the analysis
        :param file_name: a list of file names corresponding to the list of topology
        :return: It returns a dictionary with keys as the list of files passed as file_name. The value of each key
        denotes average cost of the links in the network at the instant of time represented by the key.
        """
        self.i = 0
        cost = dict()
        links_num = dict.fromkeys(file_name, 0.0)
        for node1 in self.node_loc.keys():
            cost[node1] = dict()
            for node2 in self.node_loc.keys():
                cost[node1][node2] = 'INFINITE'
        i = start
        nodes = list(self.node_loc.keys())
        while i < end + 1:
            fn = file_name[i]
            gh = self.topology_graphs[i]
            counter = 0
            for k in range(0, len(nodes)):
                node1 = nodes[k]
                for j in range(k, len(nodes)):
                    node2 = nodes[j]
                    if (node1, node2) in gh.edges or (node2, node1) in gh.edges:
                        counter += float(gh.get_edge_data(node1, node2)['cost'])
                        links_num[fn] += 1

            if links_num[fn] != 0:
                links_num[fn] = counter / links_num[fn]
            else:
                links_num[fn] = -1
            i += 1
        return links_num

    def get_degree_data(self, start, end, file_name):
        """
        This function is gives the degree of each node at every instant of time from the start till the end (end point
        included)

        :param start: start index of the analysis
        :param end: end index of the analysis
        :param file_name: a list of file names corresponding to the list of topology
        :return: It returns the a dictionary containing the degree data. The keys of the dictionary are the file name
        from the 'file_name' and value is the return value of the degree of the graph.
        """
        i = start
        res = dict()
        print('Getting Degree distribution from ', start, ' till ', end)
        while i < end + 1:
            gh = self.topology_graphs[i]
            res[str(file_name[i])] = gh.degree
            i += 1
        return res

    def get_cliques_data(self, start, end, file_name, cliques_num, max_cliques):

        i = start

        print('Getting cliques from ', start, ' till ', end)
        while i < end + 1:

            fn = file_name[i]

            gh = self.topology_graphs[i]

            tmp_list = [0, 0]
            for cq in nx.enumerate_all_cliques(gh):
                length = len(cq)

                if length > max_cliques.value:
                    max_cliques.value = length
                if length > 1:
                    try:
                        tmp_list[length] += 1
                    except IndexError:
                        tmp_list.append(1)
            cliques_num[fn] = tmp_list[2:]
            i += 1
        print("\tDone from ", start, " till ", end)
        print("\tSize of cliques_num ", len(cliques_num))
        print("\tMax size of cliques", max_cliques.value)
        # return cliques_num, max_cliques[0]

    def get_node_links_num(self, start, end, file_name, node1, node2):
        """
        This function is use to find the etx between two nodes with respect to time.

        :param start: start index of the analysis
        :param end: end index of the analysis
        :param file_name: a list of file names corresponding to the list of topology
        :param node1: The node 1 whose link cost has to be obtained with node 2
        :param node2: The node 2 whose link cost has to be obtained with node 1
        :return: It returns the list of cost of the link between the two nodes passed as the argument nodes.
        """

        links_num = dict.fromkeys(file_name, 0)
        i = start
        while i < end+1:
            gh = self.topology_graphs[i]
            fn = file_name[self.i]
            links_num[fn] = gh.get_edge_data(node1, node2, default=-1)['cost']  # to be checked
            i += 1
        return links_num

    def get_link_nums(self, start, end, file_name):
        """
        This function is use to get the total number of links existing in the network at different instant of time.

        :param start: The starting index of the topology graph
        :param end: The last index of the topology graph
        :param file_name: a list of file names corresponding to the list of topology
        :return: It returns a dictionary with keys as as the file_name and the values denoting the total number of links
        existing in the network at that instant of time.
        """
        self.i = 0
        links_num = dict.fromkeys(file_name, 0)

        for i in range(0, len(self.topology_graphs[start:end+1])):
            links_num[file_name[i]] = self.topology_graphs[i].number_of_edges()

        return links_num

    def draw_nodes(self):
        """
        This function only draws the layout of the experimental setup. It also draws the plane of different floors
        of the D3 building. This doesn't start any animation.
        :return: It doesn't return any value
        """
        for node in self.node_loc.keys():
            if node[-1] == '0':
                sphere(pos=self.node_loc[node], radius=0.5, color=self.router_color)
            elif node == '5':
                sphere(pos=self.node_loc[node], radius=0.5, color=self.unique_color)
            else:
                sphere(pos=self.node_loc[node], radius=0.5, color=self.laptop_color)
            label(pos=self.node_loc[node], xoffset=10, yoffset=10, line=True, box=False,
                  text=str(node), height=36, opacity=0)
        box(pos=vector(0, -5, -1), size=vector(80, 20, 0.01), color=color.gray(0.99))
        box(pos=vector(0, -1, 11), size=vector(40, 10, 0.01), color=color.gray(0.99))

    def represent_topology(self, index, f_name, plot_sarath=False):
        """
        This function is draws the topology along with all the links present in the dataframe of the topology passed.

        :param index: Index of the topology to display
        :param f_name: the name of the file of which the dataframe is.
        :param plot_sarath: If true then it plots the links between sarath's node to other node
        :return: It always returns the value 0
        """

        label(pos=vector(0, 0, 0), xoffset=-230, yoffset=190, line=False, box=False, text=f_name)
        label(pos=vector(0, 0, 0), xoffset=200, yoffset=190, line=False, box=False,
              text="Rate: " + str(self.freq))

        for node in self.node_loc.keys():
            if node[-1] == '0':
                sphere(pos=self.node_loc[node], radius=0.5, color=self.router_color)
            elif node == '5':
                sphere(pos=self.node_loc[node], radius=0.5, color=self.unique_color)
            else:
                sphere(pos=self.node_loc[node], radius=0.5, color=self.laptop_color)
            label(pos=self.node_loc[node], xoffset=10, yoffset=0, line=False, box=False,
                  text=str(node), height=18)
        c = dict()
        gh = self.topology_graphs[index]
        for node1 in self.node_loc.keys():
            c[node1] = dict()
            for node2 in self.node_loc.keys():
                if (node1, node2) in gh.edges:
                    c[node1][node2] = curve(pos=[self.node_loc[node1], self.node_loc[node2]], radius=0.03)
                    if not plot_sarath:
                        if node1 == '5' or node2 == '5':
                            c[node1][node2].visible = False
        return 0

    def flow_topology(self, start, end, file_name, event="all_events", plot_sarath=False, node_name=False,
                      node_to_show='ALL'):
        """
        Function to simulate the flow of topology in time.

        :param start: a starting index value of the animation
        :param end: a last index value of the animation
        :param file_name: a list of file names corresponding to the list of topology
        :param event: The name of the event being animated like rain, tcp, group mobility, etc.
        :param plot_sarath: parameters to show connections with Sarath Sir
        :param node_name: If true then the names of the nodes are shown
        :param node_to_show: The list of nodes to show.
        :return: Doesn't return any value
        """
        if node_to_show == 'ALL':
            node_to_show = self.node_loc.keys()

        for node in self.node_loc.keys():
            if node[-1] == '0':
                if node in node_to_show:
                    sphere(pos=self.node_loc[node], radius=0.6, color=self.router_color)
                else:
                    sphere(pos=self.node_loc[node], radius=0.1, color=self.router_color)
            elif node == '5':
                sphere(pos=self.node_loc[node], radius=0.1, color=self.unique_color)
            elif node in node_to_show:
                sphere(pos=self.node_loc[node], radius=0.6, color=self.laptop_color)
            else:
                sphere(pos=self.node_loc[node], radius=0.1, color=self.laptop_color)
        print('Starting animation')
        self.i = 0
        time_label = label(pos=vector(0, 0, 0), xoffset=-230, yoffset=190, line=False, box=False, opactiy=0,
                           text=str(file_name[self.i])[11:-5])
        rate_label = label(pos=vector(0, 0, 0), xoffset=200, yoffset=190, line=False, box=False, opactiy=0,
                           text="Rate: " + str(self.freq))
        if event != "all_events":
            label(pos=vector(0, 0, 0), xoffset=0, yoffset=160, line=False, box=True,
                  text=event)
        c = dict()
        cost = dict()
        for node1 in self.node_loc.keys():
            cost[node1] = dict()
            c[node1] = dict()
            if node_name:
                label(pos=self.node_loc[node1], xoffset=0.5, yoffset=0.5, line=True, box=False, opactiy=0,
                      text=node1)
            for node2 in self.node_loc.keys():
                cost[node1][node2] = 'INFINITE'
                c[node1][node2] = curve(pos=[self.node_loc[node1], self.node_loc[node2]])
                c[node1][node2].visible = False

        while True:
            while self.animate:
                for gh in self.topology_graphs[start:end+1]:
                    if not self.animate:
                        continue
                    for node1 in self.node_loc.keys():
                        if not plot_sarath:
                            cost['5'][node1] = 'INFINITE'
                            cost[node1]['5'] = 'INFINITE'
                        for node2 in self.node_loc.keys():
                            if node1 in node_to_show and node2 in node_to_show:
                                if (node1, node2) in gh.edges:
                                    c[node1][node2].visible = True
                                else:
                                    c[node1][node2].visible = False
                                if not plot_sarath:
                                    if node1 == '5' or node2 == '5':
                                        c[node1][node2].visible = False
                            else:
                                c[node1][node2].visible = False
                    time_label.text = str(file_name[self.i])
                    rate_label.text = "Rate: " + str(self.freq)
                    rate(self.freq)
                    self.i += 1
                    self.i %= (end - start + 1)
