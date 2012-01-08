#!/usr/bin/perl

#Round 1: Conditionals: jz(ZF==1), jnz(ZF==0), ja(CF==0 AND ZF==0), jb(CF==1)
#Round 2: Add new mnemonics for same conditionals: jz/je(ZF==1), jnz/jne(ZF==0), ja/jnbe(CF==0 AND ZF==0), jb/jnae(CF==1)
#Round 3: New instructions for previous round conditionals + new conditionals: jb/jnae/jc(CF==1), jae/jnc(CF==0), jbe/jna(CF==1 OR ZF==1)
#Round 4: New instructions + new conditionals: jg/jnle(ZF==0 AND SF==OF), jge/jnl(SF==OF), jl/jnge(SF!=OF), jle/jng(ZF==1 OR SF!=OF)
#Round 5: New instructions + new conditionals: jo(OF==1), jno(OF!=1), jp/jpe(PF==1), jnp/jpo(PF!=1)
#Round 6: New instructions + new conditionals: js(SF==1), jns(SF!=1), jecxz(register ecx == 0)

#***************************
#********ROUND 1************
#***************************

@round1Condition1 = 	("jz (ZF==1)");
@round1TrueAsm1 = (	"xor %rx,%rx");
@round1FalseAsm1 = (	"mov %rx,%lti32\nxor %rx,%i32", 
			"mov %rx,%nzi32\nadd %rx,%nzi32");

@round1Condition2 = 	("jnz (ZF==0)");
@round1TrueAsm2 = 	@round1FalseAsm1;
@round1FalseAsm2 = 	@round1TrueAsm1;

@round1Condition3 = (	"ja (CF==0 AND ZF==0)");
@round1TrueAsm3 = (	"mov %rx,%nzi32\ncmp %rx,%ltnzi32", 
			"mov %rx,%nzi32\nsub %rx,%ltnzi32");
@round1FalseAsm3 = (	"mov %rx,%ltnzi32\ncmp %rx,%nzi32", 
			"mov %rx,%ltnzi32\nsub%rx,%nzi32");

@round1Condition4 = 	("jb (CF==1)");
@round1TrueAsm4 =	@round1FalseAsm3;
@round1FalseAsm4 =	@round1TrueAsm3;


%round1TrueHash = ( @round1Condition1 => \@round1TrueAsm1, @round1Condition2 => \@round1TrueAsm2, @round1Condition3 => \@round1TrueAsm3, @round1Condition4 => \@round1TrueAsm4);
%round1FalseHash = ( @round1Condition1 => \@round1FalseAsm1, @round1Condition2 => \@round1FalseAsm2, @round1Condition3 => \@round1FalseAsm3, @round1Condition4 => \@round1FalseAsm4);

#***************************
#********ROUND 2************
#***************************

my @round2Condition1 =	("jz (ZF==1)","je (ZF==1)");
my @round2TrueAsm1 = (	@round1TrueAsm1, 
			"sub %rx,%rx", 
			"mov %rx,%nzi32\nsub %rx,%nzi32", 
			"mov %rx,0\nsub %rx,0",
			"mov %rx,%nzi32\nxor %rx,%nzi32");
my @round2FalseAsm1 = (	@round1FalseAsm1, 
			"cmp %nzi32,%ltnzi32", 
			"mov %rx,%ltnzi32\ncmp %rx,%nzi32",
			"mov %rx,%nzi32\nxor %rx,%ltnzi32", 
			"mov %rx,%ltnzi32\nsub %rx,%nzi32", 
			"mov %rx,%ltnzi32\nadd %rx,%nzi32");

my @round2Condition2 =	("jnz (ZF==0)", "jne (ZF==0)");
my @round2TrueAsm2 =	@round2FalseAsm1;
my @round2FalseAsm2 =	@round2TrueAsm1;

my @round2Condition3 = 	("ja (CF==0 AND ZF==0)","jnbe (CF==0 AND ZF==0)");
my @round2TrueAsm3 = (	@round1TrueAsm3, 
			"mov %rx,%nzi32\nsub %rx,%ltnzi32",
			"mov %rx,%nzi32\ncmp %rx,%ltnzi32");
