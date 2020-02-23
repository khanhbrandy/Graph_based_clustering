Created on 2019-08-20

# Graph Mining
Market basket analysis using graph mining approach over transactional data

# Dataset Information:
Transactional dataset contains all the transactions of a retail company
- InvoiceNo: Invoice number. Nominal, a 6-digit integral number uniquely assigned to each transaction. If this code starts with letter 'c', it indicates a cancellation.

- StockCode: Product (item) code. Nominal, a 5-digit integral number uniquely assigned to each distinct product.

- Quantity: The quantities of each product (item) per transaction. Numeric.

# Graph mining techniques:

The transactional data will be imported then treated as bipartite graph with pre-defined source and target
The bipartite graph (B) then will be trasformed into weighted undirected graph (G) to be analysed using modified Newman Girvan
modularity. 

<p align="center">
  <img src="graph.png">
</p>

Detected communities after n-split would be considered clusters of items (StockCode) then compared with some traditional frequent itemset mining techniques. 
