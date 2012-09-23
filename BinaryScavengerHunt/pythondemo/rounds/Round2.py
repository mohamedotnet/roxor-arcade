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

#This is Round 2 and will cover questions on the IMAGE_NT_HEADERS.IMAGE_OPTIONAL_HEADER
#but it will exclude the data directory portion of the optional header
#because we will cover each portion of that independently

import os
import random
import pefile
from time import time
from rounds.helpers import CheckAnswerNum, CheckAnswerString
import rounds.helpers

#This function asks questions about the IMAGE_OPTIONAL_HEADER.Magic
def R2Q0(questionCounter):
  Qs = ["What is the IMAGE_OPTIONAL_HEADER.Magic in hex?: ",
  "What value, in hex, of the optional header 'Magic' field indicates a 32 bit (PE32) binary?: ",
  "According to the IMAGE_OPTIONAL_HEADER.Magic, is this a 32 bit (PE32) binary? (Y or N): ",
  "What value, in hex, of the optional header 'Magic' field indicates a 64 bit (PE32+) binary?: ",
  "According to the IMAGE_OPTIONAL_HEADER.Magic, is this a 64 bit (PE32+) binary? (Y or N): "]

  #For simplicity, rather than trying to go through the rigamarole of
  #changing the optional header, we just randomly pick whether we open
  #a 32 or 64 bit template 
  x = random.randint(0,1)
  if x == 0:
    pe = pefile.PE('template32.exe')
    is32 = "Y"
    is64= "N"
  else:
    pe = pefile.PE('template64.exe')
    is32 = "N"
    is64= "Y"

  #write out the (actually un)modified file
  outFileName = "Round2Q" + str(questionCounter) + ".exe"
  pe.write(filename=outFileName)

  #Print the question
  q = random.randint(0,4)
#  if q == 0:
#    print "answer = %x" % pe.OPTIONAL_HEADER.Magic
#  elif q == 1:
#    print "answer = %x" % 0x010B
#  elif q == 2:
#    print "answer = %s" % is32
#  elif q == 3:
#    print "answer = %x" % 0x020B  
#  elif q == 4:
#    print "answer = %s" % is64
  
  print "For binary %s..." % outFileName
  answer = raw_input(Qs[q])

  if q == 0:
    CheckAnswerNum(answer,16,pe.OPTIONAL_HEADER.Magic) 
  elif q == 1:
    CheckAnswerNum(answer,16,0x010B) 
  elif q == 2:
    CheckAnswerString(answer,is32)
  elif q == 3:
    CheckAnswerNum(answer,16,0x020B)  
  elif q == 4:
    CheckAnswerString(answer,is64)

#This function asks questions about the IMAGE_OPTIONAL_HEADER.AddressOfEntryPoint
def R2Q1(questionCounter):
  Qs = ["What is the value of IMAGE_OPTIONAL_HEADER.AddressOfEntryPoint?: ",
  "What is the RVA of the first code which executes in this binary?: ",
  "What is the AVA of the first code which executes in this binary?: "]

  if random.randint(0,1) == 0:
    pe = pefile.PE('template32.exe')
  else:
    pe = pefile.PE('template64.exe')

  #TODO: randomize this a bit (just want to get the basics of the question for now)

  #write out the (actually un)modified file
  outFileName = "Round2Q" + str(questionCounter) + ".exe"
  pe.write(filename=outFileName)

  #Print the question
  q = random.randint(0,2)
#  if q == 0 or q == 1:
#    print "answer = %x" % pe.OPTIONAL_HEADER.AddressOfEntryPoint
#  elif q == 2:
#    print "answer = %x" % (pe.OPTIONAL_HEADER.AddressOfEntryPoint + pe.OPTIONAL_HEADER.ImageBase)
  print "For binary %s..." % outFileName
  answer = raw_input(Qs[q])

  if q == 0 or q == 1:
    CheckAnswerNum(answer,16,pe.OPTIONAL_HEADER.AddressOfEntryPoint) 
  elif q == 2:
    CheckAnswerNum(answer,16,pe.OPTIONAL_HEADER.AddressOfEntryPoint + pe.OPTIONAL_HEADER.ImageBase) 

#This function asks questions about the IMAGE_OPTIONAL_HEADER.ImageBase
def R2Q2(questionCounter):
  Qs = ["What is the value of IMAGE_OPTIONAL_HEADER.ImageBase?: ",
  "What is the preferred AVA this binary would like to be loaded into memory at?: "]

  if random.randint(0,1) == 0:
    pe = pefile.PE('template32.exe')
  else:
    pe = pefile.PE('template64.exe')

  #TODO: randomize, but...
  #If we're going to rebase it, we have to fix up all the relocations
  #Since if the loader loads it at that address it won't use them

  #write out the modified file
  outFileName = "Round2Q" + str(questionCounter) + ".exe"
  pe.write(filename=outFileName)

  #Print the question
  q = random.randint(0,1)
