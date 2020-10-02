#This file contains the class of PDA.
#import needed libraries
import copy
import sys
#define the class of deterministic pushdown automata
class PDA:

#define global variables
	file_name = ''
	Q = 0
	input_alphabet=[]
	stack_alphabet=[]
	start_state = 0
	accept_states = []
	transition_table=[]
	input_string=''
	current_state=0
	stack=['$']

#input: string of file name containing PDA's descriptions
#init with file containing PDA's descriptions
	def __init__(self, str):
		self.file_name = str
		
#input: array containing the number of states
#instantiate the set of all states
	def buildQ(self, str):
		if int(str[0]) < 1:
			print("The number of states is less than 1. The program is terminated.")
			sys.exit()
		self.Q = str[0]
		print("There are "+self.Q+" states in this PDA.")
		
#input: an array containing the input symbols
#add symbols to the input_alphabet global variable
	def build_input_alphabet(self, str):
		for i in range(len(str)):
			if str[i] == '^':
				continue
			elif str[i] == '\n':
				break
			else:
				self.input_alphabet.append(str[i])
		print("The input alphabet for this PDA is: " + ' '.join(self.input_alphabet))
			
#input: an array containing the stack symbols
#add stack symbol to the stack_alphabet global variable
	def build_stack_alphabet(self, str):
		for i in range(len(str)):
			if str[i] == '^':
				continue
			elif str[i] == '\n':
				break
			else:
				self.stack_alphabet.append(str[i])
		print("The stack alphabet for this PDA is: " + ' '.join(self.stack_alphabet))
		
#input: the start state number
#instantiate the start_state global variable
	def build_start_state(self, str):
			self.start_state = str[0]
			print("The start state is: " + self.start_state)

#input: an array of accept states
#add the accept states to the accept_states global variable			
	def build_accept_states(self, str):
		for i in range(len(str)):
			if str[i] == ' ':
				continue
			elif str[i] == '\n':
				break
			else:
				self.accept_states.append(str[i])
		print("The accept states are: " + ' '.join(self.accept_states))

#input: an array of coded transitions
#add transitions to the transition_table global variable	
#handles improper coded transitions	
	def build_transition_table(self, str):
		print("The transition table is as follows:")
		for i in range(5,len(str)):
			line = str[i]
			transition = []
			for j in range(len(line)):
				if line[j] == ' ':
					continue
				elif line[j] == '\n':
					break
				else:
					transition.append(line[j])
			if not (int(transition[0])>0 and int(transition[0]) < int(self.Q)+1):
				print("First state isn't in the listed states. This transition is dropped.")
				continue
			if (transition[1] not in self.input_alphabet):
				print("Input symbol isn't in the input alphabet. This transition is dropped.")
				continue
			if (transition[2] not in self.stack_alphabet):
				print("The first stack symbol isn't in the stack alphabet. This transition is dropped.")
				continue
			if not (int(transition[3]) >0 and int(transition[3])<int(self.Q)+1):
				print("Second state isn't in the listed states. This transition is dropped.")
				continue
			if (transition[4] not in self.stack_alphabet):
				print("The second stack symbol isn't in the stack alphabet. This transition is dropped.")
				continue
			if (transition[2] == 'E' and transition[2] == transition[4]):
				print("You can only either push or pop in a transition. This transition is dropped.")
				continue
			self.transition_table.append(transition)
			f_half="State "+transition[0]+", on input "+transition[1]+" and top of stack " 
			s_half=transition[2]+", goes to state "+transition[3]+" with "+transition[4]+" as the new top of stack."
			message=f_half+s_half
			print(message)
		
#build the PDA given the PDA description from a file
	def build(self):
		print("Building PDA...")
		print()
		des_file = open(self.file_name, 'r')
		lines = des_file.readlines()
		#print(lines)
		self.buildQ(lines[0])
		self.build_input_alphabet(lines[1])
		self.build_stack_alphabet(lines[2])
		self.build_start_state(lines[3])
		self.build_accept_states(lines[4])
		self.build_transition_table(lines)
		print("Building PDA is complete.") 
		print()
		
#input: the first state and the input for a transition
#check existence of a transition in the transition table
	def exists_transition(self, state, inp):
		for transition in self.transition_table:
			if transition[0] == state and transition[1]==inp:
				return transition
			else:
				continue
		return None	
			
#input: the transition to be processed
#given a transition, this function propagates the machine to move to the next state
	def process_input(self, inp):
		if self.exists_transition(self.current_state, inp) == None:
			print("There doesn't exist a transition in the table for state "+self.current_state+" and symbol "+inp)
			return None
		else:
			transition = self.exists_transition(self.current_state, inp)
			if transition[2] == 'E':
				print("On state "+self.current_state+", input "+inp+", we push "+transition[4]+" on to the stack and goes to state "+transition[3])
				self.stack.append(transition[4])
				self.current_state = transition[3]
				print("The stack now, from bottom to top, is: ")
				list_stack = ""
				for i in range(len(self.stack)):
					list_stack += self.stack[i]+" "
				if list_stack == '':
					print("The stack is empty!")
				else:
					print(list_stack)
				return 1
			else:
				if transition[2] != self.stack[-1]:
					print("There exists a transition in the table for state "+self.current_state+" and symbol "+inp+", but top of stack doesn't match the transition.")
					return None
				else:
					print("On state "+self.current_state+", input "+inp+", we pop "+transition[2]+" from the stack and goes to state "+transition[3])
					self.stack.pop(-1)
					self.current_state = transition[3]
					print("The stack now, from bottom to top, is: ")
					list_stack = ""
					for i in range(len(self.stack)):
						list_stack += self.stack[i]+" "
					if list_stack == '':
						print("The stack is empty!")
					else:
						print(list_stack)
					return 1		
	
#input: a string of file name that contains the input to the PDA
#this function handles the file's input string and run the machine with the given input
	def execute(self,str):
		inp_file = open(str, 'r')
		inp = inp_file.read()
		self.input_string = inp
		print("Executing PDA with given input: "+self.input_string)
		self.current_state = copy.copy(self.start_state)
		for i in range(len(inp)):
			if inp[i] == '\n':
				print("End of input file.")
				break
			result=self.process_input(inp[i])
			if result == None:
				return "Thus, we reject."
			elif result == 1:
				continue
		if self.current_state in self.accept_states:
			print("The final state is one of the Accept states.")
			return "Accept."
		else:
			print("The final state is not one of the Accept states.")
			return "Thus, we reject."

