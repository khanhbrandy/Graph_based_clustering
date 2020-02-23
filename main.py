"""
Created on 2019-10-19
Creator: khanh.brandy

"""
import time
import community

if __name__=='__main__':
    path = 'data_test.xlsx'
    source='StockCode'
    target='InvoiceNo'
    edge_attr='Quantity'
    com = community.Community()
    G = com.get_graph(path=path, source=source,  target=target, edge_attr=edge_attr)
    print('Start decomposing graph...')
    start = time.time()
    comps = com.find_optimalQ(G)
    print('Done detecting communities. Time taken = {:.1f}(s) \n'.format(time.time()-start))
    print('Maximum modularity is {}'.format(max(comps.keys())))
