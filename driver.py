import utils as util

filename = "trial.csv"
parsed = util.parse_csv(filename)
print("-> Parsed - "+filename)
block_ids, block_fee, block_wts = util.create_valid_mempool_list(parsed)
print("-> Generated valid mempool list")
print("-> Getting optimal transaction selection")
optimal_block_list = util.get_optimal_blocks_dp(
    block_fee, block_wts, len(block_ids), 6000)
result = [block_ids[i] for i in optimal_block_list]
generated_file = util.dump_to_text(result)
print("-> Generated block file: "+generated_file)
