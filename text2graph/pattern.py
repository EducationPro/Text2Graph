from lemmatizer import lemmatizer

class PatternNode:

	def __init__ (self):
		self.properties = []
		self.actions = []

	def extendProperty (self, Object):
		if Object is list:
			for x in Object:
				self.properties.append(x)
		else:
			self.properties.append(Object)

		self.properties = [x for x in set(self.properties)]
	
	def extendAction (self, act, Object):
		if Object is list:
			for x in Object:
				self.actions.append({'action': lemmatizer.to_verb(act), 'obj': x})
		else:
			self.actions.append({'action': lemmatizer.to_verb(act), 'obj': Object})
	
	def all_nodes (self):
		ans = [self]
		return ans
	
	def all_properties (self):
		return self.properties

	def printStr (self, tabs = 0, action = ''):
		print('  ' * tabs, end=action)
		print('Pattern(', ','.join(self.properties),')')
