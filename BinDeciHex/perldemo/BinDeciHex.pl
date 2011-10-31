#!/usr/bin/perl

srand();

$SIG{INT} = \&forceExit;
$currentScore = 0;

print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n";
print "Welcome to the perl demo of BinDeciHex!\n";
print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n";
print "In this game of skill, you will convert numbers between\n";
print "difference bases (radices). This skill is very useful\n";
print "when reading memory addresses, which are often represented\n";
print "in base 16, hexidecimal. Also, when code performs bit-wise\n";
print "operations, it is good to know how to convert constants\n";
print "in to base 2, binary.\n";
print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n";
print "In this round you will always convert binary to hex.\n";
print "A trick you can use is to memorize the mapping from groups\n";
print "of 4 binary characters to a single hex character.\n";
print "For instance, hex '1' is binary 0001, hex '2' is binary\n";
print "0010, hex '3' is binary 0011. This continues until hex 'f'\n";
print "which is binary 1111. Make yourself a table, and memorize.\n";
print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n";
print "Enter q at any time to quit.\n";
print "ROUND 1: 1000 points needed to pass\n";
print "Hit q to quit, and any other key to continue\n";
chomp($userInput = <STDIN>);
if($userInput eq 'q'){
	print("You entered q to quit. Returning score = $currentScore\n");
	$currentScore = $currentScore / 100;
	exit($currentScore);
}

#For round 1 it will always be binary to hex
while($currentScore < 1000){

	#generate a random byte
	$randByte = int(rand(257));
	#printf("randByte = 0x%x\n", $randByte); #for cheating

	#print in binary and ask for conversion
	printf("Binary value: %08b\n", $randByte);
	print "What is this value in hex? (optionally prefix with 0x)\n";

	chomp($userInput = <STDIN>);
	if($userInput eq 'q'){
		print("You entered q to quit. Returning score = $currentScore\n");
		$currentScore = $currentScore / 100;
		exit($currentScore);
	}
	if($userInput eq 's'){
		print("~tweeEEtle deeEEtle deeEEt~ s00p3r s3kr47 level skipping warp whistle enabled!\n");
		last;
	}
	#print("$userInput $randByte\n");
	if(hex($userInput) == $randByte){
		print "Correct! :D \n";
		$currentScore += 100;
		print "You gained 100 points, and now have $currentScore points\n";
	}
	else{
		print "Incorrect :( \n";
		$currentScore -= 200;
		print "You lost 200 points, and now have $currentScore points\n";
	}

}
print "~~~~~~~~~~~~~~~~~~~~~~LEVEL 1 COMPLETED~~~~~~~~~~~~~~~~~~~~~~\n";
print "In this round you will always convert hex back to binary.\n";
print "Simply use the same memorized mappings.\n";
print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n";
print "ROUND 2: 2000 points needed to pass\n";
print "Hit q to quit, and any other key to continue\n";
chomp($userInput = <STDIN>);
if($userInput eq 'q'){
	print("You entered q to quit. Returning score = $currentScore\n");
	$currentScore = $currentScore / 100;
	exit($currentScore);
}

while($currentScore < 2000){

	#generate a random byte
	$randByte = int(rand(257));
	#printf("randByte = %08b\n", $randByte); #for cheating

	#print in hex and ask for conversion
	printf("Hex value: 0x%02x\n", $randByte);
	print "What is this value in binary?\n";

	chomp($userInput = <STDIN>);
	if($userInput eq 'q'){
		print("You entered q to quit. Returning score = $currentScore\n");
		$currentScore = $currentScore / 100;
		exit($currentScore);
	}
	if($userInput eq 's'){
		print("~tweeEEtle deeEEtle deeEEt~ s00p3r s3kr47 level skipping warp whistle enabled!\n");
		last;
	}
	$userInput = bin2dec($userInput);
	#print("$userInput $randByte\n");
	if($userInput == $randByte){
		print "Correct! :D \n";
		$currentScore += 100;
		print "You gained 100 points, and now have $currentScore points\n";
	}
	else{
		print "Incorrect :( \n";
		$currentScore -= 200;
		print "You lost 200 points, and now have $currentScore points\n";
	}

}

