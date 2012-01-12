#!/usr/bin/perl

use Switch;

print("GREETINGS PROFESSOR X\n");
print("SHALL WE PLAY A GAME?\n");
system("say 'GREETINGS PROFESSOR X'");
system("say 'SHALL WE PLAY A GAME?'");

$currentScore = 0;

#http://www.network-science.de/ascii/

print(":::       ::: :::::::::: :::        ::::::::   ::::::::  ::::    ::::  :::::::::: \n");
print(":+:       :+: :+:        :+:       :+:    :+: :+:    :+: +:+:+: :+:+:+ :+:        \n");
print("+:+       +:+ +:+        +:+       +:+        +:+    +:+ +:+ +:+:+ +:+ +:+        \n");
print("+#+  +:+  +#+ +#++:++#   +#+       +#+        +#+    +:+ +#+  +:+  +#+ +#++:++#   \n");
print("+#+ +#+#+ +#+ +#+        +#+       +#+        +#+    +#+ +#+       +#+ +#+        \n");
print(" #+#+# #+#+#  #+#        #+#       #+#    #+# #+#    #+# #+#       #+# #+#        \n");
print("  ###   ###   ########## ########## ########   ########  ###       ### ########## \n");
print("\n");
print("                              ::::::::::: ::::::::  \n");
print("                                  :+:    :+:    :+: \n");
print("                                  +:+    +:+    +:+ \n");
print("                                  +#+    +#+    +:+ \n");
print("                                  +#+    +#+    +#+ \n");
print("                                  #+#    #+#    #+# \n");
print("                                  ###     ########  \n");
print("\n");
print("              :::::::::   ::::::::  :::    :::  ::::::::   ::::::::: \n");
print("              :+:    :+: :+:    :+: :+:    :+: :+:    :+: :+:    :+: \n");
print("              +:+    +:+ +:+    +:+  +:+  +:+  +:+    +:+ +:+    +:+ \n");
print("              +#++:++#:  +#+    +:+   +#++:+   +#+    +:+  :#++:++#+ \n");
print("              +#+    +#+ +#+    +#+  +#+  +#+  +#+    +#+ +#+    +#+ \n");
print("              #+#    #+# #+#    #+# #+#    #+# #+#    #+# #+#    #+# \n");
print("              ###    ###  ########  ###    ###  ########  ###    ### \n");
print("\n");
print("            :::     :::::::::   ::::::::      :::     :::::::::  :::::::::: \n");
print("          :+: :+:   :+:    :+: :+:    :+:   :+: :+:   :+:    :+: :+:        \n");
print("         +:+   +:+  +:+    +:+ +:+         +:+   +:+  +:+    +:+ +:+        \n");
print("        +#++:++#++: +#++:++#:  +#+        +#++:++#++: +#+    +:+ +#++:++#   \n");
print("        +#+     +#+ +#+    +#+ +#+        +#+     +#+ +#+    +#+ +#+        \n");
print("        #+#     #+# #+#    #+# #+#    #+# #+#     #+# #+#    #+# #+#        \n");
print("        ###     ### ###    ###  ########  ###     ### #########  ########## \n");


while(1){
	print("Current Score = $currentScore\n\n");
	print("What would you like to play?\n");
	print("0) BinDeciHex\n");
	print("1) DarkMathemagic\n");
	print("2) One step forward, 3 steps back\n");
	print("3) The *other* ESP game\n");
	print("4) Global Thermonuclear War\n");
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
	case 1 {
		#DarkMathemagic
		$returnScore = system("perl DarkMathemagic/perldemo/DarkMathemagic_round1working.pl");
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
	case 3 {
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
	case 4 {
		print ("Are you sure you wouldn't prefer a good game of chess?\n");
		system("say \"Are you sure you wouldn't prefer a good game of chess?\"");
		chomp($userInput = <STDIN>);
		print ("Guess what? Nobody cares what you want. Go contemplate your mortality, meatsack. :P\n");
		system(" say \"Guess what? Nobody cares what you want. Go contemplate your mortality, meatsack. :P\"");
		exit(0x0ddba11);
	}
	case 'q' {
		print "A curious arcade. The only winning move is to play a LOT!\n";
		system(" say \"A curious arcade. The only winning move is to play a LOT!\"");
		exit(0x31337);
	}
	else{
		print "I'm sorry this is confusing to you. Maybe you can ask your mommy to help you with the 'puter?\n";
		exit(0xbeefface);
	}
	}#end switch
}
