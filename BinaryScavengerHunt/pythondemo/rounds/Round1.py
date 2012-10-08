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

#This is round 1, which covers questions about the DOS_HEADER
#And the IMAGE_NT_HEADERS.IMAGE_FILE_HEADER


import os
import random
import pefile
from time import time
from rounds.helpers import CheckAnswerNum, CheckAnswerString
import rounds.helpers

#This function asks questions about the IMAGE_DOS_HEADER with hardcoded answers
#thus it requires no PE file changing
def R1Q0(questionCounter):
  Qs = ["What is the IMAGE_DOS_HEADER.e_magic in ASCII?",
	"What is the numeric value of the IMAGE_DOS_HEADER.e_magic?"]

  #Print the question
  q = random.randint(0,len(Qs)-1)

  print Qs[q]
  answer = raw_input("Answer: ")

  if q == 0:
    CheckAnswerString(answer,"MZ")
  else:
    CheckAnswerNum(answer,0x5A4D)


#This function deals with questions about IMAGE_DOS_HEADER.e_lfanew
def R1Q1(questionCounter):
  Qs = ["How far into the binary is the IMAGE_NT_HEADERS structure?",
        "How far into the binary is the structure with the 'PE' signature?",
        "What is the IMAGE_DOS_HEADER.e_lfanew?",
        "What is the offset from the end of the IMAGE_DOS_HEADER to the IMAGE_NT_HEADERS?"]

  #Open the binary and manipulate IMAGE_DOS_HEADER.e_lfanew
  x = random.randint(0,3)
  if x == 0:
    pe = pefile.PE('../template32.exe')
    suffix = ".exe"
  elif x == 1:
    pe = pefile.PE('../template64.exe')
    suffix = ".exe"
  elif x == 2:
    pe = pefile.PE('../template32.dll')
    suffix = ".dll"
  else:
    pe = pefile.PE('../template64.dll')
    suffix = ".dll"

  outFileName = "Round1Q" + str(questionCounter) + suffix

  #pe.write(filename=outFileName)
  #Made a new function in pefile which also writes the file
  #Create a random sized (but less than 0x200) byte list
  bytelist = ['\x41']*4*random.randint(0,128)
  #Insert the byte string wherever the DOS_HEADER.e_lfanew currently says it is
  pe.randomize_NT_HEADER_location(bytelist, pe.DOS_HEADER.e_lfanew, outFileName)

  #Print the question
  q = random.randint(0,len(Qs)-1)

  print "For binary R1Bins/%s..." % outFileName
  print Qs[q]
  answer = raw_input("Answer: ")

  #Check the answer
  if q == 3:
    #When it's question [3] we're actually looking for a difference from the end
    #of the DOS header not just from the beginning of the file
    CheckAnswerNum(answer,(pe.DOS_HEADER.e_lfanew - list(pe.DOS_HEADER.__pack__()).__len__()))
  else:
    CheckAnswerNum(answer,pe.DOS_HEADER.e_lfanew)


#This function deals with questions about FILE_HEADER.TimeDateStamp
def R1Q2(questionCounter):
  Qs = ["What year was this binary compiled according to the TimeDateStamp?",
        "What is the IMAGE_FILE_HEADER's TimeDateStamp?",
        "How many years old is this binary? (round down)"]

  #Open the binary and manipulate FILE_HEADER.TimeDateStamp
  x = random.randint(0,3)
  if x == 0:
    pe = pefile.PE('../template32.exe')
    suffix = ".exe"
  elif x == 1:
    pe = pefile.PE('../template64.exe')
    suffix = ".exe"
  elif x == 2:
    pe = pefile.PE('../template32.dll')
    suffix = ".dll"
  else:
    pe = pefile.PE('../template64.dll')
    suffix = ".dll"

  #pick the random question
  q = random.randint(0,len(Qs)-1)

  currentTime = int(time())
  #If we happen to get the [2]nd question, we need a binary
  #that's older than the current year
  if q == 2:
    pe.FILE_HEADER.TimeDateStamp = random.randint(0,currentTime)
  #otherwise it can just be from whenever
  else:
    pe.FILE_HEADER.TimeDateStamp = random.randint(0,4294967296)

  #print "selected random TimeDateStamp = %u" % pe.FILE_HEADER.TimeDateStamp

  #31556926 seconds per year as far as epoc time is concerned
  #so divide by that many to get the year
  binaryYear = 1970 + int(pe.FILE_HEADER.TimeDateStamp / 31556926)
  #print binaryYear
  currentYear = 1970 + int(currentTime / 31556926)    
 
  #write out the modified file
  outFileName = "Round1Q" + str(questionCounter) + suffix
  pe.write(filename=outFileName)

  #Print the question
  print "For binary R1Bins/%s..." % outFileName
  print Qs[q]
  answer = raw_input("Answer: ")

  if q == 0:
    CheckAnswerNum(answer,binaryYear)
  elif q == 1:
    CheckAnswerNum(answer,pe.FILE_HEADER.TimeDateStamp)
  elif q == 2:
    CheckAnswerNum(answer,int(currentYear - binaryYear))

