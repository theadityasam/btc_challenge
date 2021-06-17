import utils as util

parsed = util.parse_csv("test.csv")
block_ids, block_fee, block_wts = util.create_valid_mempool_list(parsed)
print("# Getting optimal value")
optimal_block_list = util.get_optimal_blocks_dp(
    block_fee, block_wts, len(block_ids))
result = [block_ids[i] for i in optimal_block_list]
util.dump_to_text(result)
