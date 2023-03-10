# -*- coding: utf-8 -*-
# @Author  : yz
# @Version : 1.0
# @Time    : 2019/12/16
# import unittest
# from graph.community_detection.corpaoml_al_mp.COPRA_host import COPRA_Host
# from corpaoml_al_mp.COPRA_driver import COPRA_Driver
# from corpaoml_al_mp.COPRA_load_data import COPRA_Load_Data
# from corpaoml_al_mp.COPRA_coordinator import COPRA_Coordinator
from COPRA_driver import COPRA_Driver
from COPRA_load_data import COPRA_Load_Data
from COPRA_coordinator import COPRA_Coordinator
import time
# from collections import defaultdict
import networkx as nx
import onmi
import EQ


class Test():
    def test_intersect(datatype,seed_node,attribute,param,party,file_name,scale,k,mi):
        edge_path = []
        if datatype == 'artificial':
            for i in range(int(party)):   
                edge_path.append('../data/' + datatype + '/' + param + '/' + party + '/network'+ file_name +'_{}.txt'.format(i))
            feat_path = '../data/' + datatype + '/' + param + '/feat/network' + file_name +'_bd_feat.txt'
            # write_path = '../data/' + datatype + '/' + param + '/' + party + '/network' + file_name + '_' + party + '_re.txt'
            write_path = '../data/' + datatype + '/' + param + '/' + party + '/network' + file_name + '_' + party + '_re.txt'
            real_path = '../data/' + datatype + '/' + param + '/' + party + '/community' + file_name +'.txt'
        else:
            # for i in range(int(party)):   
            #     edge_path.append('../data/' + datatype + '/' + party + '/'+ file_name +'_{}.txt'.format(i))
            # feat_path = '../data/' + datatype + '/feat/' + file_name +'.feat'
            # write_path = '../data/' + datatype + '/' + party + '/' + file_name + '_' + party + '_re.txt'
            # real_path = '../data/' + datatype + '/' + party + '/' + file_name +'.circles'
            # graph_path = '../data/' + datatype + '/' + file_name + '.edges'
            for i in range(int(party)):   
                edge_path.append('../data/' + datatype + '/' + party + '/'+ file_name +'_{}.txt'.format(i))

            # ?????????
            # edge_path ??????????????????????????????
            #feat_path ?????????????????????
            #real_path ?????????????????????
            # feat_path = '../data/' + datatype + '/feat/' + file_name +'.txt'
            feat_path = '../data/' + datatype + '/feat/' + file_name +'.feat'
            # write_path = '../data/' + datatype + '/' + party + '/' + file_name + '_' + party + '_re.txt'
            # ????????????????????????
            write_path = '../data/' + datatype + '/' + party + '/' + file_name + '_' + party + '_re.txt'
            # real_path = '../data/' + datatype + '/' + party + '/' + file_name +'_com.txt'
            # ?????????xx.com.txt ??????.circles
            real_path = '../data/' + datatype + '/' + party + '/' + file_name +'.circles'
            # graph_path = '../data/' + datatype + '/' + file_name + '.txt'
            graph_path = '../data/' + datatype + '/' + file_name + '.edges'

        begin_time = time.perf_counter()
        G = []
        nodeset = []
        n = int(party) #party???2|4|8|10 ??????
        Coordinator = COPRA_Coordinator()
        load_data = COPRA_Load_Data()
        for i in range(n):
            G.append(load_data.read_graph_from_file(edge_path[i],seed_node))
            nodeset.append(G[i].nodes()) #nodeset??????????????????????????????????????? e.g. n=2 ???????????????
        sum1=0
        sum2=0
        for small_g in G:
            sum1+=small_g.number_of_edges()
            sum2+=small_g.number_of_nodes()


        if datatype == 'real':

            # ?????????????????????
            Graph = load_data.read_graph_from_file(graph_path,seed_node)
        # Graph = load_data.read_graph_from_file(graph_path, seed_node)
        # print(G[0].nodes(1000))

        # ??????COPRA???????????????????????????

        #??????????????????
        A = load_data.read_attr_from_file(feat_path)
        Driver = COPRA_Driver()
        # 2?????????
        communities= Driver.run(G, A, n, 2, attribute,scale,seed_node,k,mi)
        end_time = time.perf_counter()
        total_time = end_time - begin_time
        
        #????????????
        Coordinator.print_communities_to_file(communities, write_path)

        # ????????????onmi
        onmi_ = onmi.cale_onmi(real_path,write_path)
        if datatype == 'real':
            EQ_ = EQ.cal_EQ(communities,Graph)
            print('eq???',EQ_)
        else:
            EQ_ = 0
            # print('??????????????????EQ')
            # graph_path = '../data/' + datatype + '/' + param +  '/network' + file_name+'.txt'
            # Graph = load_data.read_graph_from_file(graph_path, seed_node)
            # EQ_ = EQ.cal_EQ(communities,Graph)
            # print('eq=',EQ_)
        print('?????????',total_time)
        
        # host = COPRA_Host()
        #     G = nx.read_edgelist("../../corpa/genuine/karate.txt")
        #     com = host.load_data("../../corpa/genuine/copraoml_karate.txt")
        #     mod = host.cal_EQ(com, G)
            # if(mod>=0):
        #     s.append(mod)
        #     print(mod)
        # print("???????????????",s)
        # print("?????????????????????",sum(s) / len(s))
        return total_time,[onmi_,EQ_]


if __name__ == '__main__':
    datatype = 'real'
    seed_node = 'off'
    scale = 0.5
    k = 0.5
    mi = 5
    attribute = 'on'
    # attribute = 'off'
    param = 'n'
    party = '2'
    # party = "4"
    # party = "6"
    # party = "8"
    party = '10'
    # file_name = '1239671'
    # file_name = '2363991'
    # file_name = '5747502'
    file_name = '7682452'
    app=Test
    app.test_intersect(datatype, seed_node, attribute, param, party, file_name ,scale, k ,mi)
    
