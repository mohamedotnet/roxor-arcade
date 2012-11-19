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

#This is Round 8 and will cover questions on thread local storage (TLS) callbacks

import os
import random
import pefile
from time import time
from rounds.helpers import CheckAnswerNum, CheckAnswerString
import rounds.helpers

#Basic questions about the TLS information
def R8Q0(questionCounter):
  #NOTE: if you update the number of questions in this function, you need to update the boundaries in StartR8
  Qs = ["What is the RVA of the TLS directory?",
        "What is the VA of the TLS directory?",
        "What is the file offset to the TLS directory?",
        "What is the RVA of the TLS callbacks array?",
        "What is the VA of the TLS callbacks array?",
        "What is the file offset to the TLS callbacks array?",
        "How many TLS callbacks does this binary contain?",
        "What is the RVA of callback index %u?",
        "What is the VA of callback index %u?"]
  #NOTE: if you update the number of questions in this function, you need to update the boundaries in StartR8

  #TODO: currently I just made one template file that has 5 functions that can possibly be called
  #and the code will just add or subtract pointers in the callback table to these functions
  x = random.randint(0,0)
  if x == 0:
    pe = pefile.PE('../template32-tls.exe')
    suffix = ".exe"
#  elif x == 1:
#    pe = pefile.PE('../template32-bound.exe')
#    suffix = ".exe"
#  if x == 2:
#    pe = pefile.PE('../template64-bound.exe')
#    suffix = ".exe"
#  else:
#    pe = pefile.PE('../template64-bound.dll')
#    suffix = ".dll"
    
  numTlsEntries = random.randint(1,5)
  #TODO: randomly and independently pick numTlsEntries entries from the binary's exports
  randomCallbackAddressesList = [0x401000] * numTlsEntries
  randomCallbackAddressesList += [0] #easier to just add the null terminator here
  #FIXME: what's the more graceful way of doing this?
  error = 1
  while error:
    try:
      outFileName = "Round8Q" + str(questionCounter) + suffix
      pe.x_CreateTLS(randomCallbackAddressesList, outFileName)
      error = 0
    except IOError:
      questionCounter+=1

  pe = pefile.PE(outFileName)
  
  q = random.randint(0,len(Qs)-1)
  print "For binary R8Bins/%s..." % outFileName
  if q >= 7:
    randIndex = random.randint(0,numTlsEntries-1)
    interpolatedQuestion = Qs[q] % randIndex
  else:
    interpolatedQuestion = Qs[q]
  print interpolatedQuestion
  answer = raw_input("Answer: ")
  
  if q == 0:
    CheckAnswerNum(answer, pe.OPTIONAL_HEADER.DATA_DIRECTORY[9].VirtualAddress)
  elif q == 1:
    CheckAnswerNum(answer, pe.OPTIONAL_HEADER.ImageBase + pe.OPTIONAL_HEADER.DATA_DIRECTORY[9].VirtualAddress)
  elif q == 2:
    CheckAnswerNum(answer, pe.DIRECTORY_ENTRY_TLS.struct.get_file_offset())
  elif q == 3:
    CheckAnswerNum(answer, pe.DIRECTORY_ENTRY_TLS.struct.AddressOfCallBacks - pe.OPTIONAL_HEADER.ImageBase)
  elif q == 4:
    CheckAnswerNum(answer, pe.DIRECTORY_ENTRY_TLS.struct.AddressOfCallBacks)
  elif q == 5:
    CheckAnswerNum(answer, pe.get_offset_from_rva(pe.DIRECTORY_ENTRY_TLS.struct.AddressOfCallBacks - pe.OPTIONAL_HEADER.ImageBase))
  elif q == 6:
    CheckAnswerNum(answer, numTlsEntries)
  elif q == 7:
    callbackArray = pe.DIRECTORY_ENTRY_TLS.struct.AddressOfCallBacks - pe.OPTIONAL_HEADER.ImageBase
    CheckAnswerNum(answer, pe.get_dword_at_rva(callbackArray + randIndex*4) - pe.OPTIONAL_HEADER.ImageBase)
  elif q == 8:
    callbackArray = DIRECTORY_ENTRY_TLS.struct.AddressOfCallBacks - pe.OPTIONAL_HEADER.ImageBase
    CheckAnswerNum(answer, pe.get_dword_at_rva(callbackArray + randIndex*4))

def StartR8(seed, suppressRoundBanner, escapeScore):
  global gScore
  global gNextLevelRequiredScore
  if not suppressRoundBanner:
    print "================================================================================"
    print "Welcome to Round 8:"
    print "This round covers thread local storage (TLS), which can be used on unwitting"
    print "analysts in order to execute code before the AddressOfEntryPoint is called to."
    print "================================================================================\n"
  #making a directory that the files go into, just to keep things tidier
  try:
    os.mkdir("R8Bins")
  except OSError:
    pass
  os.chdir("R8Bins")
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
      R8Q0(questionCounter)
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
    print "\nCongratulations, you passed round 8!"
    print "It took you %u minutes, %u seconds for this round." % (roundMinutes, roundSeconds)
    totalMinutes = totalElapsedTime / 60
    totalSeconds = totalElapsedTime % 60
    print "And so far it's taken you a total time of %u minutes, %u seconds." % (totalMinutes, totalSeconds) 

  os.chdir("..")


