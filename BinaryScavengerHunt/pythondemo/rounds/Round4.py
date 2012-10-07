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

#This is Round 4 and will cover questions on the "normal" imports
#and the Import Address Table (IAT)

import os
import random
import pefile
from time import time
from rounds.helpers import CheckAnswerNum, CheckAnswerString, RandomizeSectionNames, GetExportsByName
import rounds.helpers

#TODO: find a way to randomize
#"In which section can the IAT be found?: "
#"In which section can the IMPORT_DIRECTORY be found?: "

#This function asks questions about the IMAGE_OPTIONAL_HEADER.DataDirectory entries
#that pertain to normal imports
def R4Q0(questionCounter):
  #NOTE: if you update the number of questions in this function, you need to update the boundaries in StartR2
  Qs = ["What is the value of IMAGE_OPTIONAL_HEADER.DataDirectory[IMAGE_DIRECTORY_ENTRY_IMPORT].RVA?",
        "What is the RVA that points at the import directory table?",
        "What is the value of IMAGE_OPTIONAL_HEADER.DataDirectory[IMAGE_DIRECTORY_ENTRY_IMPORT].Size?",
        "What is the size of the import directory table?",
        "What is the value of IMAGE_OPTIONAL_HEADER.DataDirectory[IMAGE_DIRECTORY_ENTRY_IAT].RVA?",
        "What is the RVA that points directly at the Import Address Table (IAT)?",
        "What is the value of IMAGE_OPTIONAL_HEADER.DataDirectory[IMAGE_DIRECTORY_ENTRY_IAT].Size?",
        "What is the total size of the Import Address Table (IAT)?"]
  #NOTE: if you update the number of questions in this function, you need to update the boundaries in StartR2

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

  #TODO: eventually I want to be able to move around the IAT

  #write out the (actually un)modified file
  outFileName = "Round4Q" + str(questionCounter) + suffix
  pe.write(outFileName)
  
  #Print the question
  q = random.randint(0,len(Qs)-1)
  print "For binary R4Bins/%s..." % outFileName
  print Qs[q]
  answer = raw_input("Answer: ")

  if q == 0 or q == 1:
    CheckAnswerNum(answer,pe.OPTIONAL_HEADER.DATA_DIRECTORY[1].VirtualAddress)
  elif q == 2 or q == 3:
    CheckAnswerNum(answer,pe.OPTIONAL_HEADER.DATA_DIRECTORY[1].Size)
  elif q == 4 or q == 5:
    CheckAnswerNum(answer,pe.OPTIONAL_HEADER.DATA_DIRECTORY[12].VirtualAddress)
  elif q == 6 or q == 7:
    CheckAnswerNum(answer,pe.OPTIONAL_HEADER.DATA_DIRECTORY[12].Size)
    
def R4Q1(questionCounter):
  #NOTE: if you update the number of questions in this function, you need to update the boundaries in StartR2
  Qs = ["How many DLLs does this binary import from?",
        "How many entries are there in the import directory table?",
        "Does this binary directly import functions from %s? (Y or N)"]
  #NOTE: if you update the number of questions in this function, you need to update the boundaries in StartR2
  
  #These names should all be things that none of the template binaries actually import from
  randomDLLNames = ["ADVAPI32.dll", "GDI32.dll", "SHELL32.dll", "NTDLL.dll", 
                    "COMCTL32.dll", "MSI.dll", "OLE32.dll", "MSVCRT.dll", 
                    "SETUPAPI.dll", "CRYPT32.dll", "SECUR32.dll", "IMAGEHLP.dll"]

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

  #TODO: eventually I want to be able to add new IAT information

  #write out the (actually un)modified file
  outFileName = "Round4Q" + str(questionCounter) + suffix
  pe.write(filename=outFileName)

  #Print the question
  q = random.randint(0,len(Qs)-1)
  print "For binary R4Bins/%s..." % outFileName
  interpolatedQuestion = Qs[q]
  if q == 2:
    if random.randint(0,1):
      #In this case we will ask about a fake DLL
      dllName = randomDLLNames[random.randint(0, len(randomDLLNames)-1)]
      importsNamedDll = "N"
    else:
      #In this case we will ask about a real DLL
      dllName = pe.DIRECTORY_ENTRY_IMPORT[random.randint(0, len(pe.DIRECTORY_ENTRY_IMPORT)-1)].dll
      importsNamedDll = "Y"
    interpolatedQuestion = Qs[q] % dllName
  print interpolatedQuestion
  answer = raw_input("Answer: ")

  if q == 0 or q == 1:
    CheckAnswerNum(answer,len(pe.DIRECTORY_ENTRY_IMPORT))
  elif q == 2:
    CheckAnswerString(answer,importsNamedDll)

