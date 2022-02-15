import unittest
import graph as gph
import numpy as np

def nodesInvolved(_cycle):

    result = []

    for x in _cycle:

        result.append(x[0])

    result.sort()
    return result

class TestGraph(unittest.TestCase):

    def testNegCycle1(self):

        graph = gph.Graph()

        edge1 = gph.Edge("A", "B", -np.log(0.5), "AB")
        edge2 = gph.Edge("B", "D", -np.log(2), "BD")
        edge3 = gph.Edge("D", "C", -np.log(5), "DC")
        edge4 = gph.Edge("C", "B", -np.log(3), "CB")
        
        graph.addEdge(edge1)
        graph.addEdge(edge2)
        graph.addEdge(edge3)
        graph.addEdge(edge4)

        graph.addNode("A")
        graph.addNode("B")
        graph.addNode("C")
        graph.addNode("D")

        result = gph.negCycleBellmanFord(graph, "A")

        expected_result = ["B", "D", "C"]
        expected_result.sort()

        self.assertEqual(nodesInvolved(result), expected_result)

    def testNoNegCycle1(self):

        graph = gph.Graph()

        edge1 = gph.Edge("A", "B", -np.log(0.5), "AB")
        edge2 = gph.Edge("B", "D", -np.log(1/3), "BD")
        edge3 = gph.Edge("D", "C", -np.log(1/4), "DC")
        edge4 = gph.Edge("C", "B", -np.log(1/5), "CB")
        
        graph.addEdge(edge1)
        graph.addEdge(edge2)
        graph.addEdge(edge3)
        graph.addEdge(edge4)

        graph.addNode("A")
        graph.addNode("B")
        graph.addNode("C")
        graph.addNode("D")

        result = gph.negCycleBellmanFord(graph, "A")

        self.assertEqual(result, -1)


if __name__ == "__main__":

    unittest.main()