my @round2FalseAsm3 = (	@round1FalseAsm3, 
			"mov %rx,%ltnzi32\nsub %rx,%nzi32",
			"mov %rx,%ltnzi32\ncmp %rx,%nzi32");

my @round2Condition4 = 	("jb (CF==1)","jnae (CF==1)");
my @round2TrueAsm4 =	@round2FalseAsm3;
my @round2FalseAsm4 =	@round2TrueAsm3;

my %round2TrueHash = ( join('-',@round2Condition1) => \@round2TrueAsm1, join('-',@round2Condition2) => \@round2TrueAsm2, join('-',@round2Condition3) => \@round2TrueAsm3, join('-',@round2Condition4) => \@round2TrueAsm4);
my %round2FalseHash = ( join('-',@round2Condition1) => \@round2FalseAsm1, join('-',@round2Condition2) => \@round2FalseAsm2, join('-',@round2Condition3) => \@round2FalseAsm3, join('-',@round2Condition4) => \@round2FalseAsm4);

#***************************
#********ROUND 3************
#***************************

my @round3Condition1 =	("jz (ZF==0)","je (ZF==0)");
my @round3TrueAsm1 = (	@round2TrueAsm1, 
			"push %nzi32\npop %rx\nxor %rx,%rx",
			"push %nzi32\nmov %ry,%ltnzi32\npop %rx\nxor %rx,%rx",
			"mov %rx,%nzi32\nmov %nzi32\nxor %rx,%ry");
my @round3FalseAsm1 = (	@round2FalseAsm1, 
			"push %nzi32\npop %rx\nxor %rx,%ltnzi32", 
			"push %nzi32\nmov %ry,%ltnzi32\npop %rx\nxor %rx,%ltnzi32", 
			"push %ltnzi32\npop %rx\nxor %rx,%nzi32");

my @round3Condition2 =	("jnz (ZF==1)", "jne (ZF==1)");
my @round3TrueAsm2 = 	@round3FalseAsm1;
my @round3FalseAsm2 = 	@round3TrueAsm1;

my @round3Condition3 = 	("ja (CF==0 AND ZF==0)","jnbe (CF==0 AND ZF==0)");
my @round3TrueAsm3 = (	@round2TrueAsm3, 
			"mov %rx,%ltnzi32\nsub %nzi32,%rx",
			"mov %rx,%ltnzi32\ncmp %nzi32,%rx");
#none of these will actually ever fail due to ZF==1, so it's safe to use them for just assuming CF==1
my @round3FalseAsm3 = (	@round2FalseAsm3, 
			"mov %rx,%ltnzi32\nsub %rx,%nzi32",
			"mov %rx,%ltnzi32\ncmp %rx,%nzi32");

my @round3Condition4 = ("jb (CF==1)","jnae (CF==1)", "jc (CF == 1)");
my @round3TrueAsm4 =	@round3FalseAsm3;
my @round3FalseAsm4 =	@round3TrueAsm3;

my @round3Condition5 = ("jae (CF==0)", "jnc (CF==0)");
my @round3TrueAsm5 =	@round3TrueAsm3;
my @round3FalseAsm5 =	@round3FalseAsm3;

my @round3Condition6 = 	("jbe (CF==1 OR ZF==1)", "jna (CF==1 OR ZF==1)");
my @round3TrueAsm6 = (	@round3TrueAsm4, @round3TrueAsm2); #all results have CF==1 or ZF==1
my @round3FalseAsm6 = (	@round3TrueAsm3, @round3FalseAsm2); #all results have CF==0 or ZF==0

