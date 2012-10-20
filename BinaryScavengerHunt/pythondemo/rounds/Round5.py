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
from rounds.helpers import CheckAnswerNum, CheckAnswerString, GetExportsByName
import rounds.helpers

#This function asks questions about the IMAGE_OPTIONAL_HEADER.DataDirectory entries
#that pertain to bound and delay load imports
def R5Q0(questionCounter):
  #NOTE: if you update the number of questions in this function, you need to update the boundaries in StartR5
  Qs = ["What is the value of IMAGE_OPTIONAL_HEADER.DataDirectory[IMAGE_DIRECTORY_ENTRY_BOUND_IMPORT].RVA?",
        "What is the RVA that points at the bound import directory table?",
        "What is the value of IMAGE_OPTIONAL_HEADER.DataDirectory[IMAGE_DIRECTORY_ENTRY_BOUND_IMPORT].Size?",
        "What is the size of the bound import directory table?",
        "What is the value of IMAGE_OPTIONAL_HEADER.DataDirectory[IMAGE_DIRECTORY_ENTRY_DELAY_IMPORT].RVA?",
        "What is the RVA that points directly at the delay-load Import Address Table (IAT)?",
        "What is the value of IMAGE_OPTIONAL_HEADER.DataDirectory[IMAGE_DIRECTORY_ENTRY_DELAY_IMPORT].Size?",
        "What is the total size of the delay-load Import Address Table (IAT)?"]
  #NOTE: if you update the number of questions in this function, you need to update the boundaries in StartR5

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

  #TODO: want to be able to randomize entries/size of delay load IAT

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

#drilling down on the bound imports
#Here's what I like about this question set:
#peview doesn't currently support analyzing 64 bit binaries very well
#and CFF Explorer doesn't seem to expose the bound import directory table
#So when you randomly get a 64 bit binary here, you have to go to the relevant RVA
#and just start interpreting and inferring the results based on knowledge of the 
#structure definition, as provided at the start of the section in the LoB class
def R5Q1(questionCounter):
  #NOTE: if you update the number of questions in this function, you need to update the boundaries in StartR5
  Qs = ["How many IMAGE_BOUND_IMPORT_DESCRIPTOR structures are in the bound import directory table (excluding the null entry)?",
        "How many DLLs are referenced by the bound import directory table?",
        "What is the value of IMAGE_BOUND_IMPORT_DESCRIPTOR.OffsetModuleName for %s?",
        "How far is it from the start of the bound import directory table to the string for %s?",
        "What is the value of IMAGE_BOUND_IMPORT_DESCRIPTOR.TimeDateStamp for %s?",
        "For the %s that bound imports were bound against, what year was it compiled?"]
  #NOTE: if you update the number of questions in this function, you need to update the boundaries in StartR5

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

  #TODO: want to be able to randomize entries/size of delay load IAT

  #write out the (actually un)modified file
  outFileName = "Round5Q" + str(questionCounter) + suffix
  pe.write(outFileName)
  
  #pick a random bound import entry
  entry = pe.DIRECTORY_ENTRY_BOUND_IMPORT[random.randint(0, len(pe.DIRECTORY_ENTRY_BOUND_IMPORT)-1)]
  #Print the question
  q = random.randint(0,len(Qs)-1)
  if q <= 1:
    interpolatedQuestion = Qs[q]
  else:
    interpolatedQuestion = Qs[q] % entry.name
  
  print "For binary R5Bins/%s..." % outFileName
  print interpolatedQuestion
  answer = raw_input("Answer: ")

  if q == 0 or q == 1:
    CheckAnswerNum(answer,len(pe.DIRECTORY_ENTRY_BOUND_IMPORT))
  elif q == 2 or q == 3:
    CheckAnswerNum(answer,entry.struct.OffsetModuleName)
  elif q == 4:
    CheckAnswerNum(answer,entry.struct.TimeDateStamp)
  elif q == 5:
    binaryYear = 1970 + int(entry.struct.TimeDateStamp / 31556926)
    CheckAnswerNum(answer,binaryYear)
 
