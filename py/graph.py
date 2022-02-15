from unittest import result
import random
import numpy as np
import multiprocessing as mp
import time

aave_accepted_tokens = [
    "0x7fc66500c84a76ad7e9c93437bfc5ac33e2ddae9", # AAVE
    "0xd46ba6d942050d489dbd938a2c909a5d5039a161", # AMPL
    "0xba100000625a3754423978a60c9317c58a424e3d", # BAL
    "0x0d8775f648430679a709e98d2b0cb6250d2887ef", # BAT
    "0x4fabb145d64652a948d72533023f6e7a623c7c53", # BUSD
    "0xd533a949740bb3306d119cc777fa900ba034cd52c", # CRV
    "0x6b175474e89094c44da98b954eedeac495271d0f", # DAI
    "0xf629cbd94d3791c9250152bd8dfbdf380e2a3b9c", # ENJ
    "0x956f47f50a910163d8bf957cf5846d573e7f87ca", # FEI
    "0x853d955acef822db058eb8505911ed77f175b99e", # FRAX
    "0x056fd409e1d7a124bd7017459dfea2f387b6d5cd", # GUSD
    "0xdd974d5c2e2928dea5f71b9825b8b646686bd200", # KNC
    "0x514910771af9ca656af840dff83e8264ecf986ca", # LINK
    "0x0f5d2fb29fb7d3cfee444a200298f468908cc942", # MANA
    "0x9f8f72aa9304c8b593d555f12ef6589cc3a579a2", # MKR
    "0x03ab458634910aad20ef5f1c8ee96f1d6ac54919", # RAI
    "0x408e41876cccdc0f92210600ef50372656052a38", # REN
    "0xd5147bc8e386d91cc5dbe72099dac6c9b99276f5", # RENFIL
    "0xc011a73ee8576fb46f5e1c5751ca3b9fe0af2a6f", # SNX
    "0x57ab1ec28d129707052df4df418d58a2d46d5f51", # SUSD
    "0x0000000000085d4780b73119b644ae5ecd22b376", # TUSD
    "0x1f9840a85d5af5bf1d1762f925bdaddc4201f984", # UNI
    "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48", # USDC
    "0x8e870d67f660d95d5be530380d0ec0bd388289e1", # USDP
    "0xdac17f958d2ee523a2206206994597c13d831ec7", # USDT
    "0x2260fac5e5542a773aa44fbcfedf7c193bc2c599", # WBTC
    "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2", # WETH
    "0x8798249c2e607446efb7ad49ec89dd1865ff4272", # XSUSHI
    "0x0bc529c00c6401aef6d220be8c6ea1667f6ad93e", # YFI
    "0xe41d2489571d322189246dafa5ebde1f4699f498" # ZRX
    ]

useMultiprocessing = True

class Edge:
    """
    Representation of a graph edge
    """

    def __init__(self, _src, _dest, _weight, _id):
        """
        Initializes an edge, taking in values for the source node, destination
        node, the weight of the edge, and the id of the liquidity pool. [_src],
        [_dest], [_id] must be strings. [_weight] must be an int/float.
        """
        self.src = _src
        self.dest = _dest
        self.weight = _weight
        self.id = _id

class Graph:
    """
    Representation of a graph. 
    """

    def __init__(self):
        """
        Initializes an graph. Sets the number of edges and the number of nodes
        equal to 0. In addition, creates the association lists for edges and 
        nodes
        """

        self.numOfNodes = 0
        self.numOfEdges = 0

        self.edges = []
        self.nodes = []

    def addNode(self, _node):
        """
        Adds a node to the graph, adding it to self.nodes and updating the 
        number of nodes present 
        """
        self.nodes.append(_node)
        self.numOfNodes += 1

    def addEdge(self, _edge):
        """
        Adds an edge to the graph, adding it to self.edges and updating the 
        number of edges present
        """
        self.edges.append(_edge)
        self.numOfEdges += 1

def getNegativeNode(_edges, _dist):
    """
    Helper function for negCycleBellmanFord(). Returns a node that is part of a
    negative cycle
    """

    C = None

    for i in range(len(_edges)):

        u = _edges[i].src
        v = _edges[i].dest
        weight = _edges[i].weight
        poolID = _edges[i].id

        if (_dist[u] != float('inf') and _dist[u] + weight < _dist[v]):
            C = (v, poolID)
    return C

manager = mp.Manager()
shared_list = manager.list()