print "~~~~~~~~~~~~~~~~~~~~~~LEVEL 2 COMPLETED~~~~~~~~~~~~~~~~~~~~~~\n";
print "This round will always convert binary to unsigned decimal.\n";
print "The trick here is to memorize what power of 2 each place in \n";
print "a binary value corresponds to. So for instance: \n";
print "00000001 is saying 2^0 (1)\n";
print "00000010 is saying 2^1 (2)\n";
print "00000100 is saying 2^2 (4)\n";
print "...\n";
print "10000000 is saying 2^7 (128)\n";
print "So a binary number can be converted to decimal by simply  \n";
print "adding up all these values. For example:\n";
print "10000100 is 2^7 (128) + 2^2 (4) = 132 decimal.\n";
print "00110001 is 2^5 (32) + 2^4 (16) + 2^0 (1) = 49 decimal.\n";
print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n";
print "ROUND 3: 4000 points needed to pass\n";
print "Hit q to quit, and any other key to continue\n";
chomp($userInput = <STDIN>);
if($userInput eq 'q'){
	print("You entered q to quit. Returning score = $currentScore\n");
	$currentScore = $currentScore / 100;
	exit($currentScore);
}
while($currentScore < 4000){

	#generate a random byte
	$randByte = int(rand(257));
	#printf("randByte = %d\n", $randByte); #for cheating

	#print in binary and ask for conversion
	printf("Binary value: %08b\n", $randByte);
	print "What is this value in unsigned decimal?\n";

	chomp($userInput = <STDIN>);
	if($userInput eq 'q'){
		print("You entered q to quit. Returning score = $currentScore\n");
		$currentScore = $currentScore / 100;
		exit($currentScore);
	}
	if($userInput eq 's'){
		print("~tweeEEtle deeEEtle deeEEt~ s00p3r s3kr47 level skipping warp whistle enabled!\n");
		last;
	}
	#print("$userInput $randByte\n");
	if($userInput == $randByte){
		print "Correct! :D \n";
		$currentScore += 200;
		print "You gained 200 points, and now have $currentScore points\n";
	}
	else{
		print "Incorrect :( \n";
		$currentScore -= 400;
		print "You lost 400 points, and now have $currentScore points\n";
	}

}

print "~~~~~~~~~~~~~~~~~~~~~~LEVEL 3 COMPLETED~~~~~~~~~~~~~~~~~~~~~~\n";
print "Converting from decimal to binary is slightly more difficult\n";
print "because it requires subtracting the maximum divisible power\n";
print "of two, and then the next maximum, etc.\n";
print "Most of the time you will just break out the calculator in\n";
print "'programmer mode' for this. But it is good for you to go \n";                        
print "through it by hand a few times just to make sure you are\n";
print "comfortable with it.\n";
print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n";
print "ROUND 4: 6000 points needed to pass\n";
print "Hit q to quit, and any other key to continue\n";
chomp($userInput = <STDIN>);
if($userInput eq 'q'){
        print("You entered q to quit. Returning score = $currentScore\n");
        $currentScore = $currentScore / 100;
        exit($currentScore);
}
while($currentScore < 6000){

        #generate a random byte
        $randByte = int(rand(257));
        #printf("randByte = %08b\n", $randByte); #for cheating

        #print in binary and ask for conversion
        printf("Decimal value: %d\n", $randByte);
        print "What is this value in binary?\n";

        chomp($userInput = <STDIN>);
        if($userInput eq 'q'){
                print("You entered q to quit. Returning score = $currentScore\n");
                $currentScore = $currentScore / 100;
                exit($currentScore);
        }
        if($userInput eq 's'){
                print("~tweeEEtle deeEEtle deeEEt~ s00p3r s3kr47 level skipping warp whistle enabled!\n");
                last;
        }
        $userInput = bin2dec($userInput);
	#print("$userInput $randByte\n");
        if($userInput == $randByte){
                print "Correct! :D \n";
                $currentScore += 200;
                print "You gained 200 points, and now have $currentScore points\n";
        }
        else{   
                print "Incorrect :( \n";
                $currentScore -= 400;
                print "You lost 400 points, and now have $currentScore points\n";
        }
}

