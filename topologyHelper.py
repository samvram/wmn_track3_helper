# -*- coding: utf-8 -*-
"""
Wireless Mesh Networks - Track III Analysis
-Samvram Sahu
"""
import os
from datetime import datetime
import pandas as pd
import sys
from vpython import *

if sys.version_info[0] < 3:
    from StringIO import StringIO
else:
    from io import StringIO

import math


class topologyHelper:
    """
    A class to help in topology visualization of networks, from files obtained
    using OSLRD data
    """

    def __init__(self, freq):
        self.freq = freq
        self.i = 0
        self.animate = False

    def getFileList(self, directoryName=''):
        """
        input directoryName : The directory from which files are to be displayed.
        output list_of_files : File List in the directory provided.
        """
        directory_path = os.getcwd()
        if directoryName != '':
            directory_path = os.path.join(os.getcwd(), directoryName)
        list_of_files = []
        for file in os.listdir(directory_path):
            file_dict = dict()
            file_dict['file_name'] = file
            file_dict['file_path'] = os.path.join(directory_path, file)
            list_of_files.append(file_dict)
        return list_of_files

    def parseFile(self, file_dict):
        """
        input file_dict : The dictionary type file object, whose list is given by getFileList()
        output topology_info : A dictionary consisting of all tabular data of stuff
        """
        topology_info = dict()
        name = file_dict['file_name']
        topology_info['Time'] = datetime.strptime(name[0:-3], '%Y-%m-%d_%H_%M_%S.%f')
        fread = ''
        with open(file_dict['file_path']) as f:
            fread = f.read()
        tables = fread.split('\n\n')
        for table in tables:
            try:
                tname = table.split('\n')[0].split(': ')[1]
                TableData = StringIO(table[table.index('\n'):-1])
                topology_info[tname] = pd.read_csv(TableData, index_col=False, delimiter='\t')
            except:
                continue
        return topology_info

    def representTopology(self, df, plotSarath=False):
        """
        input df : dataframe containing topology values
        input plotSarath : False(default), provide as True, if you want to plot Sarath Sir
        output topology representation in a tab
        """
        node_loc = {'10': vector(-32, 2 - 9, 0),
                    '11': vector(-28, 2 - 9, 0),
                    '12': vector(-30, -2 - 9, 0),
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
                    '63': vector(0, -2, 12),
                    '90': vector(13, 2 - 4.5, 12),
                    '91': vector(17, 2 - 4.5, 12),
                    '92': vector(15, -2 - 4.5, 12),
                    '110': vector(-32, -2 - 9, 0),
                    '5': vector(15, 0 - 4.5, 3)}

        for node in node_loc.keys():
            if node[-1] == '0':
                sphere(pos=node_loc[node], radius=0.5, color=color.yellow)
            elif node == '5' or node == '110':
                sphere(pos=node_loc[node], radius=0.5, color=color.green)
            else:
                sphere(pos=node_loc[node], radius=0.5, color=color.red)

        cost = dict()
        for node1 in node_loc.keys():
            cost[node1] = dict()
            for node2 in node_loc.keys():
                cost[node1][node2] = 'INFINITE'

        for i in range(0, len(df)):
            node1 = df['Dest. IP'][i].split('.')[-1]
            node2 = df['Last hop IP'][i].split('.')[-1]
            if node1 in node_loc.keys() and node2 in node_loc.keys():
                cost[node1][node2] = df['Cost'][i]

        if plotSarath == False:
            for node in node_loc.keys():
                cost['5'][node] = 'INFINITE'
                cost[node]['5'] = 'INFINITE'

        c = dict()
        for node1 in node_loc.keys():
            c[node1] = dict()
            for node2 in node_loc.keys():
                if cost[node1][node2] != 'INFINITE':
                    c[node1][node2] = curve(pos=[node_loc[node1], node_loc[node2]])
        return 0

    def changeRate(self, evt):
        s = evt.key
        if s == "up":
            self.freq += 10
        elif s == "down":
            self.freq -= 10

        if self.freq <= 0:
            self.freq = 1

        if s == "left":
            self.i -= 1
        elif s == "right":
            self.i += 1

        if self.i <= 0:
            self.i = 0


        if s == ' ':
            self.animate = not self.animate



    def flowTopology(self, list_of_topology, fileName, plotSarath=False):
        """
        Function to simulate the flow of topology in time
        :param list_of_topology: the list of topology tables
        :param plotSarath: parameters to show connections with Sarath Sir
        :param freq: The rate at which simulation runs
        :return:
        """
        scene.bind('keydown', self.changeRate)
        count = 0
        node_loc = {'10': vector(-32, 2 - 9, 0),
                    '11': vector(-28, 2 - 9, 0),
                    '12': vector(-30, -2 - 9, 0),
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
                    '63': vector(0, -2, 12),
                    '90': vector(13, 2 - 4.5, 12),
                    '91': vector(17, 2 - 4.5, 12),
                    '92': vector(15, -2 - 4.5, 12),
                    '110': vector(-32, -2 - 9, 0),
                    '5': vector(15, 0 - 4.5, 3)}

        for node in node_loc.keys():
            if node[-1] == '0':
                sphere(pos=node_loc[node], radius=0.5, color=color.yellow)
            elif node == '5' or node == '110':
                sphere(pos=node_loc[node], radius=0.5, color=color.green)
            else:
                sphere(pos=node_loc[node], radius=0.5, color=color.red)

        print('Starting animation')
        firstTime = True
        self.i = 0
        while True:
            while self.animate:
                self.i %= len(list_of_topology)
                df = list_of_topology[self.i]
                label(pos=vector(0, 0, 0), xoffset=-230, yoffset=190, line=False, box=False, text=fileName[self.i])
                label(pos=vector(0, 0, 0), xoffset=200, yoffset=190, line=False, box=False, text="Rate: "+str(self.freq))

                rate(self.freq)
                cost = dict()
                for node1 in node_loc.keys():
                    cost[node1] = dict()
                    for node2 in node_loc.keys():
                        cost[node1][node2] = 'INFINITE'

                for i in range(0, len(df)):
                    node1 = df['Dest. IP'][i].split('.')[-1]
                    node2 = df['Last hop IP'][i].split('.')[-1]
                    if node1 in node_loc.keys() and node2 in node_loc.keys():
                        cost[node1][node2] = df['Cost'][i]

                if plotSarath == False:
                    for node in node_loc.keys():
                        cost['5'][node] = 'INFINITE'
                        cost[node]['5'] = 'INFINITE'

                if firstTime == True:
                    c = dict()
                    for node1 in node_loc.keys():
                        c[node1] = dict()
                        for node2 in node_loc.keys():
                            if cost[node1][node2] != 'INFINITE' and cost[node1][node2] != 'INFINIT':
                                c[node1][node2] = curve(pos=[node_loc[node1], node_loc[node2]])
                            else:
                                c[node1][node2] = curve(pos=[node_loc[node1], node_loc[node2]])
                                c[node1][node2].visible = False
                    firstTime = False
                else:
                    for node1 in node_loc.keys():
                        for node2 in node_loc.keys():
                            if cost[node1][node2] == 'INFINITE' or cost[node1][node2] == 'INFINIT':
                                c[node1][node2].visible = False
                            else:
                                c[node1][node2].visible = True
                self.i += 1
                if self.i >= len(list_of_topology):
                    firstTime = True
                    self.i = 0

        print('Animation over')
        return 0
