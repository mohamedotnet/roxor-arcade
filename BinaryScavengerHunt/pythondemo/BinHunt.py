#Binary Scavenger Hunt
#A game developed by Xeno Kovah for the class "The Life of Binaries"
#(my first largish program written in python. be kind. rewind)
# This game is meant to reinforce the materials covered in the class
# by giving them hands-on experience using tools to determine
# particular attributes of PE binaries
#Class material and videos available at:
#http://OpenSecurityTraining.info/LifeOfBinaries.html
#This game licensed Creative Commons, Share-Alike w/ Attribution
#http://creativecommons.org/licenses/by-sa/3.0/
# Special thanks to Ero Carrera for creating the pefile python library,
# without which, making this game would have taken much longer

import os
import random
import pefile
from time import time
from rounds.Round1 import Round1 
from rounds.Round2 import Round2 

#player's current score
gScore = 0  
gNextLevelRequiredScore = 0


#############################
#MAIN CODE STARTS HERE
#############################
print "Welcome to Binary Scavenger Hunt!\n\n"
mode = raw_input("Enter 0 for single player mode or 1 for class mode: ")
seed = "0"

if mode == "1":
  print "You will be asked for a 'seed'. This is just a number that affects"
  print "the way the internal random number generator works."
  print "WAIT for your instructor to tell you the seed.\n"
  seed = raw_input("Enter the seed: ")
else:
  mode = "0"

if mode == "0" or seed == "0":
	#Get the current time (it will be a float before we use int()) 
	#to use as a seed if they don't want to specify one 
	seed = int(time())
	print "Time-based seed = %u" % (seed)

Round1(seed)
if mode == "1":
  print "WAIT for your instructor to tell you the seed.\n"
  seed = raw_input("Enter the seed: ")
Round2(seed)
