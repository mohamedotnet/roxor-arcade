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

#This function asks questions about the IMAGE_EXPORT_DIRECTORY structure
def R6Q0(questionCounter):
  #NOTE: if you update the number of questions in this function, you need to update the boundaries in StartR6
  Qs = ["What is the value of IMAGE_EXPORT_DIRECTORY.Base?",
        "What value should be subtracted from an ordinal to get its index into the AddressOfFunctions array?",
        "What is the value of IMAGE_EXPORT_DIRECTORY.NumberOfFunctions?",
        "How many functions does this binary export?",
        "What is the value of IMAGE_EXPORT_DIRECTORY.NumberOfNames?",
        "How many functions does this binary export by name?",
        "How many functions does this binary export by ordinal?",
        "Is NumberOfNames == NumberOfFunctions? (Y or N)",
        "What is the value of IMAGE_EXPORT_DIRECTORY.AddressOfFunctions?",
        "What is the RVA to the Export Address Table (EAT)?",
        "What is the VA to the Export Address Table (EAT)?",
        "What is the value of IMAGE_EXPORT_DIRECTORY.AddressOfNames?",
        "What is the RVA of the Export Names Table (ENT)?",
        "What is the VA of the Export Names Table (ENT)?",
        "What is the value of IMAGE_EXPORT_DIRECTORY.AddressOfNameOrdinals?",
        "What is the value of IMAGE_EXPORT_DIRECTORY.TimeDateStamp?",
        "According to the exports information, what year was this binary compiled?",
        "Does the exports' TimeDateStamp match the File Header TimeDateStamp? (Y or N)",
        "Is the exports' TimeDateStamp what's checked against when the loader is checking if bound imports still have correct VAs? (Y or N)",
        "Is the File Header's TimeDateStamp what's checked against when the loader is checking if bound imports still have correct VAs? (Y or N)",
        "Which of the following points at the Export Address Table (EAT): AddressOfFunctions, AddressOfNames, or AddressOfNameOrdinals?",
        "Which of the following points at the Export Names Table (ENT): AddressOfFunctions, AddressOfNames, or AddressOfNameOrdinals?",
        ]
  #NOTE: if you update the number of questions in this function, you need to update the boundaries in StartR6

  x = random.randint(2,3)