#drilling down on the delayed imports
#NOTE: The delay load imports this creates can never *actually* be called, since
#we do not have the necessary dynamic loading stub code in our templates
#However in the future if I make a template that has some legit, delay load entries
#then we could make the others work by reusing that code
def R5Q2(questionCounter):
  #NOTE: if you update the number of questions in this function, you need to update the boundaries in StartR5
  Qs = ["How many ImgDelayDescr structures are in the delayed import directory table (excluding the null entry)?",
        "How many DLLs are referenced by the delay import directory table?",
        "What is the RVA of the delayed IAT for %s?",
        "What is the VA of the delayed IAT for %s?",
        "What is the RVA of the delayed INT for %s?",
        "What is the VA of the delayed INT for %s?"]
  #NOTE: if you update the number of questions in this function, you need to update the boundaries in StartR5

  possibleDLLNames = ["ADVAPI32.dll", "GDI32.dll", "SHELL32.dll", "NTDLL.dll", 
                      "COMCTL32.dll", "MSI.dll", "OLE32.dll", "MSVCRT.dll", 
                      "SETUPAPI.dll", "CRYPT32.dll", "SECUR32.dll", "IMAGEHLP.dll"]

  x = random.randint(0,1) #FIXME: change back to 0,3 when 64 bit delay load stuff is working
  if x == 0:
    pe = pefile.PE('../template32-bound.exe')
    suffix = ".exe"
  elif x == 1:
    pe = pefile.PE('../template32-bound.dll')
    suffix = ".dll"
  elif x == 2:
    pe = pefile.PE('../template64-bound.exe')
    suffix = ".exe"
  else:
    pe = pefile.PE('../template64-bound.dll')
    suffix = ".dll"
    
  outFileName = "Round5Q" + str(questionCounter) + suffix
  
  numDelayLoadEntries = random.randint(1,4)
  i = 0
  randomDllList = []
  randomFunctionsList = []
  while i < numDelayLoadEntries:
    #meh, don't care if we get duplicates for now
    randomDllList.append(possibleDLLNames[random.randint(0,len(possibleDLLNames)-1)])
    randomFunctionsList += [[]]
    randomFunctionsList[i] += GetExportsByName(randomDllList[i]);
    i+=1
  
  #This will create a new section, ".dload", with a bunch of fake entries for delay load imports
  pe.CreateDelayLoadEntries(randomDllList, randomFunctionsList, outFileName)
  #reopen so we can pick a random delay load entry
  pe = pefile.PE(outFileName)

  #select random existing DLL being imported from
  entry = pe.DIRECTORY_ENTRY_DELAY_IMPORT[random.randint(0, len(pe.DIRECTORY_ENTRY_DELAY_IMPORT)-1)]

  #Print the question
  q = random.randint(0,len(Qs)-1)
  if q <= 1:
    interpolatedQuestion = Qs[q]
  else:
    interpolatedQuestion = Qs[q] % entry.dll
  
  print "For binary R5Bins/%s..." % outFileName
  print interpolatedQuestion
  answer = raw_input("Answer: ")
  
  if q == 0 or q == 1:
    CheckAnswerNum(answer,len(pe.DIRECTORY_ENTRY_DELAY_IMPORT))
  if q == 2:
    CheckAnswerNum(answer,entry.struct.pIAT)
  if q == 3:
    CheckAnswerNum(answer,pe.OPTIONAL_HEADER.ImageBase + entry.struct.pIAT)
  if q == 4:
    CheckAnswerNum(answer,entry.struct.pINT)
  if q == 5:
    CheckAnswerNum(answer,pe.OPTIONAL_HEADER.ImageBase + entry.struct.pINT)
    
#misc questions
def R5Q3(questionCounter):
  #NOTE: if you update the number of questions in this function, you need to update the boundaries in StartR5
  Qs = ["Is this binary using \"normal\" or \"bound\" imports?",
        "How many IMAGE_BOUND_FORWARDER_REF structures are in the bound import directory table?"]
  #NOTE: if you update the number of questions in this function, you need to update the boundaries in StartR5

  totalBoundRefs = 0

  q = random.randint(0,len(Qs)-1)

  if q == 0:
    x = random.randint(0,7)
  else:
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
  elif x == 3:
    pe = pefile.PE('../template64-bound.dll')
    suffix = ".dll"
  elif x == 4:
    pe = pefile.PE('../template32.exe')
    suffix = ".exe"
  elif x == 5:
    pe = pefile.PE('../template64.exe')
    suffix = ".exe"
  elif x == 6:
    pe = pefile.PE('../template32.dll')
    suffix = ".dll"
  else:
    pe = pefile.PE('../template64.dll')
    suffix = ".dll"
  if x <= 3:
    importType = "bound"
    for entry in pe.DIRECTORY_ENTRY_BOUND_IMPORT:
      totalBoundRefs += len(entry.entries)
  else:
    importType = "normal"

  #TODO: want to be able to randomize entries/size of delay load IAT

  #write out the (actually un)modified file
  outFileName = "Round5Q" + str(questionCounter) + suffix
  pe.write(outFileName)
  
  #Print the question
  print "For binary R5Bins/%s..." % outFileName
  print Qs[q]
  answer = raw_input("Answer: ")

  if q == 0:
    CheckAnswerString(answer,importType)
  elif q == 1:
    CheckAnswerNum(answer,totalBoundRefs)


def StartR5(seed, suppressRoundBanner, escapeScore):
  global gScore
  global gNextLevelRequiredScore
  if not suppressRoundBanner:
    print "================================================================================"
    print "Welcome to Round 5:"
    print "This round is all about \"bound\" imports and delay-loaded imports"
    print "\nRound terminology note:"
    print "RVA = Relative Virtual Address (relative to image base)."
    print "VA = Absolute Virtual Address (base + RVA)"
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
    x = random.randint(0,14)
    if x <= 3:
      R5Q0(questionCounter)
    elif x <= 7:
      R5Q1(questionCounter)
    elif x <= 12:
      R5Q2(questionCounter)
    elif x <= 14:
      R5Q3(questionCounter)
      
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