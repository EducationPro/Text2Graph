class Node:
	def __init__ (self):
		self.properties = []
		self.actions = []
	def extendAction (self, act, Object):
		if Object is list:
			for x in Object:
				self.actions.append({'action': act, 'obj': x})
		else:
			self.actions.append({'action': act, 'obj': Object})
	def extendProperty (self, Object):
		if Object is list:
			for x in Object:
				self.properties.append(x)
		else:
			self.properties.append(Object)

	def extendNode (self, node):
		for i in node.properties:
			self.properties.append (i)
		for i in list(node.actions):
			self.actions.append (i)
	
	def __str__(self):
		return "({0})".format (', '.join(self.properties))

