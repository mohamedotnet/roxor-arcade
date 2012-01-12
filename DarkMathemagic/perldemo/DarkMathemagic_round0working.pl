#!/usr/bin/perl

#The following is a brief description of what is done in each round
#Round 0: adding and subtracting random 16 bit hex values
#Round 1: adding and subtracting random 32 bit hex values which are limited so that they will not overflow or underflow the 32 bit range
#Round 2: adding and subtracting random 32 bit hex values which can overflow and underflow the 32 bits range
#Round 3: AND, OR, NOT, XOR random 32 bit hex values
#Round 4: multiply and divide random 32 bit hex values
#Round 5: Moving values into memory 
#Round 6: bit setting? (CMP/TEST)

#Interpolation conventions:
#%rx and %ry = two randomly selected registers (from the set eax,ebx,ecx,edx,edi,esi) which cannot both be the same
#interpolated to: $regX and $regY
#%i16 = randomly selected 32 bit integer (0x0 - 0xFFFFFFFF)
#interpolated to: $i16
#%i32 = randomly selected 32 bit integer (0x0 - 0xFFFFFFFF)
#interpolated to: $i32
#%-i32 = same number as $i32 but made negative
#interpolated to: $neg_i32
#%nzi32 = non-zero randomly selected 32 bit integer (0x1 - 0xFFFFFFFF)
#interpolated to: $nonZero_i32
#%lti32 = number less than the selected %i32
#interpolated to: $lessThani32
#%ltnzi32 = number less than the selected %nzi32
#interpolated to: $lessThanNonZeroi32
#%noltnzi32 = value less than %nxi32 which can be added to %nzi32 and not cause an overflow
#interpolated to: $nonOverflowingLessThanNonZeroi32
#%nultnzi32 = value less than %nzi32 which can be subtracted from %nzi32 and not cause an underflow
#interpolated to: $nonUnerflowingLessThanNonZeroi32


#***************************
#********ROUND 0************
#***************************

#These are the asm statements the user will see
@round0Asm = (	"mov %rx,%nzi16\nadd %rx, %ltnzi16", 
		"mov %rx,%nzi16\nmov %ry, %ltnzi16\nadd %rx, %ry",
		"mov %rx,%nzi16\nsub %rx, %ltnzi16", 
		"mov %rx,%nzi16\nmov %ry, %ltnzi16\nsub %rx, %ry");

#These are the perl statements which do the equivalent math behind the scenes.
#The statements should use variable names which will already exist in the function asmInterpolate()
@round0Perl = (	'$result = $nonZero_i16 + $lessThanNonZeroi16',
		'$result = $nonZero_i16 + $lessThanNonZeroi16',
		'$result = $nonZero_i16 - $lessThanNonZeroi16',
		'$result = $nonZero_i16 - $lessThanNonZeroi16');

#***************************
#********ROUND 1************
#***************************

#These are the asm statements the user will see
@round1Asm = (	"mov %rx,%nzi32\nadd %rx, %noltnzi32", 
		"mov %rx,%nzi32\nmov %ry, %noltnzi32\nadd %rx, %ry",
		"mov %rx,%nzi32\nsub %rx, %noltnzi32", 
		"mov %rx,%nzi32\nmov %ry, %noltnzi32\nsub %rx, %ry");

#These are the perl statements which do the equivalent math behind the scenes.
#The statements should use variable names which will already exist in the function asmInterpolate()
@round1Perl = (	'$result = $nonZero_i32 + $nonOverflowingLessThanNonZeroi32',
		'$result = $nonZero_i32 + $nonOverflowingLessThanNonZeroi32',
		'$result = $nonZero_i32 - $nonUnderflowingLessThanNonZeroi32',
		'$result = $nonZero_i32 - $nonUnderflowingLessThanNonZeroi32');

#The indices for the @round1Asm statements have to match the indices for the @round1Eval statements
#otherwise the math won't work out

#***************************
#********ROUND 2************
#***************************

@round2Asm = (	"mov %rx,%nzi32\nadd %rx, %ltnzi32", 
		"mov %rx,%nzi32\nmov %ry, %ltnzi32\nadd %rx, %ry",
		"mov %rx,%nzi32\nsub %rx, %ltnzi32", 
		"mov %rx,%nzi32\nmov %ry, %ltnzi32\nsub %rx, %ry");

