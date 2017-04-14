class Node:
	def __init__(self):
		self.label = None
		self.children = {}
		# you may want to add additional fields here...
		self.direction = {}
		self.modeClass = None
		self.classString = None
	def get_label(self):
		return self.label

	def get_children(self):
		return self.children

	def get_direction(self):
		return self.direction

	def get_parent(self):
		return self.parent

	def get_modeClass(self):
		return self.modeClass

	def get_classString(self):
		return self.classString