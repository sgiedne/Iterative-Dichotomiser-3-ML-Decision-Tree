class Node:
	def __init__(self):
		self.label = None
		self.children = {}
		# you may want to add additional fields here...
		self.direction = {}

		self.democrats = 0
		self.republicans = 0
		self.mode = None
		self.examples = []

	def get_label(self):
		return self.label

	def get_children(self):
		return self.children

	def get_direction(self):
		return self.direction
