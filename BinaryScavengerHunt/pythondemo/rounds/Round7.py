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

#This is Round 7 and will cover questions on relocations and debug info

import os
import random
import pefile
from time import time
from rounds.helpers import CheckAnswerNum, CheckAnswerString
import rounds.helpers


#Questions about the debug information
def R7Q0(questionCounter):
  #NOTE: if you update the number of questions in this function, you need to update the boundaries in StartR7
  Qs = ["According to the debugging information, what year was this file compiled?",
        "Does the debug information TimeDateStamp match the File Header TimeDateStamp?",
        "What is the RVA that would point at this file's path the the debugging information (.pdb file)?",
        "What is the full filename, including path, where this file's debugging information (.pdb file) was originally placed at compile time?",
        "What is the file offset that points at the .pdb file path?",
        "What is the RVA of the debug information?",
        "What is the VA of the debug information?",
        "What is the file offset to the debug information?"]
  #NOTE: if you update the number of questions in this function, you need to update the boundaries in StartR7

  x = random.randint(0,3)
  if x == 0:
    pe = pefile.PE('../template32-bound.dll')
    suffix = ".dll"
  elif x == 1:
    pe = pefile.PE('../template32-bound.exe')
    suffix = ".exe"
  if x == 2:
    pe = pefile.PE('../template64-bound.exe')
    suffix = ".exe"
  else:
    pe = pefile.PE('../template64-bound.dll')
    suffix = ".dll"

  outFileName = "Round7Q" + str(questionCounter) + suffix
  
  if random.randint(0,1):
    pe.DIRECTORY_ENTRY_DEBUG[0].struct.TimeDateStamp = random.randint(0,4294967296)
    if random.randint(0,1):
      pe.FILE_HEADER.TimeDateStamp = pe.DIRECTORY_ENTRY_DEBUG[0].struct.TimeDateStamp
  
  #TODO: randomize some more of these elements
  pe.write(outFileName)
  
  q = random.randint(0,len(Qs)-1)
  print "For binary R7Bins/%s..." % outFileName
  print Qs[q]
  
  answer = raw_input("Answer: ")
  
  if q == 0:
    debugYear = 1970 + int(pe.DIRECTORY_ENTRY_DEBUG[0].struct.TimeDateStamp / 31556926)
    CheckAnswerNum(answer, debugYear)
  elif q == 1:
    if pe.DIRECTORY_ENTRY_DEBUG[0].struct.TimeDateStamp == pe.FILE_HEADER.TimeDateStamp:
      CheckAnswerString(answer, "Y")
    else:
      CheckAnswerString(answer, "N")
  elif q == 2:
    #The 0x18 offset comes from the fact that all my template binaries currently are
    #using CV_INFO_PDB70 for the debug information
    #TODO: want to show both CV_INFO_PDB70 and CV_INFO_PDB20 types (in the original
    #class all the files were CV_INFO_PDB20 type)
    CheckAnswerNum(answer, pe.DIRECTORY_ENTRY_DEBUG[0].struct.AddressOfRawData + 0x18)
  elif q == 3:
    CheckAnswerString(answer, pe.get_string_at_rva(pe.DIRECTORY_ENTRY_DEBUG[0].struct.AddressOfRawData + 0x18))
  elif q == 4:
    CheckAnswerNum(answer, pe.get_offset_from_rva(pe.DIRECTORY_ENTRY_DEBUG[0].struct.AddressOfRawData + 0x18))
  elif q == 5:
    CheckAnswerNum(answer, pe.OPTIONAL_HEADER.DATA_DIRECTORY[6].VirtualAddress)
  elif q == 6:
    CheckAnswerNum(answer, pe.OPTIONAL_HEADER.ImageBase + pe.OPTIONAL_HEADER.DATA_DIRECTORY[6].VirtualAddress)
  elif q == 7:
    CheckAnswerNum(answer, pe.get_offset_from_rva(pe.OPTIONAL_HEADER.DATA_DIRECTORY[0].VirtualAddress))

