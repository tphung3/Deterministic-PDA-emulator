#import libraries and PDA class
import sys
from PDA_machine import PDA
#read the description file of PDA and input
PDA_machine = sys.argv[1]
input_file = sys.argv[2]
pda_m = PDA(PDA_machine)
#build the PDA
pda_m.build()
print("Please verify that PDA is constructed correctly. Proceed?[Y/N]")
user_inp = input()
if (user_inp=='Y' or user_inp=='y'):
	print("OK.")
elif (user_inp=='N' or user_inp=='n'):
 	print("The program is terminated. Please revise your encoded PDA file.")
 	exit()
else:
	print("Invalid response. THe program is terminated.")
	exit()
#execute the PDA with the given input
result = pda_m.execute(input_file)
print(result)