def processNegCycle(graph, edges, parent, dist, queue):
    """
    Function meant to be used for multiprocessing.

    Returns None if a negative cycle is not possible, returns -1 if the process
    created an unacceptable cycle
    """
    C = getNegativeNode(edges, dist)


    if C in list(shared_list):
        queue.put(-1)

    

    if (C == (None, None) or C == None):
        queue.put(None)
    else:
        for i in range(graph.numOfNodes):
            C = parent[C[0]]
            
        cycle = []
        v = C

        while True:
            cycle.append(v)
            if (v == C and len(cycle) > 1):
                break
            v = parent[v[0]]

        if len(cycle) > 4:
            queue.put(-1)
            shared_list.append(C)
            return

        totalWeight = 0
        for i in range(0, len(cycle) - 1):
            totalWeight += cycle[i][2]
        
        if totalWeight >= -np.log((1.03 ** 3) * 1.0009):
            queue.put(-1)
            shared_list.append(C)
            return

        cycle.reverse()
        result = []
        for i in range(len(cycle)):

            if i == len(cycle) - 2:
                result.append((cycle[i][0], cycle[i+1][0], cycle[i][1]))
                # cycleWeight += cycle[i][2]
                break

            else:
                result.append((cycle[i][0], cycle[i+1][0], cycle[i][1]))

        if cycle[0][0] not in aave_accepted_tokens:
            queue.put(-1)
            shared_list.append(C)
            return

        queue.put(result)
        



def negCycleBellmanFord(graph, src):
    """
    Main function for computing a feasible 3-node cyclical arbitrage
    opportunity.
    
    Returns a list of tuples describing the cycle to take. Returns -1 if no
    arbitrage opportunities exist.
    """
    # Maps nodes to their distance relative to src
    dist = {}
    # Maps nodes to their parent, related poolID, and edge weight
    parent = {}

    for node in graph.nodes:
        dist[node] = float("inf")
    for node in graph.nodes:
        parent[node] = (None, None)

    listOfNodes = graph.nodes
    listOfNodes.insert(0, listOfNodes.pop(listOfNodes.index(src)))

    dist[src] = 0

    # Lemma: If an iteration of the main loop of algorithm terminates without
    # making any changes, the algorithm itself can be terminated.
    noChanges = True

    # Main Bellman-Ford Algorithm
    for i in range(1, graph.numOfNodes):

        noChanges = True

        for j in range(graph.numOfEdges):


            u = graph.edges[j].src
            v = graph.edges[j].dest
            weight = graph.edges[j].weight
            poolID = graph.edges[j].id

            # Edge Relaxation
            if (dist[u] != float('inf') and dist[u] + weight < dist[v]):

                noChanges = False

                dist[v] = dist[u] + weight
                # tuple = (source, poolID, weight in opposite direction)
                parent[v] = (u, poolID, weight)

        if noChanges:
            break

    # All code from here can be used in multiprocessing
    print("on multiprocessing!")
    time0 = time.time()
    if useMultiprocessing:
        while True:
            queue = mp.Queue()

            listOfProcesses = []
            availableProcesses = mp.cpu_count()

            for i in range(availableProcesses):
                random.shuffle(graph.edges)
                pr = mp.Process(target=processNegCycle, args=(graph, graph.edges, parent, dist, queue))
                listOfProcesses.append(pr)
            
            for pr in listOfProcesses:
                pr.start()

            for pr in listOfProcesses:
                pr.join()

            results = [queue.get() for pr in listOfProcesses]

            for result in results:
                if result == None:
                    return -1
                if result != -1:
                    return result
            
            # print(len(list(shared_list)))
            # if len(list(shared_list)) > 2000:
            #     print("TOO MANY CYCLES, CANCELLING")
            #     return -1

            time1 = time.time()
            if (time1 - time0 > 10):
                print("ETH BLOCK HAS PASSED")
                return -1

            print("another round of multiprocessing!")
        
    else:
        # Gets a node that's part of a negative cycle
        C = getNegativeNode(graph.edges, dist)

        # Result of getNegativeNode
        while True:
            # If there exists a negative node
            if (C != (None, None) and C != None):
                for i in range(graph.numOfNodes):
                    C = parent[C[0]]
                
                cycle = []
                v = C

                while True:
                    cycle.append(v)
                    if (v == C and len(cycle) > 1):
                        break
                    v = parent[v[0]]
                
                if len(cycle) > 4:
                    random.shuffle(graph.edges)
                    C = getNegativeNode(graph.edges, dist)
                    continue
                
                totalWeight = 0
                for i in range(0, len(cycle) - 1):
                    totalWeight += cycle[i][2]
                
                if totalWeight >= -np.log((1.03 ** 3) * 1.0009):
                    random.shuffle(graph.edges)
                    C = getNegativeNode(graph.edges, dist)
                    continue

                cycle.reverse()
                result = []
                for i in range(len(cycle)):

                    if i == len(cycle) - 2:
                        result.append((cycle[i][0], cycle[i+1][0], cycle[i][1]))
                        # cycleWeight += cycle[i][2]
                        break

                    else:
                        result.append((cycle[i][0], cycle[i+1][0], cycle[i][1]))
                        # cycleWeight += cycle[i][2]

                # Each element returns a tuple of the format:
                # (from, to, poolID)

                # COMMENT OUT THE FOLLOWING IF TESTING WITH NODES THAT DON'T
                # REPRESENT TOKENS

                if cycle[0][0] not in aave_accepted_tokens:
                    print("START TOKEN NOT ACCEPTED")
                    random.shuffle(graph.edges)
                    C = getNegativeNode(graph.edges, dist)
                    continue

                return result
                
            else:
                
                return -1
