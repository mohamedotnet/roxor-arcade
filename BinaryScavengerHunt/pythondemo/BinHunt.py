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
from rounds import *

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

Round1.StartR1(seed)
if mode == "1":
  print "WAIT for your instructor to tell you the seed.\n"
  seed = raw_input("Enter the seed: ")
Round2.StartR2(seed)
#TODO:I want it to be that you get a few questions from previous rounds 
#after you're done with the new questions
if mode == "1":
  print "WAIT for your instructor to tell you the seed.\n"
  seed = raw_input("Enter the seed: ")
Round3.StartR3(seed)
if mode == "1":
  print "WAIT for your instructor to tell you the seed.\n"
  seed = raw_input("Enter the seed: ")
Round4.StartR4(seed)
if mode == "1":
  print "WAIT for your instructor to tell you the seed.\n"
  seed = raw_input("Enter the seed: ")
Round5.StartR5(seed)
if mode == "1":
  print "WAIT for your instructor to tell you the seed.\n"
  seed = raw_input("Enter the seed: ")
Round6.StartR6(seed)
if mode == "1":
  print "WAIT for your instructor to tell you the seed.\n"
  seed = raw_input("Enter the seed: ")
Round7.StartR7(seed)
if mode == "1":
  print "WAIT for your instructor to tell you the seed.\n"
  seed = raw_input("Enter the seed: ")
Round8.StartR8(seed)
if mode == "1":
  print "WAIT for your instructor to tell you the seed.\n"
  seed = raw_input("Enter the seed: ")
Round9.StartR9(seed)
if mode == "1":
  print "WAIT for your instructor to tell you the seed.\n"
  seed = raw_input("Enter the seed: ")
Round10.StartR10(seed)
#Only now enter the bonus round if the user has got 100 in a row correct
if helpers.gWinningStreak >= 100:
  if mode == "1":
    print "WAIT for your instructor to tell you the seed.\n"
    seed = raw_input("Enter the seed: ")
  RoundX.StartRX(seed)
else:
  print "Congratulations on completing the game!"
  print "You should try the game again, and if you get 100 questions"
  print "in a row correct, you will unlock the bonus Round X :D"