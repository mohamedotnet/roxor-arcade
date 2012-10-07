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
#Like it says, score to get out of the level. Is a global so the cheat code can help skip levels
gNextLevelRequiredScore = 0
#Used to unlock RoundX! Need to have gWinningStreak >= 100
gWinningStreak = 0
#used to print how long the player has been playing
#and also to write a log of their scores for later graphing and analysis
gAbsoluteStartTime = 0
#Used to help identify what session a given log was from, 
#so that for instance someone can try to race their own score
gStartingSeed = 0

def LogResults():
  print os.getcwd()
  f = open('../BasicLogile.csv', 'a+')
  tmp = "%u,%u,%u\n" % (gStartingSeed, (int(time()) - gAbsoluteStartTime), gScore)
  f.write(tmp)
  

def CheckAnswerNum(studentAnswer, correctAnswer):
  global gScore
  global gNextLevelRequiredScore
  global gWinningStreak

  #ch347 0xc0d3zzz
  if studentAnswer == "s":
    gScore = gNextLevelRequiredScore
    print "gscore = %u" % gScore
    LogResults()
    print "~tweeEEtle deeEEtle deeEEt~ W4Rp W1zzL3 4 5h1zzl3!"
    return

  #print studentAnswer
  #ch347 0xc0d3zzz
  if studentAnswer == "x":
    gScore += 100
    print "BOOM! FREE LUNCH! Score = %u" % gScore
    LogResults()
    return

  try:
    if int(studentAnswer,16) == int(correctAnswer):
      gScore += 100
      print "Correct! Score = %u" % gScore
      LogResults()
      gWinningStreak += 1
      return
  except ValueError:
    #silently continue
    pass

  try:
    if int(studentAnswer,10) == int(correctAnswer):
      gScore += 100
      print "Correct! Score = %u" % gScore
      LogResults()
      gWinningStreak += 1
      return
  except ValueError:
    #silently continue
    pass

  gScore -= 200
  LogResults()
  gWinningStreak = 0
  print "Incorrect. The answer was 0x%x (decimal %u)\n Score = %u" % (correctAnswer, correctAnswer, gScore)

def CheckAnswerString(studentAnswer, correctAnswer):
  global gScore
  global gNextLevelRequiredScore
  global gWinningStreak

  #ch347 0xc0d3zzz
  if studentAnswer == "s":
    gScore = gNextLevelRequiredScore
    LogResults()
    print "~tweeEEtle deeEEtle deeEEt~ W4Rp W4zzL3 4 5h4zzl3!"
    return

  #ch347 0xc0d3zzz
  if studentAnswer == "x":
    gScore += 100
    LogResults()
    print "BOOM! FREE LUNCH! Score = %u" % gScore
    return

  if studentAnswer.lower() == correctAnswer.lower():
    gScore += 100
    LogResults()
    gWinningStreak += 1
    print "Correct! Score = %u" % gScore
  else:
    gScore -= 200
    LogResults()
    gWinningStreak = 0
    print "Incorrect. The answer was '%s'\n Score = %u" % (correctAnswer, gScore)

#Randomizes the existing section names, but doesn't add new sections for instance
def RandomizeSectionNames(pe):
  pickedIndices = []
  randomSectionNames = [".xeno", "xeno", ".kovah", "kovah", 
                        ".chunky", ".junky", ".funky", ".punky", ".spunky", ".skunky", ".monkey",
                        ".fee", ".fi", ".fo", ".fum",
                        ".t3x7", ".d474", ".rDaT4",".r310c",".p4g3", ".1337",
                        ".spam",".tram",".glam",".wham",".blam",".slam",".tram",".fam",".jam",".cam",".ma'am",
                         "she", "sells", "seashells", "by_the", "seashore",
                         "<-ereht", "<-si", "<-on", "<-noops",
                         ".domo",".arigato", ".mister", ".roboto"]
  
  #We want a new name for each section
  for section in pe.sections:
    #and we're going to keep trying until we find one
    x = random.randint(0,len(randomSectionNames)-1)
    #But make sure we don't pick the same name twice.
    #While it's possible to have two sections with the same name, that would
    #lead to ambiguous answers in this case
    while x in pickedIndices:
      x = random.randint(0,len(randomSectionNames)-1)
    pickedIndices.append(x)
    section.Name = randomSectionNames[x]

#Requires there to already be a file in ../exports with
#entries of the form "RVA exportName" one per line
def GetExportsByName(dllName):
  fileName = "../exports/" + dllName
  with open(fileName, 'r') as f:
    lines = f.read().splitlines()
  exportNames = []
  for line in lines:
    exportNames.append(line.split()[1])
  return exportNames