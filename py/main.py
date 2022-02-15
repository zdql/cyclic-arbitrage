import pools
import graph
import time
import secrets

# "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2"
UNISWAPV2_URL = "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2"


SUSHISWAP_URL = f"https://gateway.thegraph.com/api/{secrets.API_KEY}/subgraphs/id/0x4bb4c1b0745ef7b4642feeccd0740dec417ca0a0-0"

time0 = time.time()
uniV2pool = pools.getPools(UNISWAPV2_URL)
time1 = time.time()
negCycle = graph.negCycleBellmanFord(uniV2pool, "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2")
time2 = time.time()
print(negCycle)
print("time to calculate negative cycle: " + str(time2 - time1))
print("total time: " + str(time2 - time0))
