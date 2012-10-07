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

#This is Round 5 and will cover questions on "bound" and "delay load" imports

import os
import random
import pefile
from time import time
from rounds.helpers import CheckAnswerNum, CheckAnswerString
import rounds.helpers

#This function asks questions about the IMAGE_OPTIONAL_HEADER.DataDirectory entries
#that pertain to normal imports
def R5Q0(questionCounter):
  #NOTE: if you update the number of questions in this function, you need to update the boundaries in StartR2
  Qs = ["What is the value of IMAGE_OPTIONAL_HEADER.DataDirectory[IMAGE_DIRECTORY_ENTRY_BOUND_IMPORT].RVA?",
        "What is the RVA that points at the bound import directory table?",
        "What is the value of IMAGE_OPTIONAL_HEADER.DataDirectory[IMAGE_DIRECTORY_ENTRY_BOUND_IMPORT].Size?",
        "What is the size of the bound import directory table?",
        "What is the value of IMAGE_OPTIONAL_HEADER.DataDirectory[IMAGE_DIRECTORY_ENTRY_DELAY_IMPORT].RVA?",
        "What is the RVA that points directly at the delay-load Import Address Table (IAT)?",
        "What is the value of IMAGE_OPTIONAL_HEADER.DataDirectory[IMAGE_DIRECTORY_ENTRY_DELAY_IMPORT].Size?",
        "What is the total size of the delay-load Import Address Table (IAT)?"]
  #NOTE: if you update the number of questions in this function, you need to update the boundaries in StartR2

  x = random.randint(0,3)
  if x == 0:
    pe = pefile.PE('../template32-bound.exe')
    suffix = ".exe"
  elif x == 1:
    pe = pefile.PE('../template64-bound.exe')
    suffix = ".exe"
  elif x == 2:
    pe = pefile.PE('../template32-bound.dll')
    suffix = ".dll"
  else:
    pe = pefile.PE('../template64-bound.dll')
    suffix = ".dll"

  #TODO: eventually I want to be able to move around the IAT

  #write out the (actually un)modified file
  outFileName = "Round5Q" + str(questionCounter) + suffix
  pe.write(outFileName)
  
  #Print the question
  q = random.randint(0,len(Qs)-1)
  print "For binary R5Bins/%s..." % outFileName
  print Qs[q]
  answer = raw_input("Answer: ")

  if q == 0 or q == 1:
    CheckAnswerNum(answer,pe.OPTIONAL_HEADER.DATA_DIRECTORY[11].VirtualAddress)
  elif q == 2 or q == 3:
    CheckAnswerNum(answer,pe.OPTIONAL_HEADER.DATA_DIRECTORY[11].Size)
  elif q == 4 or q == 5:
    CheckAnswerNum(answer,pe.OPTIONAL_HEADER.DATA_DIRECTORY[13].VirtualAddress)
  elif q == 6 or q == 7:
    CheckAnswerNum(answer,pe.OPTIONAL_HEADER.DATA_DIRECTORY[13].Size)

def StartR5(seed, suppressRoundBanner, escapeScore):
  global gScore
  global gNextLevelRequiredScore
  if not suppressRoundBanner:
    print "================================================================================"
    print "Welcome to Round 4:"
    print "This round is all about \"bound\" imports and delay-loaded imports"
    print "\nRound terminology note:"
    print "RVA = Relative Virtual Address (relative to image base)."
    print "AVA = Absolute Virtual Address (base + RVA)"
    print "================================================================================\n"
  #making a directory that the files go into, just to keep things tidier
  try:
    os.mkdir("R5Bins")
  except OSError:
    pass
  os.chdir("R5Bins")
  filelist = [ f for f in os.listdir(".")]
  for f in filelist:
    os.remove(f)
  roundStartTime = int(time())
  rounds.helpers.gNextLevelRequiredScore = escapeScore
  random.seed(seed)
  questionCounter = 0;
  while rounds.helpers.gScore < rounds.helpers.gNextLevelRequiredScore:
    #Now changed it so that a given R*Q* only has as many chances to be called
    #as it has calls to CheckAnswer*. This way the number of variant ways
    #to ask the question doesn't increase the probability of the question being asked
    #NOTE: if you update the number of questions in the round, you need to update these boundaries
    x = random.randint(0,3)
    if x <= 3:
      R5Q0(questionCounter)
#    elif x <= 5:
#      R4Q1(questionCounter)
#    elif x <= 8:
#      R4Q2(questionCounter)
#    elif x <= 14:
#      R4Q3(questionCounter)
      
    questionCounter+=1

  if not suppressRoundBanner:
    currentTime = int(time())
    roundTime = currentTime - roundStartTime
    roundMinutes = roundTime / 60
    roundSeconds = roundTime % 60
    totalElapsedTime = currentTime - rounds.helpers.gAbsoluteStartTime
    print "\nCongratulations, you passed round 5!"
    print "It took you %u minutes, %u seconds for this round." % (roundMinutes, roundSeconds)
    totalMinutes = totalElapsedTime / 60
    totalSeconds = totalElapsedTime % 60
    print "And so far it's taken you a total time of %u minutes, %u seconds." % (totalMinutes, totalSeconds) 

  os.chdir("..")