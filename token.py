'''
Created on 27 fevr. 2010

@author: Adrien
'''

import re
import sms2
import csv


def smartTokenizer(filename):
	
	smslines = filename.readlines()
	tokenlines = []
	dico = {'<text_start>':True}

	for line in smslines:
		
		line = preprocess(line)
		
		reSplit = r"(<?\w+>?)"
		reSplit = re.compile(reSplit)
		tokens = reSplit.findall(line)
		
		tokenline = []
		
		for token in tokens:
			if token == '':
				continue
			if token in dico.keys():
				tokenline.append(token)
			else : 
				dico[token] = True
				tokenline.append('<unk>')
		tokenlines.append(tokenline)

	return tokenlines


def tokenizer(filename):
	
	smslines = filename.readlines()
	tokenlines = []

	for line in smslines:
		line = preprocess(line)
		
		reSplit = r"(<?\w+>?)"
		reSplit = re.compile(reSplit)
		tokens = reSplit.findall(line)
		
		tokenline = []
		
		for token in tokens:
			if token == '':
				continue
			tokenline.append(token)
		tokenlines.append(tokenline)

	return tokenlines
	
	# Compute a dictionary of N-grams

def preprocessTraining(tokenlines,lexicon):
	filteredTokens = []
	
	for tokenline in tokenlines :
		filteredLine = []
		for token in tokenline :
			if (token,) in lexicon.keys():
				filteredLine.append(token)
			else : filteredLine.append('<unk>')
		
		filteredTokens.append(filteredLine)
	
	return filteredTokens