#These are the perl statements which do the equivalent math behind the scenes.
#The statements should use variable names which will already exist in the function asmInterpolate()
@round2Perl = (	"$result = $nonZero_i32 + $lessThanNonZeroi32",
		"$result = $nonZero_i32 + $lessThanNonZeroi32",
		"$result = $nonZero_i32 - $lessThanNonZeroi32",
		"$result = $nonZero_i32 - $lessThanNonZeroi32");

#***************************
#********ROUND 3************
#***************************



#			"sub %rx,%rx", "mov %rx,%nzi32\nsub %rx,%nzi32", "mov %rx,0\nsub %rx,0",
#			"mov %rx,%nzi32\nsub %nzi32,%rx", "mov %rx,%nzi32\nxor %nzi32,%rx");
#			"cmp %nzi32,%ltnzi32", "mov %rx,%ltnzi32\ncmp %nzi32,%rx", "mov %rx,%ltnzi32\ncmp %rx,%nzi32",
#			"mov %rx,%nzi32\nxor %rx,%ltnzi32", "mov %rx,%nzi32\nxor %ltnzi32,%rx", 
#			"mov %rx,%ltnzi32\nsub %nzi32,%rx", "mov %rx,%ltnzi32\nsub %rx,%nzi32",
#			"mov %rx,%ltnzi32\nadd %nzi32,%rx", "mov %rx,%ltnzi32\nadd %rx,%nzi32");
#
#
#			"push %nzi32\npop %rx\nxor %rx,%rx",
#			"push %nzi32\nmov %ry,%ltnzi32\npop %rx\nxor %rx,%rx",
#			"mov %rx,%nzi32\nmov %nzi32\nxor %rx,%ry");
#			"push %nzi32\npop %rx\nxor %rx,%ltnzi32", 
#			"push %nzi32\nmov %ry,%ltnzi32\npop %rx\nxor %rx,%ltnzi32", 
#			"push %ltnzi32\npop %rx\nxor %rx,%nzi32");
#

print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n";
print "Welcome to the perl demo of DarkMathemagic!\n";
print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n";
print "In this game of skill, you will evaluate increasingly \n";
print "complex assembly statements in order to determine what\n";
print "value will be held in a given register after the code\n";
print "is evaluated by a processor. Enter the hex value of the\n";
print "register which is asked for.\n";
print "Try to do this first round by hand, and then you can use\n";
print "a calculator on subsequent rounds.\n";
print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n";
print "ROUND 0: 1000 points needed to pass\n";


$MAX_32BIT_INT = 0xFFFFFFFF;
srand();
$currentScore = 0;


while($currentScore < 1000){
	$numStatements = @round0Asm;
	$randIndex = int(rand($numStatements));
	$randomAsm = $round0Asm[$randIndex];
	$randomEval = $round0Perl[$randIndex];
	if(asmInterpolate($randomAsm,$randomEval)){
		$currentScore += 100;
		print "You gained 100 points, and now have $currentScore points\n";
	}
	else{
		$currentScore -= 200;
		print "You lost 200 points, and now have $currentScore points\n";
	}


}
print "-------------LEVEL 0 COMPLETED---------------\n";
print "On to round 1!\n";
print "ROUND 1: 2000 points needed to pass\n";

#while($currentScore < 2000){

#}
print "-------------LEVEL 1 COMPLETED---------------\n";
print "On to round 3!\n";
print "ROUND 2: 4000 points needed to pass\n";

#while($currentScore < 4000){

#}
print "-------------LEVEL 2 COMPLETED---------------\n";
print "WINNER WINNER CHICKEN DINNER!\n";
print "That's all for now. Check out the code and think about how\n";
print "to turn this into a real game!\n";
print "http://www.ascii-fr.com/-Chicken-.html\n";
print "      ,~.\n";
print "   ,-'__ `-,\n";
print "  {,-'  `. }              ,')\n";
print " ,( a )   `-.__         ,',')~,\n";
print "<=.) (         `-.__,==' ' ' '}\n";
print "  (   )                      /)\n";
print "   `-'\\   ,                    )\n";
print "       |  \\        `~.        /\n";
print "       \\   `._        \\      /\n";
print "        \\     `._____,'    ,'\n";
print "         `-.             ,'\n";
print "            `-._     _,-'\n";
print "                77jj'\n";
print "               //_||\n";
print "            __//--'/`          hjw\n";
print "          ,--'/`  '\n";

exit($currentScore);

