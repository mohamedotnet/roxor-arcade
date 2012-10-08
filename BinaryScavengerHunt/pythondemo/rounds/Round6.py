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

#Question about export by ordinal

#Question about forwarded exports

#TODO: Now that we've covered exports
#add a question about AVA of a given import
#note: this seems like it will require either including the binaries
#or just making up a presumed base address and then pointing them
#at the ../exports/ files

def StartR6(seed, suppressRoundBanner, escapeScore):
  global gScore
  global gNextLevelRequiredScore

  gNextLevelRequiredScore = escapeScore
  random.seed(seed)
  print "I'm just a placeholder! :D"

