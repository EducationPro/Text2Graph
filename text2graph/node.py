from lemmatizer import lemmatizer

class Node:
	def __init__ (self):
		self.properties = []
		self.actions = []
	def extendAction (self, act, Object):
		if Object is list:
			for x in Object:
				self.actions.append({'action': lemmatizer.to_verb(act), 'obj': x})
		else:
			self.actions.append({'action': lemmatizer.to_verb(act), 'obj': Object})
	def extendProperty (self, Object):
		if Object is list:
			for x in Object:
				self.properties.append(x)
		else:
			self.properties.append(Object)

		self.properties = [x for x in set(self.properties)]

	def extendNode (self, node):
		if type(node) == type(self):
			for i in node.properties:
				self.properties.append (i)
			for i in list(node.actions):
				self.actions.append (i)
		else:
			for n in node.nodes:
				for i in n.properties:
					self.properties.append (i)
				for i in list(n.actions):
					self.actions.append (i)
		self.properties = [x for x in set(self.properties)]

	def findNode (self, doActions = [], hasProperties = []):
		matches = 0
		hasProperties = [x.lower() for x in set(hasProperties)]
		doActions = [x.lower() for x in set(doActions)]
		matches = sum([int(x.lower () in hasProperties) for x in set (self.properties)])
		
		for x in doActions:
			for y in self.actions:
				if x == y['action'].lower ():
					matches += 1
					break
		ans = []
		if matches == len(doActions) + len(hasProperties):
			ans = [self]

		for x in self.actions:
			response = x['obj'].findNode (doActions, hasProperties)
			if response != None:
				ans.extend (response)
		
		if ans == []:
			return None
		else:
			return ans
	
	def get (self):
		return [self]
	
	def all_nodes (self):
		ans = [self]
		for x in self.actions:
			ans.extend (x['obj'].all_nodes ())
		return ans
	
	def all_properties (self):
		return self.properties
	
	def all_actions (self):
		return self.actions

	def getAsObject(self):
		return {
				'properties': [x for x in self.properties],
				'actions': [
					{ 'action': x['action'], 'obj': x['obj'].getAsObject () } for x in self.actions 
				]
			}

	def printStr (self, tabs = 0, action = ''):
		print('  ' * tabs, end=action)
		print('(', ','.join(self.properties),')')
		for x in self.actions:
			x['obj'].printStr (tabs = tabs+1, action = x['action'] + ': ')
	
	def __str__(self):
		return "({0})".format (', '.join(self.properties))