#  if x == 0:
#    pe = pefile.PE('../template32-bound.exe')
#    suffix = ".exe"
#  elif x == 1:
#    pe = pefile.PE('../template64-bound.exe')
#    suffix = ".exe"
  if x == 2:
    pe = pefile.PE('../template32-bound.dll')
    suffix = ".dll"
  else:
    pe = pefile.PE('../template64-bound.dll')
    suffix = ".dll"

  #TODO: want to be able to randomize entries/size of delay load IAT

  #FIXME: what's the more graceful way of doing this?
  error = 1
  while error:
    try:
      #write out the (actually un)modified file
      outFileName = "Round6Q" + str(questionCounter) + suffix
      pe.write(outFileName)
      error = 0
    except IOError:
      questionCounter+=1
  
  #Print the question
  q = random.randint(0,len(Qs)-1)
  print "For binary R6Bins/%s..." % outFileName
  print Qs[q]
  answer = raw_input("Answer: ")

  if q == 0 or q == 1:
    CheckAnswerNum(answer,pe.DIRECTORY_ENTRY_EXPORT.struct.Base)
  elif q == 2 or q == 3:
    CheckAnswerNum(answer,pe.DIRECTORY_ENTRY_EXPORT.struct.NumberOfFunctions)
  elif q == 4 or q == 5:
    CheckAnswerNum(answer,pe.DIRECTORY_ENTRY_EXPORT.struct.NumberOfNames)
  elif q == 6:
    CheckAnswerNum(answer,pe.DIRECTORY_ENTRY_EXPORT.struct.NumberOfFunctions - pe.DIRECTORY_ENTRY_EXPORT.struct.NumberOfNames)
  elif q == 7:
    if pe.DIRECTORY_ENTRY_EXPORT.struct.NumberOfFunctions == pe.DIRECTORY_ENTRY_EXPORT.struct.NumberOfNames:
      CheckAnswerString(answer,"Y")
    else:
      CheckAnswerString(answer,"N")
  elif q == 8 or q == 9:
    CheckAnswerNum(answer,pe.DIRECTORY_ENTRY_EXPORT.struct.AddressOfFunctions)    
  elif q == 10:
    CheckAnswerNum(answer,pe.OPTIONAL_HEADER.ImageBase + pe.DIRECTORY_ENTRY_EXPORT.struct.AddressOfFunctions)
  elif q == 11 or q == 12:
    CheckAnswerNum(answer,pe.DIRECTORY_ENTRY_EXPORT.struct.AddressOfNames)
  elif q == 13:
    CheckAnswerNum(answer,pe.OPTIONAL_HEADER.ImageBase + pe.DIRECTORY_ENTRY_EXPORT.struct.AddressOfNames)
  elif q == 14:
    CheckAnswerNum(answer,pe.DIRECTORY_ENTRY_EXPORT.struct.AddressOfNameOrdinals)
  elif q == 15:
    CheckAnswerNum(answer,pe.DIRECTORY_ENTRY_EXPORT.struct.TimeDateStamp)
  elif q == 16:
    exportYear = 1970 + int(pe.DIRECTORY_ENTRY_EXPORT.struct.TimeDateStamp / 31556926)
    CheckAnswerNum(answer, exportYear)
  elif q == 17:
    #50% chance to randomize file header timedatestamp
    if random.randint(0,1):
      pe.FILE_HEADER.TimeDateStamp = random.randint(0,4294967296)
    if pe.DIRECTORY_ENTRY_EXPORT.struct.TimeDateStamp == pe.FILE_HEADER.TimeDateStamp:
      CheckAnswerString(answer,"Y")
    else:
      CheckAnswerString(answer,"N")
  elif q == 18:
    CheckAnswerString(answer,"Y")
  elif q == 19:
    CheckAnswerString(answer,"N")
  elif q == 20:
    CheckAnswerString(answer,"AddressOfFunctions")
  elif q == 21:
    CheckAnswerString(answer,"AddressOfNames")

#Question about R/VA of randomly chosen randomly added export
def R6Q1(questionCounter):
  #NOTE: if you update the number of questions in this function, you need to update the boundaries in StartR6
  Qs = ["What is the RVA of %s",
        "What is the ordinal of %s"]
  #NOTE: if you update the number of questions in this function, you need to update the boundaries in StartR6

  #Randomly chosen function names which will point at faux funcs
  funcs = ["FunkyTown", "Func-yTown", "Karate", "Jujitsu", "TaeKwonDo", "DorKwonDo", "Judo", "Kickboxing",
           "DeleteHD", "PwnSauce", "JumpTheShark", "WakeUpNeo", "TheMatrixHasYou", "FollowTheWhiteRabbit", "KnockKnock",
           "Pro-rate", "Intimidate", "Inculcate", "Obviate", "Instantiate", "Devastate", "Infiltrate", "Obliviate", "Annihilate", "Eradicate", "KILLKILLKILL",
           "CheepSaram", "HousePersonLOL", "WonSoongEe", "EeShimNiDa", "Naaaay", "ChaDongCha", "NengJangGo", "PeeHenGee",
           "Add", "Sub", "Mul", "Div", "Mod", "AND", "OR", "XOR", "NOR", "NAND", 
           "MakeMountainFromMolehill", "LookGiftHorseInTheMouth", "BurnCandleAtBothEnds", "SqeezeCharmin", "CountChickensBeforeTheyreHatched",
           "PlayWithFood", "CryOverSpilledMilk", "VoteWolverine", "VoteLobo",
           "BeginPhase2", "OpenThePortal", "GetAngry", "GetEven", "GetOdd", "GetShorty", "GetBusy", "GetGone"]


  x = random.randint(0,0)
  if x == 0:
    pe = pefile.PE('../template32-bound.dll')
    suffix = ".dll"
  elif x == 1:
    pe = pefile.PE('../template32-bound.exe')
    suffix = ".exe"