def R4Q2(questionCounter):
  #NOTE: if you update the number of questions in this function, you need to update the boundaries in StartR2
  Qs = ["What section is the import directory table in?",
        "In what section can the IAT be found?",
        "What section is the import address table in?"]
  #NOTE: if you update the number of questions in this function, you need to update the boundaries in StartR2

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

  #TODO: eventually I want to be able to move around the IAT
  #For now it will always be in the same section, but with a randomized name
  RandomizeSectionNames(pe)
  #write out the modified file
  outFileName = "Round4Q" + str(questionCounter) + suffix
  pe.write(filename=outFileName)
  pe = pefile.PE(outFileName)

  #Print the question
  q = random.randint(0,len(Qs)-1)
  print "For binary R4Bins/%s..." % outFileName
  print Qs[q]
  answer = raw_input("Answer: ")

  if q == 0:
    for section in pe.sections:
      if (section.VirtualAddress <= pe.OPTIONAL_HEADER.DATA_DIRECTORY[1].VirtualAddress and
         (section.VirtualAddress + section.Misc_VirtualSize) > pe.OPTIONAL_HEADER.DATA_DIRECTORY[1].VirtualAddress):
        #V's solution to the string comparison issue ;)
        tmp = ['\x00'] * 8
        tmp[:len(answer)] = list(answer.lower())
        mungedAnswer = ''.join(tmp)
        CheckAnswerString(mungedAnswer,section.Name)
  elif q == 1 or q == 2:
    for section in pe.sections:
      if (section.VirtualAddress <= pe.OPTIONAL_HEADER.DATA_DIRECTORY[12].VirtualAddress and
         (section.VirtualAddress + section.Misc_VirtualSize) > pe.OPTIONAL_HEADER.DATA_DIRECTORY[1].VirtualAddress):
        tmp = ['\x00'] * 8
        tmp[:len(answer)] = list(answer.lower())
        mungedAnswer = ''.join(tmp)
        CheckAnswerString(mungedAnswer,section.Name)

def R4Q3(questionCounter):
  #NOTE: if you update the number of questions in this function, you need to update the boundaries in StartR2
  Qs = ["How many functions does this import from %s?",
        "At what RVA do the IAT entries from %s start?",
        "At what AVA do the IAT entries from %s start?",
        "At what RVA do the INT entries from %s start?",
        "At what AVA do the INT entries from %s start?",
        "Does this import function %s!%s? (Y or N)"]
  #NOTE: if you update the number of questions in this function, you need to update the boundaries in StartR2

  #These names should all be things that none of the template binaries actually import from the DLLs they do import from
  nonImportedFunctionNames = ["foo"]

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

  #TODO: eventually I want to be able to move around the IAT
  #For now it will always be in the same section, but with a randomized name
  RandomizeSectionNames(pe)
  #write out the modified file
  outFileName = "Round4Q" + str(questionCounter) + suffix
  pe.write(filename=outFileName)
  pe = pefile.PE(outFileName)

  #pick the question
  q = random.randint(0,len(Qs)-1)

  #select random existing DLL being imported from
  entry = pe.DIRECTORY_ENTRY_IMPORT[random.randint(0, len(pe.DIRECTORY_ENTRY_IMPORT)-1)]
  if q < 5:
    #This is the simpler question, we just need the name
    interpolatedQuestion = Qs[q] % entry.dll
  else:
    #here we need to choose whether we will 
    if random.randint(0,1):
      realImport = "Y"
      importName = entry.imports[random.randint(0,len(entry.imports)-1)].name
    else:
      realImport = "N"
      importedFunctions = []
      for imp in entry.imports:
        importedFunctions.append(imp.name)
      nonImportedFunctionNames = GetExportsByName(entry.dll)
      #Now get only the functions that are NOT imported
      nonImportedFunctionNames = list(set(nonImportedFunctionNames).difference(set(importedFunctions)))
      importName = nonImportedFunctionNames[random.randint(0,len(nonImportedFunctionNames)-1)]
    interpolatedQuestion = Qs[q] % (entry.dll, importName)
  print "For binary R4Bins/%s..." % outFileName
  print interpolatedQuestion
  answer = raw_input("Answer: ")

  if q == 0:
    CheckAnswerNum(answer,len(entry.imports))
  elif q == 1:
    CheckAnswerNum(answer,entry.struct.FirstThunk)
  elif q == 2:
    CheckAnswerNum(answer,pe.OPTIONAL_HEADER.ImageBase + entry.struct.FirstThunk)
  elif q == 3:
    CheckAnswerNum(answer,entry.struct.OriginalFirstThunk)
  elif q == 4:
    CheckAnswerNum(answer,pe.OPTIONAL_HEADER.ImageBase + entry.struct.OriginalFirstThunk)
  elif q == 5:
    CheckAnswerString(answer, realImport)

