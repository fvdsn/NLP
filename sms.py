#!/usr/bin/python
import sys
import re

def main():
	if len(sys.argv) < 2:
		exit()
	smsfile = open(sys.argv[len(sys.argv)-1])
	smslines = smsfile.readlines()
	lexicon = {}
	tokenlines = []
	twogramcon = {}
	threegramcon = {}

	for line in smslines:
		line = line.upper()
		
		line = line.replace(',',' <comma> ')
		
		# les balises ne doivent contenir que du texte pour findall
		line = line.replace('</TEXT>',' <text_end> ')
		line = line.replace('<TEXT>',' <text_start> ')
		
		line = line.replace('&APOS;',' <apos> ')
		
		# mots courant
		reMC = r"(?<=\W)E(?=\W)"
		reMC = re.compile(reMC)
		line = reMC.sub(' THE ',line,count=0)
		
		reMC = r"(?<=\W)(U|YA)(?=\W)"
		reMC = re.compile(reMC)
		line = reMC.sub(' YOU ',line,count=0)
		
		reMC = r"(?<=\W)R(?=\W)"
		reMC = re.compile(reMC)
		line = reMC.sub(' ARE ',line,count=0)
		
		reMC = r"(?<=\W)N(?=\W)"
		reMC = re.compile(reMC)
		line = reMC.sub(' AND ',line,count=0)
		
		reMC = r"(?<=\W)C(?=\W)"
		reMC = re.compile(reMC)
		line = reMC.sub(' SEE ',line,count=0)
		
		reMC = r"(?<=\W)(UR|YR)(?=\W)"
		reMC = re.compile(reMC)
		line = reMC.sub(' YOUR ',line,count=0)
		
		reMC = r"(?<=\W)(I\WAM|IAM|IM)(?=\W)"
		reMC = re.compile(reMC)
		line = reMC.sub(' I &APOS; M ',line,count=0)
		
		reMC = r"(?<=\W)WILL(?=\W)"
		reMC = re.compile(reMC)
		line = reMC.sub(' &APOS;LL ',line,count=0)
		
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
		
		reMC = r"(?<=\W)(WAN|WANNA)(?=\W)"
		reMC = re.compile(reMC)
		line = reMC.sub(' WANT ',line,count=0)
		
		
		reMC = r"(?<=\W)(JUZ|JUS)(?=\W)"
		reMC = re.compile(reMC)
		line = reMC.sub(' JUST ',line,count=0)
		
		reMC = r"(?<=\W)(OREDI|LIAO)(?=\W)"
		reMC = re.compile(reMC)
		line = reMC.sub(' ALREADY ',line,count=0)

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
		
		
		
		
		#print line
		#line = line.replace('<TEXT>','')
		#line = line.replace('</TEXT>','')
		#tokens = re.split(r"\W+|[.,!?;]",line)
		
		reSplit = r"(<?\w+>?)"
		reSplit = re.compile(reSplit)
		tokens = reSplit.findall(line)
		tokenline = []
		#print tokens
		for token in tokens:
			if token == '':
				continue
			tokenline.append(token)
			if token in lexicon:
				lexicon[token] += 1
			else:
				lexicon[token] = 1
		tokenlines.append(tokenline)

	#sorting lexicon
	lexicon_list = []
	for lex in lexicon.keys():
		lexicon_list.append( (lex, lexicon[lex]) )
	
	def comp(a,b):
		return  b[1] - a[1] 
	
	lexicon_list.sort(comp)
	
	print lexicon_list

	
	# Compute a dictionary of N-grams
	def ngramCount(tokenlines,order) :
		start = ('<text_start>',)
		count = {}
		for line in tokenlines:
			
			if order > 2 : 
				for i in range(2,order):
					key = start*(order-i) + tuple(line[0:i])
					if key in count:
						count[key] += 1
					else :
						count[key]=1
						
				
			for i in range(len(line)-order+2):
				key = tuple(line[i:i+order])
				if key in count:
					count[key] += 1
				else :
					count[key] = 1
		
		return count
							
#	#ngramcon
#	for line in tokenlines:
#		for i in range(len(line)-2):
#			key = tuple(line[i:i+3])
#			if key in threegramcon:
#				threegramcon[key] +=1
#			else:
#				threegramcon[key] = 1
#		for i in range(len(line)-1):
#			key = tuple(line[i:i+2])
#			if key in twogramcon:
#				twogramcon[key] +=1
#			else:
#				twogramcon[key] = 1
#	
#	threegramcon_list = []
#	for lex in threegramcon.keys():
#		threegramcon_list.append( (lex, threegramcon[lex]) )
#	threegramcon_list.sort(comp)
#
#	twogramcon_list = []
#	for lex in twogramcon.keys():
#		twogramcon_list.append( (lex, twogramcon[lex]) )
#	twogramcon_list.sort(comp)
#
#	#print threegramcon_list
#	threefreq = [ x[1] for x in threegramcon_list]
#	twofreq = [ x[1] for x in twogramcon_list]
#	unifreq = [ x[1] for x in lexicon_list]
#
#	def histogram(list):
#		hist = {}
#		for x in list:
#			if x in hist:
#				hist[x] += 1
#			else:
#				hist[x] = 1
#		list = hist.values()
#		list.sort()
#		list.reverse()
#		return list

	#print threefreq
	#print 'yo'

	
	#for x in histogram(unifreq):
	#	print x

	
	#print lexicon_list 
	#print tokenlines
if __name__ == '__main__':
	main()
