#Author: Sabrina Crowe
#Date: 3/4/23
import numpy as np
import copy
import collections.abc

#rubik_solver deprecated, so this is required for it to work
collections.Iterable = collections.abc.Iterable
collections.Mapping = collections.abc.Mapping
collections.MutableSet = collections.abc.MutableSet
collections.MutableMapping = collections.abc.MutableMapping
from rubik_solver import utils

class Puzzle:
	def __init__(self, top, bottom, left, right, back, front):
		#initializes rubiks cube
		self.top = np.array(top)
		self.bottom = np.array(bottom)
		self.left = np.array(left)
		self.right = np.array(right)
		self.back = np.array(back)
		self.front = np.array(front)

	def show(self):
		#show function, displays all sides
		print("Top side")
		print(self.top)
		print("Front side")
		print(self.front)
		print("Left side")
		print(self.left)
		print("Right side")
		print(self.right)
		print("Back side")
		print(self.back)
		print("Bottom side")
		print(self.bottom)

	# I'll include the functions that needed to be completed at the bottom, but they're redundant for how I chose
	# to solve this. The output of solving algorithms is made up of U, R, F, B, L, and D. The R instruction is the same as
	# rotate_column_up(2). And there is no instance in which only the middle column would need to be
	# rotated up. However, that functionality is still included.

	def U_(self):
		#I accidentally coded the U function to have the functionality of U', so I swapped them. I also
		#used different syntax here, then figured out a better way in later functions. But this still works
		'''performs U prime on rubiks cube'''
		temp = copy.deepcopy(self)
		self.top = np.rot90(self.top)
		self.front[0][0:3],self.right[0][0:3],self.back[0][0:3],self.left[0][0:3] = temp.left[0][0:3],temp.front[0][0:3]\
			,temp.right[0][0:3],temp.back[0][0:3]

	def U(self):
		'''performs U on rubiks cube'''
		for i in range(3):
			self.U_()

	def R(self):
		'''performs R on rubiks cube'''
		temp = copy.deepcopy(self)
		self.right = np.rot90(self.right,3)
		self.front[:,2],self.bottom[:,2],self.back[:,0],self.top[:,2] = temp.bottom[:,2], np.flip(temp.back[:,0]),\
			np.flip(temp.top[:,2]),temp.front[:,2]

	def R_(self):
		'''performs R prime on rubiks cube'''
		#the trick with prime moves is that they are the same as their regular counterpart being performed 3x
		for i in range(3):
			self.R()

	def F(self):
		'''performs F on rubiks cube'''
		temp = copy.deepcopy(self)
		self.front = np.rot90(self.front,3)
		self.top[2] = np.flip(temp.left[:,2])
		self.right[:,0] = temp.top[2]
		self.left[:,2] = temp.bottom[0]
		self.bottom[0] = np.flip(temp.right[:,0])

	def F_(self):
		'''performs F prime on rubiks cube'''
		for i in range(3):
			self.F()

	def B(self):
		'''performs B on rubiks cube'''
		temp = copy.deepcopy(self)
		self.back = np.rot90(self.back,3)
		self.top[0] = temp.right[:,2]
		self.left[:,0] = np.flip(temp.top[0])
		self.right[:,2] = np.flip(temp.bottom[2])
		self.bottom[2] = temp.left[:,0]

	def B_(self):
		'''performs B prime on rubiks cube'''
		for i in range(3):
			self.B()

	def L(self):
		'''performs L on rubiks cube'''
		temp = copy.deepcopy(self)
		self.left = np.rot90(self.left, 3)
		self.front[:,0] = temp.top[:,0]
		self.top[:,0] = np.flip(temp.back[:,2])
		self.back[:,2] = np.flip(temp.bottom[:,0])
		self.bottom[:,0] = temp.front[:,0]

	def L_(self):
		'''performs L prime on rubiks cube'''
		for i in range(3):
			self.L()

	def D(self):
		'''performs D on rubiks cube'''
		temp = copy.deepcopy(self)
		self.bottom = np.rot90(self.bottom, 3)
		self.front[2] = temp.left[2]
		self.right[2] = temp.front[2]
		self.back[2] = temp.right[2]
		self.left[2] = temp.back[2]

	def D_(self):
		'''performs D prime on rubiks cube'''
		for i in range(3):
			self.D()

	def solveTrad(self):
		'''solves the rubiks cube in the traditional way; all sides have the same color'''
		inStr=""
		#this creates a string describing each face that is readable by the rubiks-solver algorithm
		cube = [self.top, self.left, self.front, self.right, self.back, self.bottom]
		for face in cube:
			for row in face:
				for c in row:
					inStr += c.lower()
		#the most efficient algorithm is Kociemba. Kociemba requires the top to be yellow, front be red, left be blue, etc.
		instructionsTemp = str(utils.solve(inStr, "Kociemba"))
		#this is so the 'moves' object the algorithm outputs, which was converted into a string, can be made a list
		instructionsTemp = instructionsTemp.replace('\'', '-')
		instructionsTemp = instructionsTemp.replace(' ', '')
		instructions = instructionsTemp.split(',')

		#gets rid of brackets
		instructions[0] = instructions[0][1:]
		instructions[-1] = instructions[-1][0:-1]
		#has the program perform each move in the instructions list
		self.moves(instructions)

	def solve(self):
		#in order to get the pattern with crosses on all sides, the cube must be solved normally
		self.solveTrad()
		#these are the instructions that create the pattern
		instructions=["L-","R2","D","F2","R-","D-","R-","L","U-","D","R","D","B2","R-","U","D2"]
		#has the program perform each move in the instructions list
		self.moves(instructions)
		#outputs the final faces of the cube
		self.show()

	def moves(self, instructions):
		#reads through list of instructions and chooses the appropriate function to perform
		for i in instructions:
			if i[0] == 'U':
				if i[-1] == '2':
					self.U()
					self.U()

				elif i[-1] != 'U':
					self.U_()

				else:
					self.U()

			elif i[0] == 'D':
				if i[-1] == '2':
					self.D()
					self.D()

				elif i[-1] != 'D':
					self.D_()

				else:
					self.D()

			elif i[0] == 'R':
				if i[-1] == '2':
					self.R()
					self.R()

				elif i[-1] != 'R':
					self.R_()

				else:
					self.R()

			elif i[0] == 'L':
				if i[-1] == '2':
					self.L()
					self.L()

				elif i[-1] != 'L':
					self.L_()


				else:
					self.L()

			elif i[0] == 'F':
				if i[-1] == '2':
					self.F()
					self.F()

				elif i[-1] != 'F':
					self.F_()

				else:
					self.F()

			elif i[0] == 'B':
				if i[-1] == '2':
					self.B()
					self.B()

				elif i[-1] != 'B':
					self.B_()

				else:
					self.B()

	#requested functions here
	def rotate_row_right(self, row_num):
		#I use my already made functions when it is equivalent
		if row_num == 0:
			self.U_()
		elif row_num == 2:
			self.D()
		else:
			#otherwise, I manually set the necessary row
			temp = copy.deepcopy(self)
			self.front[1] = temp.left[1]
			self.right[1] = temp.front[1]
			temp.back[1] = temp.right[1]
			temp.left[1] = temp.back[1]

	def rotate_row_left(self, row_num):
		if row_num == 0:
			self.U()
		elif row_num == 2:
			self.D_()
		else:
			#this saves me time by doing it three times instead of coding something different
			for i in range(3):
				self.rotate_row_left(1)

	def rotate_col_up(self, col_num):
		if col_num == 0:
			self.L_()
		elif col_num == 2:
			self.R()
		else:
			temp = copy.deepcopy(self)
			self.front[:,1] = temp.bottom[:,1]
			self.top[:,1] = temp.front[:,1]
			self.back[:,1] = np.flip(temp.top[:,1])
			self.bottom[:,1] = np.flip(temp.back[:,1])

	def rotate_col_down(self, col_num):
		if col_num == 0:
			self.L()
		elif col_num == 2:
			self.R_()
		else:
			for i in range(3):
				self.rotate_col_up(1)

	#no equivalents already coded in for these
	def rotate_cube_right(self):
		temp = copy.deepcopy(self)
		self.top = np.rot90(self.top)
		self.front = temp.left
		self.left = temp.back
		self.back = temp.right
		self.right = temp. front
		self.bottom = np.rot90(self.bottom,3)
	def rotate_cube_left(self):
		for i in range(3):
			self.rotate_cube_right()
	def rotate_cube_up(self):
		temp = copy.deepcopy(self)
		self.top = temp.front
		self.back = np.flip(temp.top)
		self.bottom = np.flip(temp.back)
		self.front = temp.bottom
		self.left = np.rot90(self.left)
		self.right = np.rot90(self.right, 3)
	def rotate_cube_down(self):
		for i in range(3):
			self.rotate_cube_up()

