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

#This is Round 10 and will cover questions on the load configuration
#and about signed files

import os
import random
import pefile
from time import time
from rounds.helpers import CheckAnswerNum, CheckAnswerString
import rounds.helpers

#Basic questions about the TLS information
def R10Q0(questionCounter):
  #NOTE: if you update the number of questions in this function, you need to update the boundaries in StartR8
  Qs = ["What is the RVA of the load configuration directory?",
        "What is the VA of the load configuration directory?",
        "What is the file offset to the load configuration directory?",
        "What is the RVA of the security cookie used for buffer overflow protection?",
        "What is the RVA of the stack cookie (canary) added when the /GS compile option is used?",
        "What is the VA of the security cookie used for buffer overflow protection?",
        "What is the VA of the stack cookie (canary) added when the /GS compile option is used?",
        "What is the RVA of the structured exception handler table?",
        "What is the RVA of the table used when /SAFESEH linker option is used?",
        "What is the VA of the security cookie used for buffer overflow protection?",
        "What is the VA of the table used when /SAFESEH linker option is used?",
        "How many SEH handlers are available in this binary?"]
  #NOTE: if you update the number of questions in this function, you need to update the boundaries in StartR8

  #TODO: currently I just made one template file that has 5 functions that can possibly be called
  #and the code will just add or subtract pointers in the callback table to these functions
  x = random.randint(0,1)
  if x == 0:
    pe = pefile.PE('../template32.exe')
    suffix = ".exe"
  elif x == 1:
    pe = pefile.PE('../template32.dll')
    suffix = ".dll"
    
  #Add some misc randomizations
  #TODO: make these actually consistent with the binaries
  pe.DIRECTORY_ENTRY_LOAD_CONFIG.struct.SecurityCookie += random.randint(0,10)*0x1000
  pe.DIRECTORY_ENTRY_LOAD_CONFIG.struct.SEHandlerTable += random.randint(0,10)*0x100
  pe.DIRECTORY_ENTRY_LOAD_CONFIG.struct.SEHandlerCount = random.randint(0,10)
  
  #FIXME: what's the more graceful way of doing this?
  error = 1
  while error:
    try:
      outFileName = "Round10Q" + str(questionCounter) + suffix
      #TODO: randomize some more of these elements
      pe.write(outFileName)
      error = 0
    except IOError:
      questionCounter+=1
  
  q = random.randint(0,len(Qs)-1)
  print "For binary R10Bins/%s..." % outFileName
  print Qs[q]
  answer = raw_input("Answer: ")
  
  if q == 0:
    CheckAnswerNum(answer, pe.OPTIONAL_HEADER.DATA_DIRECTORY[10].VirtualAddress)
  elif q == 1:
    CheckAnswerNum(answer, pe.OPTIONAL_HEADER.ImageBase + pe.OPTIONAL_HEADER.DATA_DIRECTORY[10].VirtualAddress)
  elif q == 2:
    CheckAnswerNum(answer, pe.DIRECTORY_ENTRY_LOAD_CONFIG.struct.get_file_offset())
  elif q == 3 or q == 4:
    CheckAnswerNum(answer, pe.DIRECTORY_ENTRY_LOAD_CONFIG.struct.SecurityCookie - pe.OPTIONAL_HEADER.ImageBase)
  elif q == 5 or q == 6:
    CheckAnswerNum(answer, pe.DIRECTORY_ENTRY_LOAD_CONFIG.struct.SecurityCookie)
  elif q == 7 or q == 8:
    CheckAnswerNum(answer, pe.DIRECTORY_ENTRY_LOAD_CONFIG.struct.SEHandlerTable - pe.OPTIONAL_HEADER.ImageBase)
  elif q == 9 or q == 10:
    CheckAnswerNum(answer, pe.DIRECTORY_ENTRY_LOAD_CONFIG.struct.SEHandlerTable)
  elif q == 11:
    CheckAnswerNum(answer, pe.DIRECTORY_ENTRY_LOAD_CONFIG.struct.SEHandlerCount)

def StartR10(seed, suppressRoundBanner, escapeScore):
  global gScore
  global gNextLevelRequiredScore
  if not suppressRoundBanner:
    print "================================================================================"
    print "Welcome to Round 10:"
    print "This round covers load configuration and signed binary information."
    print "================================================================================\n"
  #making a directory that the files go into, just to keep things tidier
  try:
    os.mkdir("R10Bins")
  except OSError:
    pass
  os.chdir("R10Bins")
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
    x = random.randint(0,8)
    if x <= 8:
      R10Q0(questionCounter)
#    elif x <= 13:
#      R8Q1(questionCounter)
#    elif x <= 12:
#      R8Q2(questionCounter)
#    elif x <= 14:
#      R8Q3(questionCounter)
      
    questionCounter+=1

  if not suppressRoundBanner:
    currentTime = int(time())
    roundTime = currentTime - roundStartTime
    roundMinutes = roundTime / 60
    roundSeconds = roundTime % 60
    totalElapsedTime = currentTime - rounds.helpers.gAbsoluteStartTime
    print "\nCongratulations, you passed round 10!"
    print "It took you %u minutes, %u seconds for this round." % (roundMinutes, roundSeconds)
    totalMinutes = totalElapsedTime / 60
    totalSeconds = totalElapsedTime % 60
    print "And so far it's taken you a total time of %u minutes, %u seconds." % (totalMinutes, totalSeconds) 

  os.chdir("..")