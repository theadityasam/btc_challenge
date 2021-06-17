[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1TNftzAGhL-y4GrBq-aq9tSoILE2I_YpJ?usp=sharing)
# Bitcoin Test

## Problem

Bitcoin miners construct blocks by selecting a set of transactions from their mempool. Each transaction in the mempool:
includes a fee which is collected by the miner if that transaction is included in a block has a weight , which indicates the size of the transaction may have one or more parent transactions which are also in the mempool. The miner selects an ordered list of transactions which have a combined weight below the maximum block weight.
`mempool.csv` is an example mempool of the form `<txid>,<fee>,<weight>,<parent_txids>`

- `txid` is the transaction identifier
- `fee` is the transaction fee
- `weight` is the transaction weight
- `parent_txids` is a list of the txids of the transaction’s unconfirmed parent transactions (confirmed parent transactions are not included in this list). It is of the form: \<txid1\>;\<txid2\>;...

The goal is to read <mark>mempool.csv</mark> and generate a new block of transactions with the following constraints -

- Transactions with parent transactions in the mempool may be included in the list, but only if all of their parents appear before them in the list.
- The miner should ideally include the transactions that maximize the total fee.
- The output from the program should be txids, separated by newlines, which make a valid block.
- Transactions MUST appear in order (no transaction should appear before one of its parents).

## Approach

The task can basically be broken down into 4 stages. Our script file must take in a CSV, operate on it and dump a `.txt` file with valid transaction IDs. My choice of weapon was Python. You might notice that there are three files in the repo. The Jupyter Notebook (solution.ipynb) is my test grounds wherein I test code snippets and validate them for different inputs. Hence, this file can be ignored as it's just a test file.

**The real code resides in [`utils.py`](https://github.com/theadityasam/btc_challenge/blob/main/utils.py) and [`driver.py`](https://github.com/theadityasam/btc_challenge/blob/main/driver.py)**. `utils.py` hosts all the utility functions that I've created such as the file parser, valid transactions selector, optimising function for picking the best possible transactions and the text file writer. These functions are used in the `driver.py` file wherein they're called. The driver code basically performs the following function sequentially -

- **Parsing the CSV** - This step includes reading lines from the given csv and splitting the line by "," (comma) and returning a list of lists. This is as simple as opening a file and running the following

```
[line.strip().split(',') for line in f.readlines()]
```

Every sub-list within the list contains "trans_id, trans_fees, trans_weight, parent_string" in order.

- **Extracting Valid Transactions** - We know that the transactions in the mempool are ordered. The condition is that for a transaction to proceed, the parent transactions should occur before the child. Hence, to make sure this property is adhered, we'll iterate over the list and add transaction ID's to a set, say "parent_set". At every step, we'll check if the set of parents of that transaction is a subset of the "parent_set" that we're keeping a track of. If yes then that transaction is considered as a valid possible mempool transaction.

```
block_ids = []
    block_fee = []
    block_wts = []
    parent_set = set()
    for x in parsed:
        if x[1].isnumeric() and x[2].isnumeric():
            if x[3] == "" or parent_set.issuperset(x[3].split(';')):
                parent_set.add(x[0])
                block_ids.append(x[0])
                block_fee.append(int(x[1]))
                block_wts.append(int(x[2]))
```

This returns 3 lists, one for transactions IDs, one for transaction fees and one for the transaction weights.

- **Getting Optimal Transactions** -

  - Using Dynamic Programming - We have two lists under consideration - fees and weights. Our objective is to **maximise the fees** possible, yet keep the **total block weight under maximum allowed block weight**. This is a classical problem of **0-1 Knapsack**. This method has been implemented in my code with the classical tabulation way, i.e. I created a NumPy table and store the results of the sub-problems in that table. We find the most optimal value for the first **i** elements, where **i** is in range **[0,1,2...,n-1,n]** Hence our final answer is stored in the bottom-rightmost element. Although the implementation is quite easy, it has one major drawback - the time and space complexity i.e. O(N\*W) where N is number of items and W is the maximum possible weight. For the given maximum block size of 4x10<sup>6</sup>, running the algo for **mempool.csv** takes **24-25hours**! (can be seen in the following image, bottom right corner. 8mins, 59secs have elapsed and 25hours, 7mins and 52secs are ;left).
    ![Mempool DP](https://github.com/theadityasam/btc_challenge/blob/main/images/mempool_dp.png)
    The DP algorithm can be optimised for space, there is an O(W) solution as well bringing down the space complexity and the runtimes as well, however this is a minor improvement and won't impact the 24hours runtime much. There are alternative algorithms for calculating the optimal solution like the **Greedy or Genetic algorithms**. However, we then have to make a compromise on the optimality of the solution for the algo runtimes. For now, I'm considering creating the **DP function in C++ and creating Python bindings to call them**. Runtime difference between c++ and Python loops vary between 10x-25x. Even in worst cast, it might be able to bring down the runtime from 24hours to 2.4hours.
  For testing the solution, **I've selected a few transactions** from "mempool.csv" and created a ["trial.csv"](https://github.com/theadityasam/btc_challenge/blob/main/trial.csv) test file. I've selected transactions with many different conditions, transactions with:
  - No parents
  - With single parent that hasn't occured before
  - With single parent that has occured before
  - With multiple parents, some of them haven't occured before
  - With multiple parents, all of them have occured before
  - Transitive parents i.e. parents that have occured before but cannot be included as their parents haven't occured before
    
    For a block size of 4x10<sup>6</sup>
    ![Trial 4e6](https://github.com/theadityasam/btc_challenge/blob/main/images/trail_4e6.png)
    
    For a block size of 6000
    ![Trial 6000](https://github.com/theadityasam/btc_challenge/blob/main/images/trial_6000.png)    
    

- **Dumping to a text file** - This step is a simple, opening the file and writing lines to it. The generated file name is of the form - **"_filename_ current_time_in_UTC"**. If no filename is provided, `"Blocklist"` is considered as default. The generated files can be checked in the repo. You can check the last two "Blocklist..txt" that have been generated for "trial.csv". `[Trial.csv output with BS 6000](https://github.com/theadityasam/btc_challenge/blob/main/Blocklist%202021-06-17%2013:30:30.063371.txt)` `[Trial.csv output with BS 4e6](https://github.com/theadityasam/btc_challenge/blob/main/Blocklist%202021-06-17%2013:29:41.301804.txt)` `[Mempool.csdv output with VS 100,000](https://github.com/theadityasam/btc_challenge/blob/main/block.txt)`

## Caveats

- Assumes all the parent IDs are unique (No two transactions have the same ID)
- The numpy DP method has a time complexity of O(N\*W) and O(N\*W) where N is the total number of items and W is the max weight. This translates to huge runtimes for a max block weight of 4 million. Following was the runtime for

## Improvements I'm Working On

- Wrapping driver in a main function and passing parameters as command line arguments.
- Wrap utilities in class for cleaner codes.
- Write a more optimised version of the DP code with O(W) space complexity.
- Implement genetic algorithm or a greedy algorithm. Although they might not reach global optima, they'll be significantly faster.
