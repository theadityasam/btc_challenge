import utils


class MempoolTransaction():  # Class for holding transaction info
    def __init__(self, txid, fee, weight):
        self.txid = txid
        self.fee = int(fee)
        self.weight = int(weight)

    def __lt__(self, other):
        return (float(self.fee)/float(self.weight)) > (float(other.fee)/float(other.weight))


def main():
    # Code parameters
    filename = "mempool.csv"
    max_block_weight = 4e6

    # Parsing the CSV
    parsed = utils.parse_csv(filename)
    print("-> Parsed - "+filename)

    # Generating valid mempool entries
    block_ids, block_fee, block_wts = utils.create_valid_mempool_list(parsed)
    mempool_list = [MempoolTransaction(
        block_ids[i], block_fee[i], block_wts[i]) for i in range(len(block_ids))]
    print("-> Generated valid mempool list")

    # Generating result
    mempool_list.sort()
    result = []
    weight_sum = 0
    fee_sum = 0
    for transaction in mempool_list:
        if weight_sum + transaction.weight < max_block_weight:
            result.append(transaction.txid)
            weight_sum += transaction.weight
            fee_sum += transaction.fee
        else:
            break

    # Dumping to txt file
    generated_file = utils.dump_to_text(result)
    print("-> Generated block file: "+generated_file)

    # Testing the generated blockfile
    print("-> Testing the generated blockfile")
    utils.test_block(block_ids, block_fee,
                     block_wts, result)


if __name__ == "__main__":
    main()