my %round3TrueHash = ( join('-',@round3Condition1) => \@round3TrueAsm1, join('-',@round3Condition2) => \@round3TrueAsm2, join('-',@round3Condition3) => \@round3TrueAsm3, join('-',@round3Condition4) => \@round3TrueAsm4, join('-',@round3Condition5) => \@round3TrueAsm5, join('-',@round3Condition6) => \@round3TrueAsm6);
my %round3FalseHash = ( join('-',@round3Condition1) => \@round3FalseAsm1, join('-',@round3Condition2) => \@round3FalseAsm2, join('-',@round3Condition3) => \@round3FalseAsm3, join('-',@round3Condition4) => \@round3FalseAsm4, join('-',@round3Condition5) => \@round3FalseAsm5, join('-',@round3Condition6) => \@round3FalseAsm6);

srand();

$SIG{INT} = \&forceExit;
$currentScore = 0;

print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n";
print "Welcome to the perl demo of 1 step forward, 3 steps back!\n";
print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n";
print "In this game of skill, you will reverse engineer\n";
print "increasingly complex assembly statements, in order to\n";
print "determine whether a conditional statement will evaluate\n";
print "to true or not. Press 1 if you think the jump will be\n";
print "taken, press 0 if you think it will not be taken.\n";
print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n";
print "ROUND 1: 1000 points needed to pass\n";