#This function deals with questions about FILE_HEADER.Machine
def R1Q3(questionCounter):
  Qs = ["Is this a 32 bit or 64 bit binary? (enter 32 or 64)",
        "Is this a PE32 or PE32+ binary? (enter PE32 or PE32+)",
	      "What is the IMAGE_FILE_HEADER.Machine field?",
        "What IMAGE_FILE_HEADER.Machine value indicates a 64 bit binary?",
        "What IMAGE_FILE_HEADER.Machine value indicates a 32 bit binary?"]

  #pick the random question
  q = random.randint(0,len(Qs)-1)

  #For simplicity, rather than trying to go through the rigamarole of
  #changing the optional header, we just randomly pick whether we open
  #a 32 or 64 bit template 
  x = random.randint(0,1)
  if x:
    if random.randint(0,1):
      pe = pefile.PE('../template32.exe')
      suffix = ".exe"
    else:
      pe = pefile.PE('../template32.dll')
      suffix = ".dll"
    binType = 32
    binTypeStr = "PE"
  else:
    if random.randint(0,1):
      pe = pefile.PE('../template64.exe')
      suffix = ".exe"
    else:
      pe = pefile.PE('../template64.dll')
      suffix = ".dll"
    binType = 64
    binTypeStr = "PE+"
  #print "selected %s binary" % binTypeStr
   
  #In the future we might want to make modifications to the template binary in every case
  #but for now I don't think it significantly improves the learning, and it's just extra work ;)
 
  #write out the (actually un)modified file
  outFileName = "Round1Q" + str(questionCounter) + ".exe"
  pe.write(filename=outFileName)

  #Print the question
  print "For binary R1Bins/%s..." % outFileName
  print Qs[q]
  answer = raw_input("Answer: ")

  if q == 0:
    CheckAnswerNum(answer,binType)
  elif q == 1:
    CheckAnswerString(answer,binTypeStr)
  elif q == 2:
    if binType == 32:
      CheckAnswerNum(answer,0x014C)
    else:
      CheckAnswerNum(answer,0x8664)
  elif q == 3:
    CheckAnswerNum(answer,0x8664)
  elif q == 4:
    CheckAnswerNum(answer,0x014C)

