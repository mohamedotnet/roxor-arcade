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

#player's current score
gScore = 0  
gNextLevelRequiredScore = 0
gWinningStreak = 0
gTotalElapsedTime = 0

def CheckAnswerNum(studentAnswer, answerRadix, correctAnswer):
  global gScore
  global gNextLevelRequiredScore
  global gWinningStreak

  #ch347 0xc0d3zzz
  if studentAnswer == "s":
    gScore = gNextLevelRequiredScore
    print "gscore = %u" % gScore
    print "~tweeEEtle deeEEtle deeEEt~ W4Rp W1zzL3 4 5h1zzl3!"
    return

  print studentAnswer
  #ch347 0xc0d3zzz
  if studentAnswer == "x":
    gScore += 100
    print "BOOM! FREE LUNCH! Score = %u" % gScore
    return

  if int(studentAnswer,answerRadix) == int(correctAnswer):
    gScore += 100
    print "Correct! Score = %u" % gScore
    gWinningStreak += 1
  else:
    gScore -= 200
    gWinningStreak = 0
    if answerRadix == 16:
      print "Incorrect. The answer was %x\n Score = %u" % (correctAnswer, gScore)
    elif answerRadix == 10:
      print "Incorrect. The answer was %u\n Score = %u" % (correctAnswer, gScore)

def CheckAnswerString(studentAnswer, correctAnswer):
  global gScore
  global gNextLevelRequiredScore
  global gWinningStreak

  #ch347 0xc0d3zzz
  if studentAnswer == "s":
    gScore = gNextLevelRequiredScore
    print "~tweeEEtle deeEEtle deeEEt~ W4Rp W4zzL3 4 5h4zzl3!"
    return

  #ch347 0xc0d3zzz
  if studentAnswer == "x":
    gScore += 100
    print "BOOM! FREE LUNCH! Score = %u" % gScore
    return

  if studentAnswer == correctAnswer:
    gScore += 100
    gWinningStreak += 1
    print "Correct! Score = %u" % gScore
  else:
    gScore -= 200
    gWinningStreak = 0
    print "Incorrect. The answer was '%s'\n Score = %u" % (correctAnswer, gScore)
