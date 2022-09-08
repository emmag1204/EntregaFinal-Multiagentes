class Node:
	def __init__(self, data):
		self.data = data
		self.next = None
		# 0: road 1:entry 2:exit
		self.prev = None
		# 1: true 0:false
		self.available = 1

class DoublyCircularLinkedList:
	def __init__(self):
		self.start = None
	
	def insertEnd(self, value):
		if self.start == None:
			new_node = Node(value)
			new_node.next = new_node.prev = new_node
			self.start = new_node
			return

		last = self.start.prev

		new_node = Node(value)
		
		new_node.next = self.start
		self.start.prev = new_node
		
		new_node.prev = last
		last.next = new_node
		return
	
	def insertBegin(self, value):
		if self.start == None:
			new_node = Node(value)
			new_node.next = new_node.prev = new_node
			self.start = new_node
			return

		last = self.start.prev
		new_node = Node(value)
		new_node.next = self.start
		new_node.prev = last
		
		self.start.prev = last.next  = new_node

		self.start = new_node
		return

	def insertAfter(self, value1, value2):
		if self.start == None: return 
		
		new_node = Node(value1)

		temp = self.start
		while (temp.data != value2):
			temp = temp.next
		next = temp.next

		temp.next = new_node
		new_node.prev = temp
		new_node.next = next
		next.prev = new_node 
		return 

	def display(self):
		if self.start == None: return 
		temp = self.start
		items = 0

		# Traversal in forward direction:
		while (temp.next != self.start):
			items += 1
			print(temp.data, temp.type, end=" ")
			temp = temp.next

		print(temp.data, temp.type)

	def setNewStart(self, value):
		if self.start == None: return 
		
		temp = self.start
		while (temp.data != value):
			temp = temp.next
		self.start = temp
		return 

	def findNode(self, value):
		if self.start == None: return 
		temp = self.start
		while (temp.data != value):
			temp = temp.next
		return temp

def buildRoundAbout(positions):
	roundabout = DoublyCircularLinkedList()
	
	#Left side 
	i = 0
	while positions[i][0] < positions[i+1][0]:
		roundabout.insertEnd(positions[i])
		i+=1
	roundabout.insertEnd(positions[i])
	
	roundabout_lateral_size = i+1

	#Middle Part
	for index, position in enumerate(positions[ 
			roundabout_lateral_size : len(positions)-roundabout_lateral_size]):
		i+=1
		if index % 2 == 0:
			roundabout.insertBegin(position)
		else:
			roundabout.insertEnd(position)

	#Right Part
	for index, position in enumerate(positions[i+1:]):
		roundabout.insertBegin(position)
	
	return roundabout