while($currentScore < 1000){
	$conditionTruth = int(rand(2));
#	print "conditionTruth = $conditionTruth\n";
	if($conditionTruth){
		#This is where we're using round1TrueHash
		#print "trying to print the hash" . keys(%round1TrueHash) . "\n";
		@roundKeys = keys %round1TrueHash;
		$tmp = @roundKeys;
		#print "number of keys in round1TrueHash = $tmp \n";
		#print "roundKeys = @roundKeys \n";
		$condition = int(rand($tmp));
		#print "random condition = $condition\n";
		@key = $roundKeys[$condition];
		#print "we randomly selected key @key \n";
		$tmp = @round1TrueHash{@key};
		@asmStatements = @$tmp;
		#print "asmStatements = @asmStatements\n";
		$numStatements = @asmStatements;
		$randStatement = int(rand($numStatements));
		print "------------\n";
		$randomStatement = $asmStatements[$randStatement];
		$interpolatedAsmStatement = asmInterpolate($randomStatement);
		print "$interpolatedAsmStatement\n";
#		print "$randomStatement\n";
		print "@key\n";	
	}
	else{
		#This is where we're using round1FalseHash
		@roundKeys = keys %round1FalseHash;
		$tmp = @roundKeys;
		$condition = int(rand($tmp));
		@key = $roundKeys[$condition];
		$tmp = @round1FalseHash{@key};
		@asmStatements = @$tmp;
		$numStatements = @asmStatements;
		$randStatement = int(rand($numStatements));
		print "------------\n";
		$randomStatement = $asmStatements[$randStatement];
		$interpolatedAsmStatement = asmInterpolate($randomStatement);
		print "$interpolatedAsmStatement\n";
#		print "$randomStatement\n";
		print "@key\n";
	}

	print "Enter q to quit.\n";
	print "If the condition will be taken, enter 1, otherwise enter 0: ";
	chomp($userInput = <STDIN>);
	if($userInput eq 'q'){
		$currentScore = $currentScore / 100;
		exit($currentScore);
	}
	if($userInput == $conditionTruth){
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
print "-------------LEVEL 1 COMPLETED---------------\n";
print "On to round 2!\n";
print "ROUND 2: 2000 points needed to pass\n";

while($currentScore < 2000){
	$conditionTruth = int(rand(2));
#	print "conditionTruth = $conditionTruth\n";
	if($conditionTruth){
		#This is where we're using round1TrueHash
		#print "trying to print the hash" . keys(%round2TrueHash) . "\n";
		@roundKeys = keys %round2TrueHash;
		$tmp = @roundKeys;
		#print "number of keys in round2TrueHash = $tmp \n";
		#print "roundKeys = @roundKeys \n";
		$condition = int(rand($tmp));
		#print "random condition = $condition\n";
		$tmpRef = $roundKeys[$condition];
		#print "tmpRef = $tmpRef\n";
		@mnemonics = split('-',$tmpRef);
		#print "mnemonics = @mnemonics\n";
		$numMnemonics = @mnemonics;
		$randMnemonic = int(rand($numMnemonics));
		#print "randMnemonic = $randMnemonic\n";
		$mnemonic = $mnemonics[$randMnemonic];
		#print "we randomly selected key $mnemonic \n";
		$tmp = @round2TrueHash{$tmpRef};
		@asmStatements = @$tmp;
		#print "asmStatements = @asmStatements\n";
		$numStatements = @asmStatements;
		$randStatement = int(rand($numStatements));
		print "------------\n";
		$randomStatement = $asmStatements[$randStatement];
		$interpolatedAsmStatement = asmInterpolate($randomStatement);
		print "$interpolatedAsmStatement\n";
#		print "$randomStatement\n";
		print "$mnemonic\n";	
	}
	else{
		#This is where we're using round1TrueHash
		@roundKeys = keys %round2FalseHash;
		$tmp = @roundKeys;
		$condition = int(rand($tmp));
		$tmpRef = $roundKeys[$condition];
		@mnemonics = split('-',$tmpRef);
		$numMnemonics = @mnemonics;
		$randMnemonic = int(rand($numMnemonics));
		$mnemonic = $mnemonics[$randMnemonic];
		$tmp = @round2FalseHash{$tmpRef};
		@asmStatements = @$tmp;
		$numStatements = @asmStatements;
		$randStatement = int(rand($numStatements));
		print "------------\n";
		$randomStatement = $asmStatements[$randStatement];
		$interpolatedAsmStatement = asmInterpolate($randomStatement);
		print "$interpolatedAsmStatement\n";
#		print "$randomStatement\n";
		print "$mnemonic\n";	
	}

	print "Enter q to quit.\n";
	print "If the condition will be taken, enter 1, otherwise enter 0: ";
	chomp($userInput = <STDIN>);
	if($userInput eq 'q'){
		exit($currentScore);
	}
	if($userInput == $conditionTruth){
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
print "-------------LEVEL 2 COMPLETED---------------\n";
print "On to round 3!\n";
print "ROUND 3: 4000 points needed to pass\n";

while($currentScore < 4000){
	$conditionTruth = int(rand(2));
#	print "conditionTruth = $conditionTruth\n";
	if($conditionTruth){
		#This is where we're using round3TrueHash
		#print "trying to print the hash" . keys(%round3TrueHash) . "\n";
		@roundKeys = keys %round3TrueHash;
		$tmp = @roundKeys;
		#print "number of keys in round2FalseHash = $tmp \n";
		#print "roundKeys = @roundKeys \n";
		$condition = int(rand($tmp));
		#print "random condition = $condition\n";
		$tmpRef = $roundKeys[$condition];
		#print "tmpRef = $tmpRef\n";
		@mnemonics = split('-',$tmpRef);
		#print "mnemonics = @mnemonics\n";
		$numMnemonics = @mnemonics;
		$randMnemonic = int(rand($numMnemonics));
		#print "randMnemonic = $randMnemonic\n";
		$mnemonic = $mnemonics[$randMnemonic];
		#print "we randomly selected key $mnemonic \n";
		$tmp = @round3TrueHash{$tmpRef};
		@asmStatements = @$tmp;
		#print "asmStatements = @asmStatements\n";
		$numStatements = @asmStatements;
		$randStatement = int(rand($numStatements));
		print "------------\n";
		$randomStatement = $asmStatements[$randStatement];
		$interpolatedAsmStatement = asmInterpolate($randomStatement);
		print "$interpolatedAsmStatement\n";
		#print "$randomStatement\n";
		print "$mnemonic\n";	
	}
	else{
		#This is where we're using round3TrueHash
		#print "trying to print the hash" . keys(%round3TrueHash) . "\n";
		@roundKeys = keys %round3FalseHash;
		$tmp = @roundKeys;
		#print "number of keys in round3FalseHash = $tmp \n";
		#print "roundKeys = @roundKeys \n";
		$condition = int(rand($tmp));
		#print "random condition = $condition\n";
		$tmpRef = $roundKeys[$condition];
		#print "tmpRef = $tmpRef\n";
		@mnemonics = split('-',$tmpRef);
		#print "mnemonics = @mnemonics\n";
		$numMnemonics = @mnemonics;
		$randMnemonic = int(rand($numMnemonics));
		#print "randMnemonic = $randMnemonic\n";
		$mnemonic = $mnemonics[$randMnemonic];
		#print "we randomly selected key $mnemonic \n";
		$tmp = @round3FalseHash{$tmpRef};
		@asmStatements = @$tmp;
		#print "asmStatements = @asmStatements\n";
		$numStatements = @asmStatements;
		$randStatement = int(rand($numStatements));
		print "------------\n";
		$randomStatement = $asmStatements[$randStatement];
		$interpolatedAsmStatement = asmInterpolate($randomStatement);
		print "$interpolatedAsmStatement\n";
		#print "$randomStatement\n";
		print "$mnemonic\n";	
	}

	print "Enter q to quit.\n";
	print "If the condition will be taken, enter 1, otherwise enter 0: ";
	chomp($userInput = <STDIN>);
	if($userInput eq 'q'){
		exit($currentScore);
	}
	if($userInput == $conditionTruth){
		print "Correct! :D \n";
		$currentScore += 400;
		print "You gained 400 points, and now have $currentScore points\n";
	}
	else{
		print "Incorrect :( \n";
		$currentScore -= 800;
		print "You lost 800 points, and now have $currentScore points\n";
	}
}
print "-------------LEVEL 3 COMPLETED---------------\n";
print "WINNER WINNER CHICKEN DINNER!\n";
print "That's all for now. Check out the code and think about how\n";
print "to turn this into a real game!\n";


sub asmInterpolate{
	$asmString = $_[0];

	#pick some useful constants
	#used for %i32
	$i32 = int(rand(0x100000000));
	$i32_hexstr = sprintf("0x%08x",$i32);
#	print "i32 = $i32_hexstr\n";
	#used for %-i32
	$neg_i32 = -$i32;
	$neg_i32_hexstr = sprintf("0x%08x",$neg_i32);
#	print "neg_i32 = $neg_i32_hexstr\n";
	#used for %nzi32
	$nonZero_i32 = int(rand(0xFFFFFFFF))+1;
	$nonZero_i32_hexstr = sprintf("0x%08x", $nonZero_i32);
#	print "nonZero_i32 = $nonZero_i32_hexstr\n";
	#used for %lti32
	$lessThani32 = int(rand($i32));
	$lessThani32_hexstr = sprintf("0x%08x",$lessThani32);
#	print "lessThani32 = $lessThani32_hexstr\n";
	#used for %ltnzi32
	$lessThanNonZeroi32 = int(rand($nonZero_i32));
	$lessThanNonZeroi32_hexstr = sprintf("0x%08x",$lessThanNonZeroi32);
#	print "lessThanNonZeroi32 = $lessThanNonZeroi32_hexstr\n";

	#pick some useful registers
	@generalRegisters = ("eax", "ebx", "ecx", "edx", "edi", "esi");
	$numRegs = @generalRegisters;
	#used for %rx
	$regX = $generalRegisters[int(rand($numRegs))];
	#used for %ry
	$regY = $generalRegisters[int(rand($numRegs))];

#	print "Input string: $asmString\n";
	$asmString =~ s/%rx/$regX/g;
	$asmString =~ s/%ry/$regX/g;
	$asmString =~ s/%i32/$i32_hexstr/g;
	$asmString =~ s/%-i32/$neg_i32_hexstr/g;
	$asmString =~ s/%nzi32/$nonZero_i32_hexstr/g;
	$asmString =~ s/%lti32/$lessThani32_hexstr/g;
	$asmString =~ s/%ltnzi32/$lessThanNonZeroi32_hexstr/g;
#	print "Output string: $asmString\n";

	return $asmString;

}

sub forceExit{
	$currentScore = $currentScore / 100;
	print("caugt SIG{INT}, returning currentScore = $currentScore\n");
	exit($currentScore);
}
