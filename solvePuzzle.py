from collections import deque
from random import shuffle
import sys

class Box:

	def __init__(self, _num, _color):
		self.num = _num
		self.color = _color

	def getNum(self):
		return self.num

	def getColor(self):
		return self.color

	def prettyPrint(self):
		return "{ " + str(self.num) + ", " + self.color + " }"

class findPuzzleSolution:

	def __init__(self, dimension):
		self.globalCount = 0
		self.globalMax = 0
		self.BRD_DIM = dimension

	def improvedHeuristicHelper(self, list):
		
		# Check Columns
		# Find limits
		colRangeCount = 0
		for idx in range(self.BRD_DIM):
			if list[idx] == None:
				break
			else:
				colRangeCount += 1

		for col in range(colRangeCount):
			depthRangeCount = 0

			# Find depth of column
			for row in range(self.BRD_DIM):
				if list[col + self.BRD_DIM*row] == None:
					break
				else:
					depthRangeCount += 1

			# Traverse Columns
			dummyNums = dict()
			dummyColors = dict()
			for row in range(depthRangeCount):

				idx = col + self.BRD_DIM*row
				
				# Check Number
				if list[idx].getNum() in dummyNums:
					return False
				else:
					dummyNums[list[idx].getNum()] = 1

				# Check Color
				if list[idx].getColor() in dummyColors:
					return False
				else:
					dummyColors[list[idx].getColor()] = 1

		# Better row range count
		for idx in range(0, pow(self.BRD_DIM, 2), self.BRD_DIM):
			dummyNums = dict()
			dummyColors = dict()

			for cols in range(idx, idx + self.BRD_DIM):
				if list[cols] != None:
					if list[cols].getNum() in dummyNums:
						return False
					else:
						dummyNums[list[cols].getNum()] = 1

					if list[cols].getColor() in dummyColors:
						return False
					else:
						dummyColors[list[cols].getColor()] = 1
				else:
					break

		# Diags
		topToBot = range(0, pow(self.BRD_DIM, 2), self.BRD_DIM + 1)
		botToTop = range(pow(self.BRD_DIM, 2) - self.BRD_DIM, self.BRD_DIM - 2, -1*(self.BRD_DIM - 1))
		botToTop.reverse()

		dummyNums = dict()
		dummyColors = dict()

		# Construct upwards diag
		for idx in botToTop:
			if list[idx] != None:	
				if list[idx].getNum() in dummyNums:
					return False
				else:
					dummyNums[list[idx].getNum()] = 1

				if list[idx].getColor() in dummyColors:
					return False
				else:
					dummyColors[list[idx].getColor()] = 1
			else:
				break

		dummyNums = dict()
		dummyColors = dict()

		# Construct downwards diag
		for idx in topToBot:
			if list[idx] != None:	
				if list[idx].getNum() in dummyNums:
					return False
				else:
					dummyNums[list[idx].getNum()] = 1

				if list[idx].getColor() in dummyColors:
					return False
				else:
					dummyColors[list[idx].getColor()] = 1
			else:
				break

		return True

	def validSol(self, list):

		# Check columns
		for col in range(self.BRD_DIM):
			dummyNums = dict()
			dummyColors = dict()

			for row in range(self.BRD_DIM):
				idx = col + self.BRD_DIM*row

				# Check unique numbers
				if list[idx].getNum() in dummyNums:
					return False
				else:
					dummyNums[list[idx].getNum()] = 1

				# Check unique color
				if list[idx].getColor() in dummyColors:
					return False
				else:
					dummyColors[list[idx].getColor()] = 1

		# Check rows
		for idx in range(pow(self.BRD_DIM, 2)):
			
			if idx % self.BRD_DIM == 0:
				dummyNums = dict()
				dummyColors = dict()

			# Check unique numbers
			if list[idx].getNum() in dummyNums:
				return False
			else:
				dummyNums[list[idx].getNum()] = 1

			# Check unique color
			if list[idx].getColor() in dummyColors:
				return False
			else:
				dummyColors[list[idx].getColor()] = 1

		# Check diagonal
		topToBot = range(0, pow(self.BRD_DIM, 2), self.BRD_DIM + 1)
		botToTop = range(pow(self.BRD_DIM, 2) - self.BRD_DIM, self.BRD_DIM - 2, -1*(self.BRD_DIM - 1))

		dummyNums = dict()
		dummyColors = dict()

		# Diag 1
		for idx in botToTop:
			# Check unique numbers
			if list[idx].getNum() in dummyNums:
				return False
			else:
				dummyNums[list[idx].getNum()] = 1

			# Check unique color
			if list[idx].getColor() in dummyColors:
				return False
			else:
				dummyColors[list[idx].getColor()] = 1

		dummyNums = dict()
		dummyColors = dict()

		# Diag 2
		for idx in topToBot:
			# Check unique numbers
			if list[idx].getNum() in dummyNums:
				return False
			else:
				dummyNums[list[idx].getNum()] = 1

			# Check unique color
			if list[idx].getColor() in dummyColors:
				return False
			else:
				dummyColors[list[idx].getColor()] = 1

		return True

	def printSol(self, list):

		for idx in range(len(list)):

			if idx % self.BRD_DIM == 0:
				print "\n"

			if list[idx] == None:
				print "    None     ",
			else:
				print list[idx].prettyPrint() + " ",

	# Constructs existing grid with NONES
	def construct(self, list):

		total = [None]*pow(self.BRD_DIM, 2)

		for idx in range(len(list)):
			total[idx] = list[idx]

		return total

	def genPerms(self, stack, queue):
		self.globalMax += 1

		if self.improvedHeuristicHelper(self.construct(stack)) == False:
			return

		if len(stack) == pow(self.BRD_DIM, 2) and self.validSol(stack) == True:
			self.printSol(stack)
			print "\n" + str(self.globalMax) + " iterations before solution was reached."
			sys.exit(0)
			return

		for idx in range(len(queue)):
			stack.append(queue.popleft())
			self.genPerms(stack, queue)
			queue.append(stack.pop())

#----------------------------------------------#
# Initialize board
queue = []
queue.extend([Box(1, "White "), Box(3, "White "), Box(5, "White "), Box(7, "White "), Box(9, "White ")])
queue.extend([Box(1, " Red  "), Box(3, " Red  "), Box(5, " Red  "), Box(7, " Red  "), Box(9, " Red  ")])
queue.extend([Box(1, " Blue "), Box(3, " Blue "), Box(5, " Blue "), Box(7, " Blue "), Box(9, " Blue ")])
queue.extend([Box(1, "Green "), Box(3, "Green "), Box(5, "Green "), Box(7, "Green "), Box(9, "Green ")])
queue.extend([Box(1, "Yellow"), Box(3, "Yellow"), Box(5, "Yellow"), Box(7, "Yellow"), Box(9, "Yellow")])

# Solve
# Find diagonals
solution = findPuzzleSolution(5)

# Run shuffle to randomize and increase chances of finding solution faster
queue = deque(queue)
#shuffle(queue)
solution.genPerms([], queue)


