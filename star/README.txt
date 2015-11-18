The smart_star_loop.py calls run_ribomap, which executes STAR.

The script builds an index on the input query (sail_trans_batch_list.txt for batch queries, sail_trans_list.txt for multiple single queries in sequence) and maps a random subset of short read files (sail_10_15_fasta_list.txt) to the index. Times are recorded and then analyzed separately.
