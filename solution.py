import pandas as pd
import numpy as np


class MempoolTransaction():
    def __init__(self, txid, fee, weight, parents):
        self.txid = txid
        self.fee = int(fee)
        # TODO: add code to parse weight and parents fields


def parse_mempool_csv(filename):
    """Parse the CSV file and return a list of MempoolTransactions."""
    with open(filename) as f:
        return([MempoolTransaction(*line.strip().split(',')) for line in f.readlines()])


class Transaction():
    def parse_mempool_csv(filename):
        """Parse the CSV file and return a list of MempoolTransactions."""
        with open(filename) as f:
            parsed = [line.strip().split(',') for line in f.readlines()]
            return ([MempoolTransaction(*x) for x in parsed if x[1].isnumeric()])


# Transact =
temp = parse_mempool_csv("mempool.csv")
print(len(temp))
