#!/usr/bin/perl

use Switch;

#With thanks to http://nedbatchelder.com/text/hexwords.html for the hex words

@wordList = ("acce55", "acc01ade", "affab1e", "a1fa1fa", "a5be5705", "babb1e", "badd00d", "ba1dd00d", "ba77d00d", "ba11ad", "ba5eba11", "bead", "beef", "be5077ed", "b1ade", "b1e55ed", "b100d", "b0bb1e", "b0b51ed", "b01dface", "b00b", "b007ab1e", "b055", "cabba1a", "cab1e", "cafebabe", "ca11ab1e", "ca5cade", "ca55e77e", "cede", "c0a1e5ce", "c0bb1e", "c0de", "c01055a1", "dabb1e", "dad", "deadbeef", "debac1e", "deba7e", "decade", "decaf", "decea5ed", "dec0de", "deface", "defea7", "de1e7ed", "d00dad", "d00d1e", "ea7ab1e",, "ee1", "effab1e", "effec7ed", "e1de57", "e1ec7ed", "e1f", "e5ca1ade", "fab1ed", "face1e55", "face7ed", "fad", "faded", "fa11", "feca1", "fece5", "feeb1e", "f1ea", "f1ee", "f1eece", "f100ded", "f0ca1", "f01ded", "f00d", "f005ba11", "f007ba11", "1abe1", "1ac7a5e", "1ad1e", "1ead", "1eaf", "10ca1e", "1005e", "0af", "0b501e7e", "0b57ac1e", "0ddba11", "0ffbea7", "0ff5e7", "00d1e5", "5add1ed", "5a1ad", "5caff01d", "5c0ff", "5eaf00d", "5e1ec7", "50f7ba11", "501ace", "57abbed", "7ab1e", "7ac71e55", "7a7700", "7e1eca57", "7e117a1e", "70ad5", "70bacc0", "70cca7a", "7001", "707a1ed"); 

srand();

my $currentScore = 0;

print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n";
print "Welcome to the perl demo of The Other ESP Game!\n";
print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n";
print "In this game of skill, you will learn to represent data\n";
print "values on \"the stack\" (as used in x86 assembly) as \n";
print "relative to either the stack pointer, the \"esp\" register,\n";
print "or the stack frame base pointer, \"ebp\".\n";
print "\n";
print "In the early rounds, you may be able to represent it as\n";
print "relative to either, but in the later rounds there may be only\n";
print "one choice.\n";
print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n";
print "ROUND 1: 1000 points needed to pass\n";


#***************************
#********ROUND 1************
#***************************

#Round 1 will always have 6 possible stack values, with the ebp at the top and the esp at the bottom

while($currentScore < 1000){
	$numStackElements = 6;
	$indexToFind = int(rand($numStackElements));
	$correctness = StackPrint(0, $numStackElements, 0, 0, $indexToFind, 0, 4);
	ScoreKeeper($correctness, 100);
}
print "-------------LEVEL 1 COMPLETED---------------\n";
print "On to round 2!\n";
print "ROUND 2: 2000 points needed to pass\n";

#$orientation values: 0 = low addresses at bottom, 1 = low addresses at top, 2 = low addresses at left, 3 = low addresses at right
#$numStackElements, 1-based number of elements in the stack, so if == 1, then there will be 1 element which both ebp and esp point at
#$ebpIndex: 0-based index from the highest element which ebp points at. If 0, then it points at the highest element.
#$espIndex: 0-based index from the lowest element which esp points at. If 0, then it points at the lowest element.
#$indexToFind: 0-based index from the lowest element which should be entered by the user.
#$oneOffsetOnly:0 = should include ebp-relative AND esp-relative offset options
	#	1 = esp-relative-only offset, ebp-relative should be impossible to select
	#	2 = ebp-relative-only offset, esp-relative should be impossible to select
