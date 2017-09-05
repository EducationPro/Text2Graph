class Graph:
	def __init__(self):
		self.n = 0
		self.m = 0
		self.nodes = dict()
		self.ln = list()

	def add_node(self, node):
		self.nodes[node] = self.n
		self.n += 1
		self.ln [self.n - 1] = dict()

	def add_edge(self, start, end, weight):
		self.ln[self.nodes [start]][slef.nodes [end]] = weight

	def has(self, start, end):
		if start in self.nodes and self.nodes[end] in self.ln[self.nodes[start]]:
			return self.ln[self.nodes[start]][self.nodes[end]]
		else:
			return None
