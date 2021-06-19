"""WIP"""

import utils
import Genetic
# filename = "mempool.csv"
# parsed = util.parse_csv(filename)
# print("-> Parsed - "+filename)
# block_ids, block_fee, block_wts = util.create_valid_mempool_list(parsed)
# print("-> Generated valid mempool list")
# print("-> Getting optimal transaction selection")
# optimal_block_list = util.get_optimal_blocks_dp(
#     block_fee, block_wts, len(block_ids), 6000)
# result = [block_ids[i] for i in optimal_block_list]
# generated_file = util.dump_to_text(result)
# print("-> Generated block file: "+generated_file)


class Solution:
    def __init__(self):
        self.block_ids = []
        self.block_fee = []
        self.block_wts = []
        self.maxCapacity = 0
        self.n_items = 0
        self.algo = 0

    def get_result(self):
        print("Input number of transactions: "+str(self.n_items))
        print("Max Block Size: "+str(self.maxCapacity))

        if self.algo == 0:
            print("Greedy Algorithm")

        if self.algo == 1:
            print("Starting Genetic Algorithm")
            genetic = Genetic.Genetic()
            fit_result = genetic.fit(
                self.block_ids, self.block_fee, self.block_wts, self.maxCapacity)
            picks = []
            for i in range(len(fit_result)):
                if fit_result[i] == 0:
                    picks.append(i)
            return picks

        elif self.algo == 2:
            return
        else:
            return []

    def run(self, filename, maxCap=4000000, algo=0):
        self.maxCapacity = maxCap
        self.algo = algo

        parsed = utils.parse_csv(filename)
        print("-> Parsed - "+filename)

        self.block_ids, self.block_fee, self.block_wts = utils.create_valid_mempool_list(
            parsed)
        print("-> Generated valid mempool list")

        if len(self.block_ids) == len(self.block_fee) and len(self.block_fee) == len(self.block_wts):
            self.n_items = len(self.block_ids)
        # check_inputs(self.block_fee, self.block_wts, self.n_items, self.maxCapacity)

        print("-> Getting optimal transaction block")
        optimal_block_list = self.get_result()

        result = [self.block_ids[i] for i in optimal_block_list]

        generated_file = utils.dump_to_text(result)
        print("-> Generated block file: "+generated_file)

        print("-> Test the generated blockfile")
        utils.test_block(self.block_ids, self.block_fee,
                         self.block_wts, result)


solution = Solution()
solution.run("mempool.csv")