#  if x == 2:
#    pe = pefile.PE('../template64-bound.exe')
#    suffix = ".exe"
#  else:
#    pe = pefile.PE('../template64-bound.dll')
#    suffix = ".dll"

  #FIXME: what's the more graceful way of doing this?
  error = 1
  while error:
    try:
      outFileName = "Round6Q" + str(questionCounter) + suffix
      pe.x_CreateExports(5, funcs, outFileName)
      pe = pefile.PE(outFileName)
      error = 0
    except IOError:
      questionCounter+=1


  #pick a random export to ask questions about
  randomOrdinal = random.randint(0,len(pe.DIRECTORY_ENTRY_EXPORT.symbols)-1)
  randomExport = pe.DIRECTORY_ENTRY_EXPORT.symbols[randomOrdinal]
  
  q = random.randint(0,len(Qs)-1)
  print "For binary R6Bins/%s..." % outFileName
  print Qs[q] % randomExport.name
  
  answer = raw_input("Answer: ")
  
  if q == 0:
    CheckAnswerNum(answer, randomExport.address)
  elif q == 1:
    CheckAnswerNum(answer, randomOrdinal)
    
#Question about export by ordinal

#Question about forwarded exports

#TODO: Now that we've covered exports
#add a question about VA of a given import
#note: this seems like it will require either including the binaries
#or just making up a presumed base address and then pointing them
#at the ../exports/ files

def StartR6(seed, suppressRoundBanner, escapeScore):
  global gScore
  global gNextLevelRequiredScore
  if not suppressRoundBanner:
    print "================================================================================"
    print "Welcome to Round 6:"
    print "This round covers the function \"exports\" typically found in DLLs"
    print "\nRound terminology note:"
    print "RVA = Relative Virtual Address (relative to image base)."
    print "VA = Absolute Virtual Address (base + RVA)"
    print "================================================================================\n"
  #making a directory that the files go into, just to keep things tidier
  try:
    os.mkdir("R6Bins")
  except OSError:
    pass
  os.chdir("R6Bins")
  filelist = [ f for f in os.listdir(".")]
  for f in filelist:
    try:
      os.remove(f)
    except OSError:
      pass
  roundStartTime = int(time())
  rounds.helpers.gNextLevelRequiredScore = escapeScore
  random.seed(seed)
  questionCounter = 0;
  while rounds.helpers.gScore < rounds.helpers.gNextLevelRequiredScore:
    #Now changed it so that a given R*Q* only has as many chances to be called
    #as it has calls to CheckAnswer*. This way the number of variant ways
    #to ask the question doesn't increase the probability of the question being asked
    #NOTE: if you update the number of questions in the round, you need to update these boundaries
    x = random.randint(0,18)
    if x <= 16:
      R6Q0(questionCounter)
    elif x <= 18:
      R6Q1(questionCounter)
#    elif x <= 12:
#      R6Q2(questionCounter)
#    elif x <= 14:
#      R6Q3(questionCounter)
      
    questionCounter+=1

  if not suppressRoundBanner:
    currentTime = int(time())
    roundTime = currentTime - roundStartTime
    roundMinutes = roundTime / 60
    roundSeconds = roundTime % 60
    totalElapsedTime = currentTime - rounds.helpers.gAbsoluteStartTime
    print "\nCongratulations, you passed round 6!"
    print "It took you %u minutes, %u seconds for this round." % (roundMinutes, roundSeconds)
    totalMinutes = totalElapsedTime / 60
    totalSeconds = totalElapsedTime % 60
    print "And so far it's taken you a total time of %u minutes, %u seconds." % (totalMinutes, totalSeconds) 

  os.chdir("..")

