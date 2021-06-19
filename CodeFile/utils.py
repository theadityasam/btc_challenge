import numpy as np
from datetime import datetime
from tqdm.auto import tqdm
from numba import jit

# Parse the CSV file and return a list of MempoolTransactions.


def parse_csv(filename):
    with open(filename) as f:
        return [line.strip().split(',') for line in f.readlines()]


# Create a valid mempool list with valid parent conditon
def create_valid_mempool_list(parsed):
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
    return (block_ids, block_fee, block_wts)


# Validate inputs that are being sent to the optimization function
def check_inputs(values, weights, n_items, capacity):
    # check variable type
    assert(isinstance(values, list))
    assert(isinstance(weights, list))
    assert(isinstance(n_items, int))
    assert(isinstance(capacity, int))
    # check value type
    assert(all(isinstance(val, int) or isinstance(val, float)
           for val in values))
    assert(all(isinstance(val, int) for val in weights))
    # check validity of value
    assert(all(val >= 0 for val in weights))
    assert(n_items > 0)
    assert(capacity > 0)


# def dp_loop(table, keep, values, weights, n_items, capacity):


# @jit(nopython=True)
# Use Dynamic Programming to get the optimal block combination
def get_optimal_blocks_dp(values, weights, n_items, capacity=4000000, return_all=False):
    # check_inputs(values, weights, n_items, capacity)
    print("Input number of transactions: "+str(n_items))
    print("Max Block Size: "+str(capacity))
    table = np.zeros((n_items+1, capacity+1), dtype=np.float32)
    keep = np.zeros((n_items+1, capacity+1), dtype=np.float32)
    # loop = tqdm(total=n_items, position=0, leave=False)  # For the progress bar
    print("Progress...")
    for i in range(1, n_items+1):
        # Display progress in progress bar
        # loop.set_description("Progress...".format(i))
        for w in range(0, capacity+1):
            wi = weights[i-1]  # weight of current item
            vi = values[i-1]  # value of current item
            if (wi <= w) and (vi + table[i-1, w-wi] > table[i-1, w]):
                table[i, w] = vi + table[i-1, w-wi]
                keep[i, w] = 1
            else:
                table[i, w] = table[i-1, w]
        # loop.update(1)
        prog = i/n_items*100
        # threshold = 90
        # if(prog > threshold):
        print(prog)
        #     threshold += 5
    picks = []
    K = capacity
    for i in range(n_items, 0, -1):
        if keep[i, K] == 1:
            picks.append(i)
            K -= weights[i-1]
    picks.sort()
    picks = [x-1 for x in picks]  # change to 0-index
    # if return_all:
    #     max_val = table[n_items, capacity]
    #     return (picks, max_val)
    print("\nNumber of transactions selected: "+str(len(picks)))
    return picks


# Takes in a list and dumps to a text file
def dump_to_text(result, name="Blocklist "):
    filename = name+str(datetime.utcnow())+".txt"
    textfile = open('GeneratedBlocks/'+filename, "w")
    for element in result:
        textfile.write(element + "\n")
    textfile.close()
    return filename

# Testing the result


def test_block(mempool_list, values, weights, block_entries):
    value_list = dict(zip(mempool_list, values))
    weight_list = dict(zip(mempool_list, weights))
    sum = 0
    wts = 0
    for i in block_entries:
        sum += value_list[i]
        wts += weight_list[i]
    print("Elements in the block: "+str(len(block_entries)))
    print("Total sum of the elements: "+str(sum))
    print("Total weight of the elements: "+str(wts))
