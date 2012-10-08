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

#This is Round 7 and will cover questions on relocations and debug info

import os
import random
import pefile
from time import time
from rounds.helpers import CheckAnswerNum, CheckAnswerString
import rounds.helpers

#Q: According to the debugging information, when was this file compiled?
#Q: does the debug TimeDateStamp match the File Header TimeDateStamp?
#Q: What is the path where this file was compiled


def StartR7(seed, suppressRoundBanner, escapeScore):
  global gScore
  global gNextLevelRequiredScore

  gNextLevelRequiredScore = escapeScore
  random.seed(seed)
  print "I'm just a placeholder! :D"