####################################
#SUBROUTINES
####################################

sub min{
	if($_[0] <= $_[1]){
		return $_[0];
	}
	else {return $_[1];}
}

sub asmInterpolate{
	$asmString = $_[0];
	$evalString = $_[1];

	#16 BIT VALUES
	#used for %i16
	$i16 = int(rand(0x10000));
	$i16_hexstr = sprintf("0x%04x",$i16);
	#used for %nzi16
	$nonZero_i16 = int(rand(0xFFFF))+1;
	$nonZero_i16_hexstr = sprintf("0x%04x", $nonZero_i16);
	#used for %lti16
	$lessThani16 = int(rand($i16));
	$lessThani16_hexstr = sprintf("0x%04x",$lessThani16);
	#used for %ltnzi16
	$lessThanNonZeroi16 = int(rand($nonZero_i16));
	$lessThanNonZeroi16_hexstr = sprintf("0x%04x",$lessThanNonZeroi16);

	#32 BIT VALUES
	#used for %i32
	$i32 = int(rand(0x100000000));
	$i32_hexstr = sprintf("0x%08x",$i32);
	#used for %-i32
	$neg_i32 = -$i32;
	$neg_i32_hexstr = sprintf("0x%08x",$neg_i32);
	#used for %nzi32
	$nonZero_i32 = int(rand(0xFFFFFFFF))+1;
	$nonZero_i32_hexstr = sprintf("0x%08x", $nonZero_i32);
	#used for %lti32
	$lessThani32 = int(rand($i32));
	$lessThani32_hexstr = sprintf("0x%08x",$lessThani32);
	#used for %ltnzi32
	$lessThanNonZeroi32 = int(rand($nonZero_i32));
	$lessThanNonZeroi32_hexstr = sprintf("0x%08x",$lessThanNonZeroi32);
	#used for %noltnzi32
	$nonOverflowingLessThanNonZeroi32 = int(rand(min($nonZero_i32, ($MAX_32BIT_INT - $nonZero_i32))));
	$nonOverflowingLessThanNonZeroi32_hexstr = sprintf("0x%08x",$nonOverflowingLessThanNonZeroi32);
	#used for %nultnzi32
	$nonUnderflowingLessThanNonZeroi32 = int(rand(min($nonZero_i32, ($MAX_32BIT_INT - $nonZero_i32))));
	$nonUnderflowingLessThanNonZeroi32_hexstr = sprintf("0x%08x",$nonUnderflowingLessThanNonZeroi32);

	#pick some useful registers
	@generalRegisters = ("eax", "ebx", "ecx", "edx", "edi", "esi");
	$numRegs = @generalRegisters;
	#used for %rx
	$regX = $generalRegisters[int(rand($numRegs))];
	#used for %ry
	$regY = $regX;
	#Want to make sure it's different
	while($regY eq $regX){
		$regY = $generalRegisters[int(rand($numRegs))];
	}

	$asmString =~ s/%rx/$regX/g;
	$asmString =~ s/%ry/$regY/g;

	$asmString =~ s/%i16/$i16_hexstr/g;
	$asmString =~ s/%nzi16/$nonZero_i16_hexstr/g;
	$asmString =~ s/%lti16/$lessThani16_hexstr/g;
	$asmString =~ s/%ltnzi16/$lessThanNonZeroi16_hexstr/g;

	$asmString =~ s/%i32/$i32_hexstr/g;
	$asmString =~ s/%-i32/$neg_i32_hexstr/g;
	$asmString =~ s/%nzi32/$nonZero_i32_hexstr/g;
	$asmString =~ s/%lti32/$lessThani32_hexstr/g;
	$asmString =~ s/%ltnzi32/$lessThanNonZeroi32_hexstr/g;
	$asmString =~ s/%noltnzi32/$nonOverflowingLessThanNonZeroi32_hexstr/g;
	$asmString =~ s/%nultnzi32/$nonUnderflowingLessThanNonZeroi32_hexstr/g;
	print "$asmString\n";

	eval $evalString;

	print "Enter the hex value (preceeded by 0x) in the $regX register: ";
	chomp($userInput = <STDIN>);
	
        if(hex($userInput) == $result){
                printf("%#x is correct! :D \n", $userInput);
                return 1;
        }
        else{
                printf("%#x is incorrect :( Answer was %#x\n", $userInput, $result);
                return 0;
        }

}
