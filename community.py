"""
Created on 2019-10-19
Creator: khanh.brandy

"""
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
from networkx.algorithms.community.centrality import girvan_newman
from networkx.algorithms import bipartite
import time


class Community():
    def __init__(self):
        pass 
    def get_graph(self, path, source,  target, edge_attr):
        '''
        The transactional data will be imported then treated as bipartite graph with pre-defined source and target
        The bipartite graph (B) then will be trasformed into weighted undirected graph (G) to be analysed 
        '''
        # Import initial network
        data = pd.read_excel(path)
        data = data.head(100) # For testing purpose, shall be commented
        # Transform into bipartite graph
        B = nx.from_pandas_edgelist(data, source=source,  target=target, edge_attr=edge_attr)
        # Check bipartite (if needed)
        if bipartite.is_bipartite(B):
            print('This is a connected network')
        else:
            print('This is NOT a connected network')
        # Generate projected graph G
        I = set(data['StockCode'])
        G = bipartite.weighted_projected_graph(B,I)
        # Number of nodes
        self.number_edges = len(G.edges())
        # Adjacency matrix
        self.adj_matrix = nx.adj_matrix(G)
        return G

    def plot_graph(self, G):
        # Draw the projected graph using the random layout
        plt.figure(figsize=(10,9))
        pos = nx.random_layout(G)
        nx.draw_networkx(G, pos, with_labels=False, node_size=30, font_size=5, node_color='red')
    
    def update_degree(self, adj_matrix, node_list):
        '''
        Update node degree after each iteration:
        adj_matrix is the new adj_matrix of G - nx.adj_matrix(G)
        node_list array contains nodes of G that will be updated - G.nodes()
        
        '''
        deg_dict = {}
        # n = adj_matrix.shape[0]
        new_deg = adj_matrix.sum(axis = 1)
        i = 0
        for idx in list(node_list):
            deg_dict[idx] = new_deg[i, 0]
            i += 1
        return deg_dict

    def get_modularity(self, G, o_deg_dict, m):
        '''
        Calculate modularity Q of the decomposed graph G:
        variables with "o_" prefix represents "original_"
        variables with "n_" prefix represents "new_"
        e_ii: the fraction of edges in the network that connect vertices in the same community 
        a_i: the fraction of edges that connect TO vertices in community i
        (Newman and Girvan, 2004)
        
        '''
        n_adj_matrix = nx.adj_matrix(G)
        n_deg_dict = self.update_degree(n_adj_matrix, G.nodes())
        # Compute modularity Q:
        print('Number of communities after split: {}'.format(nx.number_connected_components(G)))
        comp_list = nx.connected_components(G)
        Q = 0
        for comp in comp_list:
            e_ii = 0
            a_i = 0
            for node in comp:
                e_ii += n_deg_dict[node]
                a_i += o_deg_dict[node]
            Q += (float(e_ii)/(2*m) - float(a_i*a_i)/(4*m*m) )
        print('Modularity of this decomposed graph G: {}'.format(Q))
        return Q

    def find_edge(self,G):
        '''
        Finding node having the largest edge betweeness after each iteration (partition)
        '''
        edge_values = nx.edge_betweenness_centrality(G)
        edge_to_remove = sorted(edge_values.items(), key = lambda x: x[1], reverse = True)
        return edge_to_remove[0][0]

    def newman_girvan(self,G):
        '''
        Divisive community detection process
        '''
        # Number of edges in original graph G:
        m = self.number_edges
        # Original adj_matrix of graph G:
        o_adj_matrix = self.adj_matrix
        o_deg_dict = self.update_degree(o_adj_matrix, G.nodes())
        # Remove edge with highest edge betweeeness
        init_comp = nx.connected_component_subgraphs(G)
        init_ncomp = nx.number_connected_components(G)
        print('Init: {} connected components'.format(init_ncomp))
        ncomp = init_ncomp
        while ncomp <= init_ncomp:
            G.remove_edge(*self.find_edge(G))
            comp = nx.connected_component_subgraphs(G)
            ncomp = nx.number_connected_components(G)
        print('End: {} connected components'.format(ncomp))
        Q = self.get_modularity(G, o_deg_dict, m)
        subgraphs = list(nx.connected_component_subgraphs(G))
        print('*'*30)
        return subgraphs, Q


    def find_optimalQ(self,G):
        G_clone = G.copy()
        comps = {}
        while True:
            subgraphs, Q = self.newman_girvan(G_clone)
            comps[Q] = subgraphs
            if G_clone.number_of_edges() ==0:
                print('No more edge to remove. End splitting!')
                print('*'*30)
                break
        return comps