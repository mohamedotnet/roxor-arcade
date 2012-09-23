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

#This is the bonus round. You can only reach it by getting 100 questions in a row
#correct (and when you use the 'x' cheat code, it doesn't count toward the streak count
#This round will have misc questions which should be quite a bit harder than previous rounds
#I'm just putting this here for now to store misc questions I think up

import os
import random
import pefile
from time import time
from rounds.helpers import CheckAnswerNum, CheckAnswerString
import rounds.helpers

#Q: "What field of this binary is currently invalid, and thus preventing its execution?\n 
#(Give field name in WINNT.H structure.field notation): "
#A: Possible fields to b0rk:
#IMAGE_DOS_HEADER.{Magic,e_lfanew}
#IMAGE_NT_HEADERS.
# - Signature (set to something other than MZ)
#IMAGE_FILE_HEADER.
# - Machine (make it not match the IMAGE_OPTIONAL_HEADER.Magic)
#IMAGE_OPTIONAL_HEADER.
# - Magic (make it not match IMAGE_FILE_HEADER.Machine
# - FileAlignment (for the 64 bit binary it doesn't like anything other than 0x200, even things 
#                  like 0x100 which should obviously work if 0x200 works)
# - AddressOfEntryPoint (make it not point at the start of the code. This will be very tricky 
#                        for them to figure out the fix to without checking existing working 
#                        binaries' code at the entry point and then finding that code in this 
#                        modified binary)
# - SizeOfImage (make it not agree with the sum of the section sizes)
#Follow up Q: "What value do you need to set that field to in order to allow the binary to execute?"
#A: Whatever the correct value is

#Q: Is the SizeOfImage correct? Will sometimes make this larger than is justified by the 
#section allocations, and therefore the student will have to sanity check the sum of section
#allocations vs. the field size (but won't go with less than the sum, since that is covered
#by the previous question

def StartRX(seed):
  global gScore
  global gNextLevelRequiredScore

  gNextLevelRequiredScore = 3000
  random.seed(seed)
  print "I'm just a placeholder! :D"