#  print "answer = %x" % pe.OPTIONAL_HEADER.ImageBase
  print "For binary %s..." % outFileName
  answer = raw_input(Qs[q])

  if q == 0 or q == 1:
    CheckAnswerNum(answer,16,pe.OPTIONAL_HEADER.ImageBase) 

#This function asks questions about the IMAGE_OPTIONAL_HEADER.SizeOfImage
def R2Q3(questionCounter):
  Qs = ["What is the value of IMAGE_OPTIONAL_HEADER.SizeOfImage?: ",
  "What is the total amount of memory this binary will reserve in memory?: "]

  #Just reusing the capability from R1Q4
  randomSectionNames = [".xeno", "xeno", ".kovah", "kovah", 
                        ".foo", ".bar", ".baz", "foobar", "foofus",
                        "ONCE", "A_JOLLY", "SWAGMAN", "CAMPED",
                        "BY_A", "BILABONG", "UNDER", 
                        "THE", "SHADE", "OF_A", "COOLIBAH", "TREE...",
                         "AND_THEN", "A", "BASALISK", "GOT_HIM!"
                         "<-eht", "<-taehc", "<-edoc", "<-si", "<-s"]

  if random.randint(0,1) == 0:
    pe = pefile.PE('template32.exe')
  else:
    pe = pefile.PE('template64.exe')
  outFileName = "Round2Q" + str(questionCounter) + ".exe"

  #Created new function to insert random sections and write the file out
  numExtraSections = random.randint(1,5)
  totalNumSections = pe.FILE_HEADER.NumberOfSections + numExtraSections 
  #Since we haven't actually modified pe.FILE_HEADER.NumberOfSections in the binary yet
  #this function will know whether to add new sections based on whether the first param
  #is greater than the existing header or not
  pe.modifySectionsAndWrite(totalNumSections, randomSectionNames, outFileName)

  #Print the question
  q = random.randint(0,1)
#  print "answer = %x" % pe.OPTIONAL_HEADER.SizeOfImage
  print "For binary %s..." % outFileName
  answer = raw_input(Qs[q])

  if q == 0 or q == 1:
    CheckAnswerNum(answer,16,pe.OPTIONAL_HEADER.SizeOfImage)

#This function asks questions about the IMAGE_OPTIONAL_HEADER.SectionAlignment & FileAlignment
def R2Q4(questionCounter):
  Qs = ["What is the value of IMAGE_OPTIONAL_HEADER.FileAlignment?: ",
  "What are the alignment sizes needed to align section data in the file?: ",
  "What is the value of IMAGE_OPTIONAL_HEADER.SectionAlignment?: ",
  "What are the alignment sizes needed to align section information in memory?: ",]

  if random.randint(0,1) == 0:
    pe = pefile.PE('template32.exe')
  else:
    pe = pefile.PE('template64.exe')

  #TODO: randomize this a bit (just want to get the basics of the question for now)

  #write out the (actually un)modified file
  outFileName = "Round2Q" + str(questionCounter) + ".exe"
  pe.write(filename=outFileName)

  #Print the question
  q = random.randint(0,3)
#  if q == 0 or q == 1:
#    print "answer = %x" % pe.OPTIONAL_HEADER.FileAlignment
#  if q == 2 or q == 3:
#    print "answer = %x" % pe.OPTIONAL_HEADER.SectionAlignment
  print "For binary %s..." % outFileName
  answer = raw_input(Qs[q])

  if q == 0 or q == 1:
    CheckAnswerNum(answer,16,pe.OPTIONAL_HEADER.FileAlignment)
  if q == 2 or q == 3:
    CheckAnswerNum(answer,16,pe.OPTIONAL_HEADER.SectionAlignment)

#This function asks questions about the IMAGE_OPTIONAL_HEADER.DllCharacteristics flags
def R2Q5(questionCounter):
  Qs = ["What is the value of IMAGE_OPTIONAL_HEADER.DLLCharacteristics?: ",
  "Is IMAGE_DLL_CHARACTERISTICS_DYNAMIC_BASE set? (Y or N): ",
  "Does this binary support ASLR? (Y or N): ",
  "Is IMAGE_DLL_CHARACTERISTICS_NX_COMPAT set? (Y or N): ",
  "Does this binary support hardware DEP? (Y or N): ",
  "Does this binary support non-executable data? (Y or N): ",
  "Is IMAGE_DLL_CHARACTERISTICS_NO_SEH set? (Y or N): ",
  "Does this binary have the flag set for no support for SEH? (Y or N): ",
  "Is IMAGE_DLL_CHARACTERISTICS_TERMINAL_SERVER_AWARE set? (Y or N): ",
  "Does this binary support multiple users in terminal server (i.e. RDP) environments? (Y or N): ",
  "How many flags are set in the IMAGE_OPTIONAL_HEADER.DLLCharacteristics?: "]
