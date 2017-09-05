class Node:
	def __init__(self, index):
		self.index = index

class Graph:
	def __init__(self):
		self.n = 0
		self.m = 0
		self.nodes = dict()
		self.ln = list()

	def add_node(self, node):
		self.nodes[node] = self.n
		self.ln.append(dict())
		self.n += 1
		return Node(self.n - 1)

	def add_edge(self, weight, start, end):
		if type(start) == type(Node(0)):
			start = start.index
		else:
			start = self.nodes[start]

		if type(end) == type(Node(0)):
			end = end.index
		else:
			end = self.nodes[end]

		

#		raise BaseException(str(self.n) + ' ' + str(self.nodes[start]) + ' ' + str(self.nodes[end]))
#		raise BaseException(str(weight) + ' ' + str(self.nodes[start]) + ' ' + str(self.nodes[end]))
		self.ln[start][end] = weight

	def has(self, start, end):
		if start in self.nodes and self.nodes[end] in self.ln[self.nodes[start]]:
			return self.ln[self.nodes[start]][self.nodes[end]]
		else:
			return None

	def add_edges(self, graph):
		raise NotImplementedError('WordNet.add_edges method is not implemented yet')