#Questions about the relocations
def R7Q1(questionCounter):
  #NOTE: if you update the number of questions in this function, you need to update the boundaries in StartR7
  Qs = ["How many relocations are there from RVA %x to %x?",
        "Is 0x%x a relocation location? (Y or N)",
        "What is the RVA of the relocation information?",
        "What is the VA of the relocation information?",
        "What is the file offset to the relocation information?",
        "What section is the relocation information in?"]
  #NOTE: if you update the number of questions in this function, you need to update the boundaries in StartR7

  x = random.randint(0,3)
  if x == 0:
    pe = pefile.PE('../template32-bound.dll')
    suffix = ".dll"
  elif x == 1:
    pe = pefile.PE('../template32-bound.exe')
    suffix = ".exe"
  if x == 2:
    pe = pefile.PE('../template64-bound.exe')
    suffix = ".exe"
  else:
    pe = pefile.PE('../template64-bound.dll')
    suffix = ".dll"

  outFileName = "Round7Q" + str(questionCounter) + suffix
   
  #TODO: randomize some more of these elements
  pe.write(outFileName)
  
  q = random.randint(0,len(Qs)-1)
  print "For binary R7Bins/%s..." % outFileName
  relocEntry = pe.DIRECTORY_ENTRY_BASERELOC[random.randint(0,len(pe.DIRECTORY_ENTRY_BASERELOC)-1)]
  if q == 0:
    #pick a random page to ask about
    interpolatedQuestion = Qs[q] % (relocEntry.struct.VirtualAddress, relocEntry.struct.VirtualAddress+0x1000)
  elif q == 1:
    #pick a random relocation to ask about
    relocEntry2 = relocEntry.entries[random.randint(0,len(relocEntry.entries)-1)]
    relocRVA = relocEntry2.rva
    if random.randint(0,1):
      realReloc = 1
    else:
      realReloc = 0
      relocRVA += 1
      
    interpolatedQuestion = Qs[q] % relocRVA
  else:
    interpolatedQuestion = Qs[q]
  print interpolatedQuestion
  answer = raw_input("Answer: ")
  
  if q == 0:
    CheckAnswerNum(answer, len(relocEntry.entries))
  elif q == 1:
    if realReloc:
      CheckAnswerString(answer, "Y")
    else:
      CheckAnswerString(answer, "N")
  elif q == 2:
    CheckAnswerNum(answer, pe.OPTIONAL_HEADER.DATA_DIRECTORY[5].VirtualAddress)
  elif q == 3:
    CheckAnswerNum(answer, pe.OPTIONAL_HEADER.ImageBase + pe.OPTIONAL_HEADER.DATA_DIRECTORY[5].VirtualAddress)
  elif q == 4:
    CheckAnswerNum(answer, pe.get_offset_from_rva(pe.OPTIONAL_HEADER.DATA_DIRECTORY[5].VirtualAddress))
  elif q == 5:
    CheckAnswerString(answer, pe.get_section_by_rva(pe.OPTIONAL_HEADER.DATA_DIRECTORY[5].VirtualAddress).Name)
  

def StartR7(seed, suppressRoundBanner, escapeScore):
  global gScore
  global gNextLevelRequiredScore
  if not suppressRoundBanner:
    print "================================================================================"
    print "Welcome to Round 7:"
    print "This round covers the debug information which is baked into most executables,"
    print "and it also covers \"relocations\" which allow the code to be moved in memory"
    print "================================================================================\n"
  #making a directory that the files go into, just to keep things tidier
  try:
    os.mkdir("R7Bins")
  except OSError:
    pass
  os.chdir("R7Bins")
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
    x = random.randint(0,13)
    if x <= 7:
      R7Q0(questionCounter)
    elif x <= 13:
      R7Q1(questionCounter)
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
    print "\nCongratulations, you passed round 7!"
    print "It took you %u minutes, %u seconds for this round." % (roundMinutes, roundSeconds)
    totalMinutes = totalElapsedTime / 60
    totalSeconds = totalElapsedTime % 60
    print "And so far it's taken you a total time of %u minutes, %u seconds." % (totalMinutes, totalSeconds) 

  os.chdir("..")

