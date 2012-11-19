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
import sys
import random
import pefile
from time import time
from rounds import *
#import rounds.helpers

#This will select one question at a time randomly from rounds 1 to previousRoundCap, inclusive
def RandomQuestionsFromPreviousRounds(seed, roundEscapeScore, previousRoundCap):
  print "\nOh no! You've been teleported back to previous rounds!"
  print "Show that you haven't forgotten all the old material already!\n"
  qEscapeScore = helpers.gNextLevelRequiredScore
  while qEscapeScore < roundEscapeScore:
    qEscapeScore += 100
    x = random.randint(1,previousRoundCap)
    {1:Round1.StartR1,
     2:Round2.StartR2,
     3:Round3.StartR3,
     4:Round4.StartR4,
     5:Round5.StartR5,
     6:Round6.StartR6,
     7:Round7.StartR7,
     8:Round8.StartR8,
     9:Round9.StartR9,
     10:Round10.StartR10,
    }[x](seed+qEscapeScore, 1, qEscapeScore) #always suppressRoundBanner when called from this function
    #seed+qEscapeScore is because if you just keep entering only seed in each iteration
    #you will just keep re-seeding the PRNG in each round, thus getting the same
    #choice of questions each time
  print "\nOK, you escaped the previous rounds, time to move on!\n"

#############################
#MAIN CODE STARTS HERE
#############################
print "Welcome to Binary Scavenger Hunt!\n"
print "In this game you will learn about the\nPortable Executable (PE) binary format!\n\n"

#Entering a single command line argument will allow you to skip to that round
skipToRound = 1
if len(sys.argv) >= 2:
  print "First parameter = %u" % int(sys.argv[1])
  if(int(sys.argv[1]) <= 10):
    skipToRound = int(sys.argv[1])

mode = raw_input("Enter 0 for single player mode.\nEnter 1 for single player replay (specify the seed of a previous play).\nEnter 2 for class mode.\nMode: ")
seed = "0"

if mode == "2":
  print "You will be asked for a 'seed'. This is just a number that affects"
  print "the way the internal random number generator works."
  print "WAIT for your instructor to tell you the seed.\n"
  seed = int(raw_input("Enter the seed: "))
elif mode == "1":
  seed = int(raw_input("Enter the starting seed from your previous play: "))
else:
  #Default to single player mode if there is invalid input
  #Get the current time (it will be a float before we use int()) 
  #to use as a seed if they don't want to specify one 
  seed = int(time())
  print "Time-based seed = %u" % (seed)

helpers.gStartingSeed = seed
#need to set this here, so it doesn't get reset when we jump backwards to round 1 questions after round 2
helpers.gAbsoluteStartTime = int(time())

if skipToRound <= 1:
  Round1.StartR1(seed, 0, 1000)
  if mode == "2":
    print "WAIT for your instructor to tell you the seed.\n"
    seed = int(raw_input("Enter the seed: "))
if skipToRound <= 2:
  helpers.gScore = 1000
  Round2.StartR2(seed, 0, 2000)
  RandomQuestionsFromPreviousRounds(seed, 2500, 1)
  if mode == "2":
    print "WAIT for your instructor to tell you the seed.\n"
    seed = int(raw_input("Enter the seed: "))
if skipToRound <= 3:
  helpers.gScore = 2500
  Round3.StartR3(seed, 0, 3500)
  RandomQuestionsFromPreviousRounds(seed, 4000, 2)
  if mode == "2":
    print "WAIT for your instructor to tell you the seed.\n"
    seed = int(raw_input("Enter the seed: "))
if skipToRound <= 4:
  helpers.gScore = 4000
  Round4.StartR4(seed, 0, 5000)
  RandomQuestionsFromPreviousRounds(seed, 5500, 3)
  if mode == "2":
    print "WAIT for your instructor to tell you the seed.\n"
    seed = int(raw_input("Enter the seed: "))
if skipToRound <= 5:
  helpers.gScore = 5500
  Round5.StartR5(seed, 0, 6500)
  RandomQuestionsFromPreviousRounds(seed, 7000, 4)
  if mode == "2":
    print "WAIT for your instructor to tell you the seed.\n"
    seed = int(raw_input("Enter the seed: "))
if skipToRound <= 6:
  helpers.gScore = 7000
  Round6.StartR6(seed, 0, 8000)
  RandomQuestionsFromPreviousRounds(seed, 8500, 5)
  if mode == "2":
    print "WAIT for your instructor to tell you the seed.\n"
    seed = int(raw_input("Enter the seed: "))
if skipToRound <= 7:
  helpers.gScore = 8500
  Round7.StartR7(seed, 0, 9500)
  RandomQuestionsFromPreviousRounds(seed, 10000, 6)
  if mode == "2":
    print "WAIT for your instructor to tell you the seed.\n"
    seed = int(raw_input("Enter the seed: "))
if skipToRound <= 8:
  helpers.gScore = 10000
  Round8.StartR8(seed, 0, 11000)
  RandomQuestionsFromPreviousRounds(seed, 11500, 7)
  if mode == "2":
    print "WAIT for your instructor to tell you the seed.\n"
    seed = int(raw_input("Enter the seed: "))
if skipToRound <= 9:
  helpers.gScore = 11500
  Round9.StartR9(seed, 0, 12500)
  RandomQuestionsFromPreviousRounds(seed, 13000, 8)
  if mode == "2":
    print "WAIT for your instructor to tell you the seed.\n"
    seed = raw_input("Enter the seed: ")
if skipToRound <= 10:
  helpers.gScore = 13000
  Round10.StartR10(seed, 0, 14000)
  RandomQuestionsFromPreviousRounds(seed, 16500, 10)#ask more questions from all rounds 
#Only now enter the bonus round if the user has got 100 in a row correct
if helpers.gWinningStreak >= 100:
  print "Congratulations, you have made it to the mysterious Round X!"
  if mode == "2":
    print "But still WAIT for your instructor to tell you the seed ;)\n"
    seed = raw_input("Enter the seed: ")
  RoundX.StartRX(seed, 0, 25000)
else:
  print "Congratulations on completing the game!"
  print "You should try the game again, and if you get 100 questions"
  print "in a row correct, you will unlock the bonus Round X :D"