print "~~~~~~~~~~~~~~~~~~~~~~LEVEL 4 COMPLETED~~~~~~~~~~~~~~~~~~~~~~\n";
print "Now let's start examining signed numbers. A -1 in decimal is\n";
print "0xFF in hex. This is because a negative number is defined as\n";
print "the 'two's compliment' of the positive number. To get the \n";
print "two's compliment, we first flip all the bits, and then add 1.\n";
print "This can require us to conver through muliple radices, or we\n";
print "So for instance if decimal 1 is 0x01 in hex and 00000001 in\n";
print "binary, then we first flip all the bits, which gives us \n";
print "11111110 in binary and 0xFE in hex. Then we add 1 to get 0xFF\n";
print "in hex and 11111111 in binary. Therefore 0xFF and 11111111\n";
print "are the signed representation of -1, even though they are the\n";
print "unsigned representation of 255.\n";
print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n";
print "For one byte, the positive numbers are 1 to 127 (0x1 to 0x7F)\n";
print "(00000001 to 01111111) and the negative numbers are -1 to -128\n";
print "(0xFF to 0x80) (11111111 to 10000000). Thus, all positive\n";
print "numbers always have their most significant bit set to 0, and\n";
print "all negative numbers have their most significant bit set to 1.\n";
print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n";
print "A shortcut which can be used to figure out what decimal \n";
print "negative number a value corresponds to is to ask \"What value\n";
print "could I add to this value to get it to wrap around to 0?\"\n";
print "So for instance, with 0xFF if you added 0x01, and you only\n";
print "have 1 byte of space, it would wrap around to 0. Therefore \n";
print "0xFF is -1. Or 0xFC + 0x04 = 0x00, so 0xFC = -4.\n";
print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n";
print "ROUND 5: 10000 points needed to pass\n";
print "Hit q to quit, and any other key to continue\n";
chomp($userInput = <STDIN>);
if($userInput eq 'q'){
	print("You entered q to quit. Returning score = $currentScore\n");
	$currentScore = $currentScore / 100;
	exit($currentScore);
}
while($currentScore < 10000){

	#generate a random byte
	$randByte = int(rand(128));
	$randByte += 128;
	#printf("randByte = %d\n", $randByte - 256); #for cheating

	#print in binary and ask for conversion
	printf("Hex value: 0x%02x\n", $randByte);
	print "What is this value in signed decimal?\n";

	chomp($userInput = <STDIN>);
	if($userInput eq 'q'){
		print("You entered q to quit. Returning score = $currentScore\n");
		$currentScore = $currentScore / 100;
		exit($currentScore);
	}
	if($userInput eq 's'){
		print("~tweeEEtle deeEEtle deeEEt~ s00p3r s3kr47 level skipping warp whistle enabled!\n");
		last;
	}
	$userInput = scalar $userInput;
	$randByte = $randByte - 256;
	#print("$userInput $randByte\n");
	if($userInput == $randByte){
		print "Correct! :D \n";
		$currentScore += 200;
		print "You gained 200 points, and now have $currentScore points\n";
	}
	else{
		print "Incorrect :( \n";
		$currentScore -= 400;
		print "You lost 400 points, and now have $currentScore points\n";
	}

}

print "~~~~~~~~~~~~~~~~~~~~~~LEVEL 5 COMPLETED~~~~~~~~~~~~~~~~~~~~~~\n";
print "How about the opposite direction?\n";
print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n";
print "ROUND 6: 12000 points needed to pass\n";
print "Hit q to quit, and any other key to continue\n";
chomp($userInput = <STDIN>);
if($userInput eq 'q'){
	print("You entered q to quit. Returning score = $currentScore\n");
	$currentScore = $currentScore / 100;
	exit($currentScore);
}
while($currentScore < 12000){

	#generate a random byte
	$randByte = int(rand(129));
	$randByte *= -1;
	#printf("randByte = %08b\n", $randByte); #for cheating

	#print in binary and ask for conversion
	printf("Decimal value: %d\n", $randByte);
	print "What is this value in binary?\n";

	chomp($userInput = <STDIN>);
	if($userInput eq 'q'){
		print("You entered q to quit. Returning score = $currentScore\n");
		$currentScore = $currentScore / 100;
		exit($currentScore);
	}
	if($userInput eq 's'){
		print("~tweeEEtle deeEEtle deeEEt~ s00p3r s3kr47 level skipping warp whistle enabled!\n");
		last;
	}
	$userInput = bin2dec($userInput);
	if($userInput > 127){
		$userInput = $userInput - 256;
	}
	#print("$userInput $randByte\n");
	if($userInput == $randByte){
		print "Correct! :D \n";
		$currentScore += 200;
		print "You gained 200 points, and now have $currentScore points\n";
	}
	else{
		print "Incorrect :( \n";
		$currentScore -= 400;
		print "You lost 400 points, and now have $currentScore points\n";
	}

}

print "-------------CURRENT LEVELS COMPLETED---------------\n";
print "WINNER WINNER CHICKEN DINNER!\n";
print "That's all for now. Check out the code and think about how\n";
print "to turn this into a real game!\n";
print("Returning score = $currentScore\n");
$currentScore = $currentScore / 100;
exit($currentScore);

sub bin2dec { return unpack("N", pack("B32", substr("0" x 32 . shift, -32))); }

sub forceExit{
	$currentScore = $currentScore / 100;
	print("caugt SIG{INT}, returning currentScore = $currentScore\n");
	exit($currentScore);
}
