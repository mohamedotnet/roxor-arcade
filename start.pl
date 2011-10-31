#!/usr/bin/perl

use Switch;

print("GREETINGS PROFESSOR X\n");
print("SHALL WE PLAY A GAME?\n");
system("say 'GREETINGS PROFESSOR X'");
system("say 'SHALL WE PLAY A GAME?'");

$currentScore = 0;

print("  _   _   _   _   _   _   _  \n");
print(" / \\ / \\ / \\ / \\ / \\ / \\ / \\ \n");
print("( W | e | l | c | o | m | e )\n");
print(" \\_/ \\_/ \\_/ \\_/ \\_/ \\_/ \\_/ \n");
print("\n");
print(" ____  _____ \n");
print("(_  _)(  _  )\n");
print("  )(   )(_)( \n");
print(" (__) (_____)\n");
print("\n");
print("RRRR   OOO  X   X  OOO   RRRR  \n");
print("R   R O   O  X X  O   O R   R  \n");
print("RRRR  O   O   X   O   O  RRRR  \n");
print("R R   O   O  X X  O   O   R R  \n");
print("R  RR  OOO  X   X  OOO  RR  R  \n");
print("\n");
print("    :::     :::::::::   ::::::::      :::     :::::::::  :::::::::: \n");
print("  :+: :+:   :+:    :+: :+:    :+:   :+: :+:   :+:    :+: :+:        \n");
print(" +:+   +:+  +:+    +:+ +:+         +:+   +:+  +:+    +:+ +:+        \n");
print("+#++:++#++: +#++:++#:  +#+        +#++:++#++: +#+    +:+ +#++:++#   \n");
print("+#+     +#+ +#+    +#+ +#+        +#+     +#+ +#+    +#+ +#+        \n");
print("#+#     #+# #+#    #+# #+#    #+# #+#     #+# #+#    #+# #+#        \n");
print("###     ### ###    ###  ########  ###     ### #########  ########## \n");


while(1){
	print("Current Score = $currentScore\n\n");
	print("What would you like to play?\n");
	print("0) BinDeciHex\n");
	print("1) One step forward, 3 steps back\n");
	print("2) The *other* ESP game\n");
	print("3) Global Thermonuclear War\n");
	print("q) Quit\n");

	print("enter choice> ");
	chomp($userInput = <STDIN>);

	switch($userInput){
	case 0 {
		#thanks to the return value limitations, I can't handle a return value > +127, -128
		#and I'm too lazy to find another way
		$returnScore = system("perl BinDeciHex/perldemo/BinDeciHex.pl");
		$returnScore = ($returnScore >> 8);
		if($returnScore & 128){
			$returnScore = 256 - $returnScore;
			$returnScore *= -100;
		}
		else{
			$returnScore *= 100;
		}
		#print("returnScore = $returnScore\n");
		$currentScore += $returnScore;
	}
	case 0 {
		$returnScore = system("perl 1step3step/perldemo/1step3step_round3working.pl");
		$returnScore = ($returnScore >> 8);
		if($returnScore & 128){
			$returnScore = 256 - $returnScore;
			$returnScore *= -100;
		}
		else{
			$returnScore *= 100;
		}
		#print("returnScore = $returnScore\n");
		$currentScore += $returnScore;
	}
	case 1 {
		$returnScore = system("perl TheOtherESPGame/perldemo/otherESPgame_full.pl");
		$returnScore = ($returnScore >> 8);
		if($returnScore & 128){
			$returnScore = 256 - $returnScore;
			$returnScore *= -100;
		}
		else{
			$returnScore *= 100;
		}
		#print("returnScore = $returnScore\n");
		$currentScore += $returnScore;
	}
	case 2 {
		print ("Are you sure you wouldn't prefer a good game of chess?\n");
		system("say \"Are you sure you wouldn't prefer a good game of chess?\"");
		chomp($userInput = <STDIN>);
		print ("Guess what? Nobody cares what you want. Go contemplate your mortality, meatsack. :P\n");
		exit(0x0ddba11);
	}
	case 'q' {
		print "A curious arcade. The only winning move is to play a LOT!\n";
		exit(0x31337);
	}
	else{
		print "I'm sorry this is confusing to you. Maybe you can ask your mommy to help you with the 'puter?\n";
		exit(0xbeefface);
	}
	}#end switch
}