#This function deals with questions about FILE_HEADER.NumberOfSections
#But in order to randomize that, it can insert random sections
def R1Q4(questionCounter):
  Qs = ["How many sections does this binary have?",
        "What is the IMAGE_FILE_HEADER.NumberOfSections field?",
        "Does this binary have %u sections? (Y or N)"]

  #to point out that section names don't have to start with a .
  #and to have easter eggs for the student who becomes the reader :P
  randomSectionNames = [".xeno", "xeno", ".kovah", "kovah", 
                        ".foo", ".bar", ".baz", "foobar", "foofus",
                        "UPX0", "UPX1", ".UPX2", "SCREEEE!",
                        "HAHAHA", "FOOLISH", "MORTAL", 
                        "YOU_HAVE", "STEPPED", "INTO_THE",
                        "DEN_OF", "THE...", "BASALISK",
                         "<-eht", "<-taehc", "<-edoc", "<-si", "<-x"]

  #pick the random question
  q = random.randint(0,len(Qs)-1)
  correctNumSections = random.randint(0,1)
  #print "correctNumSections = %u" % correctNumSections

  x = random.randint(0,3)
  if x == 0:
    pe = pefile.PE('../template32.exe')
    suffix = ".exe"
  elif x == 1:
    pe = pefile.PE('../template64.exe')
    suffix = ".exe"
  elif x == 2:
    pe = pefile.PE('../template32.dll')
    suffix = ".dll"
  else:
    pe = pefile.PE('../template64.dll')
    suffix = ".dll"
    
  #write out the modified file
  outFileName = "Round1Q" + str(questionCounter) + suffix
  #pe.write(filename=outFileName)

  #Created new function to insert random sections and write the file out
  numExtraSections = random.randint(1,5)
  #print "numExtraSections = %u" % numExtraSections
  existingNumSections = pe.FILE_HEADER.NumberOfSections
  totalNumSections = existingNumSections + numExtraSections 
  #If it picks 5 there is then a 25% chance you will get rickrolled by the 
  #section names! (5% chance overall) Easter Egg! :D

  #Print the question
  print "For binary R1Bins/%s..." % outFileName
  if q == 2:
    if correctNumSections:
      interpolatedQuestion = Qs[q] % totalNumSections
      correctStr = "Y"
    else:
      interpolatedQuestion = Qs[q] % (totalNumSections + random.randint(1,2))
      correctStr = "N"
  else:
    interpolatedQuestion = Qs[q]

  #Since we haven't actually modified pe.FILE_HEADER.NumberOfSections in the binary yet
  #this function will know whether to add new sections based on whether the first param
  #is greater than the existing header or not
  pe.modifySectionsAndWrite(totalNumSections, randomSectionNames, 1, outFileName)

  #ask question
  print interpolatedQuestion
  answer = raw_input("Answer: ")

  if q == 0 or q == 1:
    CheckAnswerNum(answer,pe.FILE_HEADER.NumberOfSections)
  elif q == 2:
    CheckAnswerString(answer,correctStr)

#This function deals with questions about FILE_HEADER.Characteristics
def R1Q5(questionCounter):
  Qs = ["Is the IMAGE_FILE_EXECUTABLE_IMAGE file header characteristic set? (Y or N)",
        "Is this file a regular executable (.exe)? (Y or N)",
        "Is the IMAGE_FILE_DLL file header characteristic set? (Y or N)",
        "Is this file a dynamic-link library (.dll)? (Y or N)",
        "Is the IMAGE_FILE_LARGE_ADDRESS_AWARE file header characteristic set? (Y or N)",
        "Does this file support being loaded at an address > 2GB? (Y or N)",
        "Is the IMAGE_FILE_32BIT_MACHINE file header characteristic set? (Y or N)",
        "What is the IMAGE_FILE_HEADER.Characteristics field? ",
        "How many characteristics are set in this file's file header?"]#,