'''
These were used for testing and initializing the rubiks cubes
This is a pre-solved cube
sides = [[['W', 'W', 'W'], ['W', 'W', 'W'], ['W', 'W', 'W']], [['Y', 'Y', 'Y'], ['Y', 'Y', 'Y'], ['Y', 'Y', 'Y']],
        [['O', 'O', 'O'], ['O', 'O', 'O'], ['O', 'O', 'O']], [['R', 'R', 'R'], ['R', 'R', 'R'], ['R', 'R', 'R']],
        [['B', 'B', 'B'], ['B', 'B', 'B'], ['B', 'B', 'B']],
        [['G', 'G', 'G'], ['G', 'G', 'G'], ['G', 'G', 'G']]]
        
This has numbers in place of each color
sides = [[[45, 46, 47], [48, 49, 50], [51, 52, 53]], [[0, 1, 2], [3, 4, 5], [6, 7, 8]],
        [[36, 37, 38], [39, 40, 41], [42, 43, 44]], [[18, 19, 20], [21, 22, 23], [24, 25, 26]],
        [[9, 10, 11], [12, 13, 14], [15, 16, 17]], [[27, 28, 29], [30, 31, 32], [33, 34, 35]]]

This is a test case. Take this part out of the docstring if you want to see if it works
sides = [[['O', 'R', 'G'], ['O', 'W', 'R'], ['Y', 'B', 'Y']], [['W', 'O', 'W'], ['G', 'Y', 'B'], ['W', 'Y', 'O']],
        [['B', 'W', 'O'], ['R', 'O', 'R'], ['B', 'W', 'B']], [['R', 'O', 'W'], ['B', 'R', 'G'], ['Y', 'W', 'R']],
        [['G', 'Y', 'G'], ['Y', 'B', 'Y'], ['O', 'G', 'G']],
        [['B', 'O', 'R'], ['W', 'G', 'G'], ['Y', 'B', 'R']]]
cube = Puzzle(sides[1], sides[0], sides[4], sides[5], sides[2], sides[3])
cube.solve()
'''