#$numOffsetChoices: the number of choices of offsets a user is given
sub StackPrint{
	$orientation = $_[0];
	$numStackElements = $_[1];
	$ebpIndex = ($numStackElements-1) - $_[2]; #This is immediately converted into an lowest-element-relative index
	$espIndex = $_[3];
	$indexToFind = $_[4];
	$oneOffsetOnly = $_[5];
	$numOffsetChoices = $_[6];

	#Calculate the distance from both ebp and esp to the indexToFind
	$ebpRelToFind = $indexToFind - $ebpIndex;
#	print "ebpRelToFind = $ebpRelToFind\n";
	$espRelToFind = $indexToFind - $espIndex;
#	print "espRelToFind = $espRelToFind\n";

	#Calculate the given number of random choices to display for the user, and also the place where the correct choices will be displayed
	#ebp and esp can't pick the same index
	$ebpOffsetDisplayIndex = int(rand($numOffsetChoices));
#	print "ebpOffsetDisplayIndex = $ebpOffsetDisplayIndex\n";
	if($ebpRelToFind != $espRelToFind){
		do{
			$espOffsetDisplayIndex = int(rand($numOffsetChoices));
#			print "candidate espOffsetDisplayIndex = $espOffsetDisplayIndex\n";
		}while($espOffsetDisplayIndex == $ebpOffsetDisplayIndex);
#		print "espOffsetDisplayIndex = $espOffsetDisplayIndex\n";
	}

	#going to generate an array just storing the order in which the randomized options will be displayed
	@displayOrder = ();
	for($i = 0; $i < $numOffsetChoices; $i++){
		if($i == $ebpOffsetDisplayIndex){
#			printf("i = %d, pushed ebpRelToFind*4 = %d\n",$i, $ebpRelToFind*4);
			push(@displayOrder, $ebpRelToFind*4);
			next;
		}
		if($espOffsetDisplayIndex != $ebpOffsetDisplayIndex && $i == $espOffsetDisplayIndex){
#			printf("i = %d, pushed espRelToFind*4 = %d\n",$i, $espRelToFind*4);
			push(@displayOrder, $espRelToFind*4);
			next;
		}
		$posOrNeg = int(rand(2));
		do{
			#I'm doing the +2 just so it can have some values that are out of bounds
			$randOffset = int(rand($numStackElements+2));
			if($posOrNeg){
				$randOffset = -$randOffset;
			}
#			print "candidate randOffset = $randOffset\n";
		}while($randOffset == $ebpRelToFind || $randOffset == $espRelToFind);
#		print "accepted randOffset = $randOffset\n";
#		printf("i = %d, pushed randOffset*4 = %d\n",$i, $randOffset*4);
		push(@displayOrder, $randOffset*4);
	}
#	print "displayOrder = @displayOrder\n";


	#convert the ebp and esp relative values into eventual number-letter combinations like the user will have to input
	@correctInput[0] = "a$ebpOffsetDisplayIndex";
	@correctInput[1] = "b$espOffsetDisplayIndex";
#	print "correctInput = @correctInput\n";

	#now generate the random values to display on the stack
	@randStackStuff = ();
	for($i = 0; $i < $numStackElements; $i++){

		do{
			$randWord = $wordList[int(rand(@wordList))];
#			print "Candidate randWord = $randWord\n";
		}while(grep {$_ eq $randWord} @randStackStuff);
#		print "accepting $randWord\n";
		push(@randStackStuff, $randWord);
	}

	PrintStackWithOrientation($orientation, $ebpIndex, $espIndex, \@randStackStuff);

	print "Enter the combination of number and letter (like \"a1\", \"b4\", etc) for the offset to:\n";
	print "$randStackStuff[$indexToFind]\n";
	print "a) ebp, b) esp\n";
	for ($i = 0; $i < @displayOrder; $i++){
		print "$i) $displayOrder[$i]\t";
	}
	print "\n";
	print "> ";

	chomp($userInput = <STDIN>);
	if($userInput == $correctInput[0] || $userInput == $correctInput[1]){
		return 1;
	}
	else{
		return 0;
	}
}

#$orientation values: 0 = low addresses at bottom, 1 = low addresses at top, 2 = low addresses at left, 3 = low addresses at right
sub PrintStackWithOrientation{
	$orientation = $_[0];
	$ebpIndex = $_[1];
	$espIndex = $_[2];
	$stackArrayRef = $_[3];
	@array = @{$stackArrayRef};

	switch($orientation){
		#low addresses at bottom
		case 0{
			print "\nHIGH ADDRESSES\n";
			for($i = @array-1; $i >= 0; $i--){
				print "|------------|\n";
				print "| 0x";
				if(length($array[$i]) > 8){
					print "length($array[$i])\n";
					return;
				}
				$padding = 8 - length($array[$i]);
				while($padding){
					print "0";
					$padding--;
				}
				print "$array[$i] |";

				if($i == $ebpIndex) {print " <-- ebp";}
				if($i == $espIndex) {print " <-- esp";}

				print "\n";
			}
			print "|------------|\n";
			print "LOW ADDRESSES\n\n";
		}
		#low addresses at top
		case 1{
			print "case 1\n";
		}
		#low addresses at left
		case 2{
			print "case 2\n";
		}
		#low addresses at right
		case 3{
			print "case 3\n";
		}
		else{
			print "you suck\n";
		}
	}
}

sub ScoreKeeper{
	$correctness = $_[0];
	$points = $_[1];
	if($correctness){
		print "Correct! :D \n";
		$currentScore += $points;
		print "You gained $points points, and now have $currentScore points\n";
	}
	else{
		print "Incorrect :( \n";
		$currentScore -= 2*$points;
		print "You lost " + 2*$points + "points, and now have $currentScore points\n";
	}
}
