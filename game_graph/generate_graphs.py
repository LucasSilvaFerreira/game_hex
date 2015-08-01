__author__ = 'lucassilva'
# -*- coding: utf-8 -*-                                                                                                                                                   
import sys
import networkx as nx
import random
import matplotlib.pyplot as plt

class GraphCreationError(Exception):pass

class GenerateTable():

    def __init__(self, tabela_dados):
        self.entrada_dados= tabela_dados
        self.main_graph = self.generate_graph_main(file_txt_graph=tabela_dados)

    def generate_main_path(self, size, seed_node, g, cut_off):
        main_nodes = []
        count=0
        while len(main_nodes)!= 6 or count > 10:
            try:
                main_nodes.append(seed_node)
                next_node = seed_node
                #print seed_node
                for x in range(1, size):
                    node_list = [x for x in g[next_node] if g[next_node][x]['pontos'] >= cut_off]
                    for value_repeat in main_nodes:
                        if value_repeat in node_list:
                            #print value_repeat
                            node_list.remove(value_repeat)
                        else:
                            pass

                    random.shuffle(node_list)
                    next_node= node_list[0]
                    main_nodes.append(next_node)
            except:
                main_nodes=[]
                count +=1
        if count > 10:
            raise GraphCreationError("The main paths seems be impossible to construct...")
            system.exit(0)
        else:
            return main_nodes

    def get_random_neighbors(self,node, g, cut_off, count):
        n_neighbors = [x for x in nx.neighbors(g, node) if g[node][x]['pontos'] <= cut_off]
        random.shuffle(n_neighbors)
        return n_neighbors[0:count]

        #[x for x in g[next_node] if g[next_node][x]['pontos'] >= cut_off]

    def get_minimal_pathway(self, g, source, target, steps_cut_off):
        vector_shortest = [s_path for s_path in nx.all_shortest_paths(g, source, target) if len(s_path) == steps_cut_off]
        random.shuffle(vector_shortest)
        try:
            return vector_shortest[0][1]
        except:
            return []

    def get_main_minimal(self, m_path, g):
        end_bag = []
        for main_x in m_path:
            for main_member in m_path:
                return_word = self.get_minimal_pathway(g, main_x, main_member, steps_cut_off=3)
                #print len(return_word)
                if len(return_word) > 0:
                    if return_word not in end_bag:
                        end_bag.append(return_word)
        return end_bag

    def getting_graph_using_list(self, g, list_nodes_names):
        final_list = []
        for nd in list_nodes_names:
            for nd_self in list_nodes_names:
                return_biggest = 0
                if nd != nd_self:
                    #print nd, nd_self
                    try: # try first combination
                        combination_1 = g[nd][nd_self]['pontos']

                        if combination_1:

                            try:
                                combination_2 = g[nd_self][nd]['pontos']

                                if combination_2:
                                    return_biggest = max(combination_1, combination_2)
                            except:
                                #print combination_1
                                return_biggest = combination_1
                    except:
                        try:
                            return_biggest = g[nd_self][nd]['pontos']
                        except:
                            #print 'não existe esse contato'
                            return_biggest = 0

                final_list.append([nd, nd_self, str(return_biggest)])
        return final_list

    def show_graph(self, final_list):
        g_print = nx.Graph()
        #print final_list
        for element in final_list:
            s, t, v = element
            v = int(v)
            if v > 0:
                g_print.add_edge(s, t, {'pontos' : v})


        nx.draw(g_print, node_color='#A0CBE2', node_size = [g_print.degree(x)*300 for x in g_print.nodes()],edge_cmap=plt.cm.Blues, pos=nx.spring_layout(g_print), with_labels=True)
        plt.show()

    def generate_graph_main(self, file_txt_graph):
        '''Main Function'''
        print 'colocar flag para mostrar o unity os nodos do main e agrupa-los primeiro..'

        g = nx.Graph()
        file_g = open(file_txt_graph).read().split('\n')
        file_g = [x.split('\t') for x in file_g]
        for s, t, v in file_g:
            g.add_edge(s, t, {'pontos' : int(v)})
        return g

    def generate_new_game(self, seed_word, show=False, save=None):
        #print self.main_graph[seed_word]
        game_list_nodes = []
        main_path = self.generate_main_path(size=6, seed_node=seed_word, g=self.main_graph, cut_off=5)

        for node in main_path:
            game_list_nodes.append(node)

        neighbors_array = []
        for main_x in main_path:
            #print main_x
            neighbors = self.get_random_neighbors(node=main_x, g=self.main_graph, cut_off=3, count=3)
            for n_element in neighbors:
                neighbors_array.append(n_element)


        #print neighbors_array

        for node_neig in neighbors_array:
            game_list_nodes.append(node_neig)

        for node_neig in self.get_main_minimal(main_path, self.main_graph):
            game_list_nodes.append(node_neig)

        for node_neig in self.get_main_minimal(main_path,self.main_graph):
            game_list_nodes.append(node_neig)
        game_list_nodes =  list(set(game_list_nodes))

        final_list = self.getting_graph_using_list(self.main_graph, game_list_nodes)
        if show:
            self.show_graph(final_list=final_list)
        if save:  #The file name
            save_out = open(save, 'w')
            save_out.write('\n'.join(['\t'.join(info_nodes) for info_nodes in final_list]))
            save_out.close()

def main():
    file_tb = '/home/lucasfsilva/PycharmProjects/trade_ea/game_graph/saida_write_z_maior_que_1.txt'
    table = GenerateTable(file_tb)
    table.generate_new_game('dna', show=True, save='out_games/dna.txt')
    table.generate_new_game('mouse', show=True, save='out_games/mouse.txt')
    table.generate_new_game('beatles', show=True, save='out_games/beatles.txt')
    table.generate_new_game('sex', show=True, save='out_games/sex.txt')

if __name__ == '__main__':
    sys.exit(main())

