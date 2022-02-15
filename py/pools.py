import requests
import graph as gph
import numpy as np

QUERY = """
{{
    pairs(first: 1000, where: {{id_gt: "{l_id}", reserve0_gt: 100, reserve1_gt: 100 }}, orderBy: id) {{
        id
        token0 {{
            id
            symbol
        }}
        token1 {{
            id
            symbol
        }}
        reserve0
        reserve1
    }}
}}
"""

def getPools(url):
    """
    Gathers relevant information of every liquidity pool using the subgraph
    query API ``url``.
    """
    last_id = ""
    # graph = {}
    graph = gph.Graph()

    while True:
        # make request to API
        query = QUERY.format(l_id=last_id)
        req = requests.post(url, json={"query": query})

        # check if request successful
        if req.status_code == 200:
            data = req.json()
            if "data" in data:
                pairs = data["data"]["pairs"]
            else:
                continue

            # format data
            # results += [_parseItem(item) for item in pairs if float(
            #     item['reserve0']) > 10 and float(item['reserve1']) > 10]
            for pair in pairs:
                reserve0 = float(pair["reserve0"])
                reserve1 = float(pair["reserve1"])

                token0id = pair["token0"]["id"]
                token1id = pair["token1"]["id"]
                if token0id not in graph.nodes:
                    # graph[token0id] = []
                    graph.addNode(token0id)
                if token1id not in graph.nodes:
                    # graph[token1id] = []
                    graph.addNode(token1id)

                # graph[token0id].append(
                #     (
                #         reserve1 / reserve0,
                #         token1id,
                #         pair["id"],
                #     )
                # )
                # graph[token1id].append(
                #     (
                #         reserve0 / reserve1,
                #         token0id,
                #         pair["id"],
                #     )
                # )
                graph.addEdge(gph.Edge(token0id, token1id, -np.log(reserve1 / reserve0), pair["id"]))
                graph.addEdge(gph.Edge(token1id, token0id, -np.log(reserve0 / reserve1), pair["id"]))

            # update query parameter
            last_id = pairs[-1]["id"]

            # check if all pools gathered
            if len(pairs) < 1000:
                break

        
    print("broke out of loop")
    return graph