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

#This is Round 6 and will cover questions about the exports
#and the Export Address Table (EAT)

import os
import random
import pefile
from time import time
from rounds.helpers import CheckAnswerNum, CheckAnswerString
import rounds.helpers


def StartR6(seed):
  global gScore
  global gNextLevelRequiredScore

  gNextLevelRequiredScore = 3000
  random.seed(seed)
  print "I'm just a placeholder! :D"