#  "Is IMAGE_DLL_CHARACTERISTICS_FORCE_INTEGRITY set? (Y or N): ",
#  "Does this binary require checking its digital signature? (Y or N): ",
#  "Is IMAGE_DLLCHARACTERISTICS_NO_ISOLATION set? (Y or N): ",
#  "Is IMAGE_DLLCHARACTERISTICS_NO_BIND set? (Y or N): ",
#  "Is IMAGE_DLLCHARACTERISTICS_WDM_DRIVER set? (Y or N): ",

  if random.randint(0,1) == 0:
    pe = pefile.PE('template32.exe')
  else:
    pe = pefile.PE('template64.exe')

  numFlagsSet = 0
  if random.randint(0,1) == 1:
    #Found out the hard way just doing something like 
    #"pe.OPTIONAL_HEADER.IMAGE_DLL_CHARACTERISTICS_DYNAMIC_BASE = True" 
    #doesn't effect the file for these characteristics 
    #(unlike the FILE_HEADER.Characteristics)
    pe.OPTIONAL_HEADER.DllCharacteristics |= 0x40
#    print "IMAGE_DLL_CHARACTERISTICS_DYNAMIC_BASE"
    aslrCompat = "Y"
    numFlagsSet += 1
  else:
    pe.OPTIONAL_HEADER.DllCharacteristics &= ~0x40
    aslrCompat = "N"
  if random.randint(0,1) == 1:
    pe.OPTIONAL_HEADER.DllCharacteristics |= 0x100
#    print "IMAGE_DLL_CHARACTERISTICS_NX_COMPAT"
    numFlagsSet += 1
    nxCompat = "Y"
  else:
    pe.OPTIONAL_HEADER.DllCharacteristics &= ~0x100
    nxCompat = "N"
  if random.randint(0,1) == 1:
    pe.OPTIONAL_HEADER.DllCharacteristics |= 0x400
#    print "IMAGE_DLL_CHARACTERISTICS_NO_SEH"
    numFlagsSet += 1
    noSEH = "Y"
  else:
    pe.OPTIONAL_HEADER.DllCharacteristics &= ~0x400
    noSEH = "N"
  if random.randint(0,1) == 1:
    pe.OPTIONAL_HEADER.DllCharacteristics |= 0x8000
#    print "IMAGE_DLL_CHARACTERISTICS_TERMINAL_SERVER_AWARE"
    numFlagsSet += 1
    termSrv = "Y"
  else:
    pe.OPTIONAL_HEADER.DllCharacteristics &= ~0x8000
    termSrv = "N"
  #write out the modified file
  outFileName = "Round2Q" + str(questionCounter) + ".exe"
  pe.write(filename=outFileName)

  #Print the question
  q = random.randint(0,10)
#  print "characteristics = %x" % pe.OPTIONAL_HEADER.DllCharacteristics
#  print "numFlagsSet = %u" % numFlagsSet
  print "For binary %s..." % outFileName
  answer = raw_input(Qs[q])

  if q == 0:
    CheckAnswerNum(answer,16,pe.OPTIONAL_HEADER.DllCharacteristics)
  elif q == 1 or q == 2:
    CheckAnswerString(answer,aslrCompat)
  elif q == 3 or q == 4 or q == 5:
    CheckAnswerString(answer,nxCompat)
  elif q == 6 or q == 7:
    CheckAnswerString(answer,noSEH)
  elif q == 8 or q == 9:
    CheckAnswerString(answer,termSrv)
  elif q == 10:
    CheckAnswerNum(answer,16,numFlagsSet)

def StartR2(seed):
  global gScore
  global gNextLevelRequiredScore
  print "All answers should be given *in hexidecimal* unless otherwise noted."
  print "Round terminology note:"
  print "RVA = Relative Virtual Address (relative to image base)."
  print "AVA = Absolute Virtual Address (base + RVA)"
  startTime = int(time())
  rounds.helpers.gNextLevelRequiredScore = 2000
  random.seed(seed)
  questionCounter = 0;
  while rounds.helpers.gScore < rounds.helpers.gNextLevelRequiredScore:
    q = random.randint(0,5)
    #print "Round rand = %u" % q

    {0:R2Q0,
     1:R2Q1,
     2:R2Q2,
     3:R2Q3,
     4:R2Q4,
     5:R2Q5
     }[q](questionCounter)
    questionCounter+=1

  roundTime = int(time()) - startTime
  roundMinutes = roundTime / 3600
  roundSeconds = roundTime % 3600
  rounds.helpers.gTotalElapsedTime += roundTime
  print "\nCongratulations, you passed round 2!"
  print "It took you %u minutes, %u seconds for this round." % (roundMinutes, roundSeconds)
  totalMinutes = rounds.helpers.gTotalElapsedTime / 3600
  totalSeconds = rounds.helpers.gTotalElapsedTime % 3600
  print "And so far it's taken you a total time of %u minutes, %u seconds." % (totalMinutes, totalSeconds) 