#        "According to the file header, is this a 32 or 64 bit binary? (32 or 64)"#Not a good question because it can be set on 64 bit executables just fine
#        "Is this file a .exe/.sys or .dll? (enter exe, sys, or dll)",#lazy, don't want to deal with the response
#        "Is this file an executable or dynamic library? (enter \"executable\" or \"library\")"]#lazy, don't want to deal with the response


  #I am not generating any questions about other characteristics, because the
  #point is not to make it a trivia game, but to reinforce information that I 
  #think is useful:

  #pick the random question
  q = random.randint(0,len(Qs)-1)

  currentTime = int(time())
  #For simplicity, rather than trying to go through the rigamarole of
  #changing the optional header, we just randomly pick whether we open
  #a 32 or 64 bit template
  x = random.randint(0,3)
  if x == 0:
    pe = pefile.PE('../template32.exe')
    binBits = 32
    binTypeStr = "PE"
    isDll = "N"
  elif x == 1:
    pe = pefile.PE('../template64.exe')
    binBits = 64
    binTypeStr = "PE+"
    isDll = "N"
  elif x == 2:
    pe = pefile.PE('../template32.dll')
    binBits = 32
    binTypeStr = "PE"
    isDll = "Y"
  else:
    pe = pefile.PE('../template64.dll')
    binBits = 64
    binTypeStr = "PE+"
    isDll = "Y"
    
  numFlagsSet = 1
  if isDll == "Y":
    numFlagsSet += 1
  #decide whether to twiddle the bits
  #Found out the hard way just doing something like 
  #"pe.FILE_HEADER.IMAGE_FILE_LARGE_ADDRESS_AWARE = True" 
  #doesn't effect the file for these characteristics
  if random.randint(0,1) == 1:
    pe.FILE_HEADER.Characteristics |= 0x20
    isLargeAware = "Y"
    numFlagsSet += 1
  else:
    pe.FILE_HEADER.Characteristics &= ~0x20
    isLargeAware = "N"
  if random.randint(0,1) == 1:
    pe.FILE_HEADER.Characteristics |= 0x100
    is32Characteristics = "Y"
    numFlagsSet += 1
  else:
    pe.FILE_HEADER.Characteristics &= ~0x100
    is32Characteristics = "N"
     
  #write out the modified file
  outFileName = "Round1Q" + str(questionCounter) + ".txt"
  pe.write(filename=outFileName)

  #Print the question
  print "For binary R1Bins/%s..." % outFileName
  print Qs[q]
  answer = raw_input("Answer: ")

  if q == 0 or q == 1:
    CheckAnswerString(answer,"Y")
  elif q == 2 or q == 3:
    CheckAnswerString(answer,isDll)
  elif q == 4 or q == 5:
    CheckAnswerString(answer,isLargeAware)
  elif q == 6:
    CheckAnswerString(answer,is32Characteristics)
  elif q == 7:
    CheckAnswerNum(answer, pe.FILE_HEADER.Characteristics)
  elif q == 8:
    CheckAnswerNum(answer, numFlagsSet)

def StartR1(seed, suppressRoundBanner, escapeScore):
  global gScore
  global gNextLevelRequiredScore
  if not suppressRoundBanner:
    print "================================================================================"
    print "Welcome to Round 1:"
    print "This round is all about the IMAGE_DOS_HEADER (\"DOS Header\"),"
    print "and the IMAGE_NT_HEADER.IMAGE_FILE_HEADER (\"File Header\")"
    print "================================================================================\n"
  #making a directory that the files go into, just to keep things tidier
  try:
    os.mkdir("R1Bins")
  except OSError:
    pass
  os.chdir("R1Bins")
  filelist = [ f for f in os.listdir(".")]
  for f in filelist:
    os.remove(f)
  rounds.helpers.gAbsoluteStartTime = roundStartTime = int(time())
  rounds.helpers.gNextLevelRequiredScore = escapeScore
  random.seed(seed)
  questionCounter = 0;
  while rounds.helpers.gScore < rounds.helpers.gNextLevelRequiredScore:
    #Now changed it so that a given R*Q* only has as many chances to be called
    #as it has calls to CheckAnswer*. This way the number of variant ways
    #to ask the question doesn't increase the probability of the question being asked
    #NOTE: if you update the number of questions in the round, you need to update these boundaries
    x = random.randint(0,18)
    if x <= 1:
      R1Q0(questionCounter)
    elif x <= 3:
      R1Q1(questionCounter)
    elif x <= 6:
      R1Q2(questionCounter)
    elif x <= 10:
      R1Q3(questionCounter)
    elif x <= 12:
      R1Q4(questionCounter)
    elif x <= 18:
      R1Q4(questionCounter)

    questionCounter+=1

  if not suppressRoundBanner:
    roundTime = int(time()) - roundStartTime
    roundMinutes = roundTime / 3600
    roundSeconds = roundTime % 3600
    print "\nCongratulations, you passed round 1! (in %u minutes, %u seconds)\n" % (roundMinutes, roundSeconds)

  os.chdir("..")