#TODO, make a question where I ask about the file offset for some of the RVA things.
#This will require them to map the RVA to the appropriate section, figure out the intra-section
#offset, and then add that offset to the PointerToRawData for the section

#TODO: need question about import by ordinal, but none of my templates do currently
#Wait until I have the ability to insert arbitrary imports
#def R4Q4(questionCounter):
#  #NOTE: if you update the number of questions in this function, you need to update the boundaries in StartR2
#  Qs = ["Bla bla bla import by ordinal?",
#        "Does this import function %s!%s? (Y or N)"]
#  #NOTE: if you update the number of questions in this function, you need to update the boundaries in StartR2

def StartR4(seed, suppressRoundBanner, escapeScore):
  global gScore
  global gNextLevelRequiredScore
  if not suppressRoundBanner:
    print "================================================================================"
    print "Welcome to Round 4:"
    print "This round is all about \"normal\" imports and the Import Address Table (IAT)"
#    print "\nRound terminology note:"
#    print "RVA = Relative Virtual Address (relative to image base)."
#    print "AVA = Absolute Virtual Address (base + RVA)"
    print "================================================================================\n"
  #making a directory that the files go into, just to keep things tidier
  try:
    os.mkdir("R4Bins")
  except OSError:
    pass
  os.chdir("R4Bins")
  filelist = [ f for f in os.listdir(".")]
  for f in filelist:
    os.remove(f)
  roundStartTime = int(time())
  rounds.helpers.gNextLevelRequiredScore = escapeScore
  random.seed(seed)
  questionCounter = 0;
  while rounds.helpers.gScore < rounds.helpers.gNextLevelRequiredScore:
    #changed this so that now every question is equal probability
    #though obviously I still ask the same questions more than one way sometimes
    #NOTE: if you update the number of questions in the round, you need to update these boundaries
    x = random.randint(0,18)
    if x <= 7:
      R4Q0(questionCounter)
    elif x <= 9:
      R4Q1(questionCounter)
    elif x <= 12:
      R4Q2(questionCounter)
    elif x <= 18:
      R4Q3(questionCounter)
      
    questionCounter+=1

  if not suppressRoundBanner:
    currentTime = int(time())
    roundTime = currentTime - roundStartTime
    roundMinutes = roundTime / 60
    roundSeconds = roundTime % 60
    totalElapsedTime = currentTime - rounds.helpers.gAbsoluteStartTime
    print "\nCongratulations, you passed round 4!"
    print "It took you %u minutes, %u seconds for this round." % (roundMinutes, roundSeconds)
    totalMinutes = totalElapsedTime / 60
    totalSeconds = totalElapsedTime % 60
    print "And so far it's taken you a total time of %u minutes, %u seconds." % (totalMinutes, totalSeconds) 

  os.chdir("..")

