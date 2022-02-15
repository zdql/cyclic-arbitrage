import original_graph as pools

# import find_neg_cycle
import numpy as np

UNISWAPV2_URL = "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2"
uniV2Pools = pools.getPools(UNISWAPV2_URL)
print(f"done uni {len(uniV2Pools)}")