from node import Node

class MultiNode:
	def __init__ (self, existing = []):
		self.nodes = existing

	def extendAction (self, act, Object):
		for node in self.nodes:
			node.extendAction (act, Object)

	def extendProperty (self, Object):
		for node in self.nodes:
			node.extendProperty (Object)

	def extendNode (self, node):
		for _node in self.nodes:
			_node.extendNode (node)
	
	def addNode (self, new_node):
		self.nodes.append (new_node)

	def get (self):
		return self.nodes

	def getAsObject (self):
		return [x.getAsObject () for x in self.nodes]

	def findNode (self, doActions = [], hasProperties = []):
		answer = []
		for x in self.nodes:
			response = x.findNode (doActions, hasProperties)
			if response != None:
				answer.extend (response)
		if answer == []:
			return None
		else:
			return answer
	
	def printStr (self, tabs = 0, action = ''):
		for x in self.nodes:
			x.printStr (tabs = tabs, action = action)

	def __str__(self):
		return "[{0}]".format (', '.join(str(x) for x in self.nodes))

def NodeToMultiNode (node):
	return MultiNode ([node]) 

def simplify (multinode):
	tmp = MultiNode ()
	for x in multinode.nodes:
		if x != Node ():
			tmp.addNode (x)
	
	multinode = tmp

	if len(multinode.nodes) == 1:
		return multinode.nodes [0]
	else:
		return multinode