def preprocess(line):
	line = line.upper()
		
	line = line.replace(',',' <comma> ')
		
	# les balises ne doivent contenir que du texte pour findall
	line = line.replace('</TEXT>',' <text_end> ')
	line = line.replace('<TEXT>','')
	
	line = line.replace('&APOS;',' <apos> ')
		
	# mots courant
	reMC = r"(?<=\W)(E|DA|D)(?=\W)"
	reMC = re.compile(reMC)
	line = reMC.sub(' THE ',line,count=0)
		
	reMC = r"(?<=\W)(U|YA)(?=\W)"
	reMC = re.compile(reMC)
	line = reMC.sub(' YOU ',line,count=0)
		
	reMC = r"(?<=\W)R(?=\W)"
	reMC = re.compile(reMC)
	line = reMC.sub(' ARE ',line,count=0)
		
	reMC = r"(?<=\W)(N|ND)(?=\W)"
	reMC = re.compile(reMC)
	line = reMC.sub(' AND ',line,count=0)
	
	reMC = r"(?<=\W)B4(?=\W)"
	reMC = re.compile(reMC)
	line = reMC.sub(' BEFORE ',line,count=0)
	
	reMC = r"(?<=\W)C(?=\W)"
	reMC = re.compile(reMC)
	line = reMC.sub(' SEE ',line,count=0)
		
	reMC = r"(?<=\W)(UR|YR)(?=\W)"
	reMC = re.compile(reMC)
	line = reMC.sub(' YOUR ',line,count=0)
		
	reMC = r"(?<=\W)(I\WAM|IAM|IM)(?=\W)"
	reMC = re.compile(reMC)
	line = reMC.sub(' I &APOS; M ',line,count=0)
	
	reMC = r"(?<=\W)(SHLD)(?=\W)"
	reMC = re.compile(reMC)
	line = reMC.sub(' SHOULD ',line,count=0)
	
	reMC = r"(?<=\W)(WIF)(?=\W)"
	reMC = re.compile(reMC)
	line = reMC.sub(' WITH ',line,count=0)
	
	reMC = r"(?<=\W)(AFT)(?=\W)"
	reMC = re.compile(reMC)
	line = reMC.sub(' AFTER ',line,count=0)
	
	reMC = r"(?<=\W)H(M)+(?=\W)"
	reMC = re.compile(reMC)
	line = reMC.sub(' HMM ',line,count=0)
	
	reMC = r"(?<=\W)(MAYB)(?=\W)"
	reMC = re.compile(reMC)
	line = reMC.sub(' MAYBE ',line,count=0)
	
	reMC = r"(?<=\W)(CYA)(?=\W)"
	reMC = re.compile(reMC)
	line = reMC.sub(' SEE YOU ',line,count=0)
	
	reMC = r"(?<=\W)(FREN(S)*|FRIENDS)(?=\W)"
	reMC = re.compile(reMC)
	line = reMC.sub(' FRIEND ',line,count=0)
	
	reMC = r"(?<=\W)(NEVA)(?=\W)"
	reMC = re.compile(reMC)
	line = reMC.sub(' NEVER ',line,count=0)
	
	
	reMC = r"(?<=\W)(COS|COZ)(?=\W)"
	reMC = re.compile(reMC)
	line = reMC.sub(' BECAUSE ',line,count=0)
	
	reMC = r"(?<=\W)(K|OKIE|OKAY)(?=\W)"
	reMC = re.compile(reMC)
	line = reMC.sub(' OK ',line,count=0)
	
	reMC = r"(?<=\W)(DAT|T|TAT|TT)(?=\W)"
	reMC = re.compile(reMC)
	line = reMC.sub(' THAT ',line,count=0)
	
	reMC = r"(?<=\W)(LOH|LA)(?=\W)"
	reMC = re.compile(reMC)
	line = reMC.sub(' LOR ',line,count=0)
	
	
	reMC = r"(?<=\W)(ILL|I\sLL|I\s?<apos>\s?LL)(?=\W)"
	reMC = re.compile(reMC)
	line = reMC.sub(' I WILL ',line,count=0)
	
	reMC = r"(?<=\W)(LL)(?=\W)"
	reMC = re.compile(reMC)
	line = reMC.sub(' WILL ',line,count=0)
	
	reMC = r"(?<=\W)MUZ(?=\W)"
	reMC = re.compile(reMC)
	line = reMC.sub(' MUST ',line,count=0)
	
	reMC = r"(?<=\W)(TIS|DIS)(?=\W)"
	reMC = re.compile(reMC)
	line = reMC.sub(' THIS ',line,count=0)
		
	reMC = r"(?<=\W)(DUN|DUNNO)(?=\W)"
	reMC = re.compile(reMC)
	line = reMC.sub(' DO NOT ',line,count=0)
		
	reMC = r"(?<=\W)NT(?=\W)"
	reMC = re.compile(reMC)
	line = reMC.sub(' NOT ',line,count=0)
		
	reMC = r"(?<=\W)WAT(?=\W)"
	reMC = re.compile(reMC)
	line = reMC.sub(' WHAT ',line,count=0)
		
	reMC = r"(?<=\W)DEN(?=\W)"
	reMC = re.compile(reMC)
	line = reMC.sub(' THEN ',line,count=0)
		
	reMC = r"(?<=\W)(WAN|WANNA|WANA)(?=\W)"
	reMC = re.compile(reMC)
	line = reMC.sub(' WANT ',line,count=0)
		
	reMC = r"(?<=\W)(THK|TINK)(?=\W)"
	reMC = re.compile(reMC)
	line = reMC.sub(' THINK ',line,count=0)
		
	reMC = r"(?<=\W)(THKZ|THKS|THX|THANX)(?=\W)"
	reMC = re.compile(reMC)
	line = reMC.sub(' THANKS ',line,count=0)
	
	reMC = r"(?<=\W)(PPL(E)?|PP)(?=\W)"
	reMC = re.compile(reMC)
	line = reMC.sub(' PEOPLE ',line,count=0)
	
	
	reMC = r"(?<=\W)(JUZ|JUS)(?=\W)"
	reMC = re.compile(reMC)
	line = reMC.sub(' JUST ',line,count=0)
		
	reMC = r"(?<=\W)(OREDI|LIAO)(?=\W)"
	reMC = re.compile(reMC)
	line = reMC.sub(' ALREADY ',line,count=0)

	reMC = r"(?<=\W)(BOUT|ABT)(?=\W)"
	reMC = re.compile(reMC)
	line = reMC.sub(' ABOUT ',line,count=0)
	
	
	reMC = r"(?<=\W)S(?=\W)"
	reMC = re.compile(reMC)
	line = reMC.sub(' IS ',line,count=0)
		
	reMC = r"(?<=\W)B(?=\W)"
	reMC = re.compile(reMC)
	line = reMC.sub(' BE ',line,count=0)
		
	reMC = r"(?<=\W)TMR(?=\W)"
	reMC = re.compile(reMC)
	line = reMC.sub(' TOMORROW ',line,count=0)
		
		#TODO regarde s'il faut changer K (et OKAY) en OK
		
	reNum = r"(?<=[^1-9])2(?=[^1-9])"
	reNum = re.compile(reNum)
	line  = reNum.sub('2',line,count=0)
		
	reNum = r"(?<=[^1-9])4(?=[^1-9])"
	reNum = re.compile(reNum)
	line  = reNum.sub('4',line,count=0)
		
	line = line.replace('HAV ', 'HAVE ')
	line = line.replace('&APOS;',' <apos> ')
		
	# match les sries de points (>1 point)
	reDots = '\.\.+'
	reDots = re.compile(reDots)
	line = reDots.sub(' <dots> ',line,count=0)
		
	reDot = r"\.|!|\?"
	reDot = re.compile(reDot)
	line = reDot.sub(' <dot> ',line,count=0)
		
	reNum = r"\d+"
	reNum = re.compile(reNum)
	line  = reNum.sub(' <number> ',line,count=0)

	reSmiley = '(([;:][-o]?)|=)[\(\)pP]'
	reSmiley = re.compile(reSmiley)
	line = reSmiley.sub(' <smiley> ',line,count=0)
		
	return line

def tokensFilter(tokenlines):
	
	lexicons = sms2.ngramCount(tokenlines, 1)
	filteredLines = []
	
	for line in tokenlines:
		tokenline = []
		for token in line:
			if lexicons[(token,)]<3:
				tokenline.append('<unk>')
			else : tokenline.append(token)
		filteredLines.append(tokenline)
	
	return filteredLines

def main():
	
	trainfile = open("../smstrain.txt")
	lexicon = sms2.ngramCount(smartTokenizer(trainfile),4)
	
	lexicon_list = []
	for lex in lexicon.keys():
		lexicon_list.append( (lexicon[lex],lex) )

	lexicon_list.sort(reverse=True)
	print lexicon_list
	print len(lexicon_list)
	
	histo = sms2.histogram(lexicon)
	
	print histo
	
	writer = csv.writer(open("quadricounts.csv", "wb"))
	writer.writerows(lexicon_list)

	
if __name__ == '__main__':
	main()  