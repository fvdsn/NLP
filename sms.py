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
		line = line.replace('2',' TO ')
		line = line.replace('4',' FOR ')
		line = line.replace(':)','  SMILEY ')
		line = line.replace(':(','  SMILEY ')
		line = line.replace(':P','  SMILEY ')
		line = line.replace(':-)',' SMILEY ')
		line = line.replace(':-(',' SMILEY ')
		line = line.replace(';o)',' SMILEY ')
		line = line.replace('=)','  SMILEY ')
		line = line.replace('=(','  SMILEY ')
		line = line.replace('.......',' DOTS ')
		line = line.replace('......',' DOTS ')
		line = line.replace('.....',' DOTS ')
		line = line.replace('....',' DOTS ')
		line = line.replace('...',' DOTS ')
		line = line.replace('..',' DOTS ')
		line = line.replace('.',' DOT ')
		line = line.replace('?',' INTERROGATIONDOT ')
		line = line.replace('!',' EXCLAMATIONDOT ')
		line = line.replace('<TEXT>','')
		line = line.replace('</TEXT>','')
		#tokens = re.split(r"\W+|[.,!?;]",line)
		tokens = re.split('\W+',line)
		tokenline = ['S_BEGIN']
		for token in tokens:
			if token.isdigit():
				token = 'NUMBER'
			if token == '':
				continue
			tokenline.append(token)
			if token in lexicon:
				lexicon[token] += 1
			else:
				lexicon[token] = 1
		tokenline.append('S_END')
		tokenlines.append(tokenline)

	#sorting lexicon
	lexicon_list = []
	for lex in lexicon.keys():
		lexicon_list.append( (lex, lexicon[lex]) )
	
	def comp(a,b):
		return  b[1] - a[1] 
	
	lexicon_list.sort(comp)
	
	#ngramcon
	for line in tokenlines:
		for i in range(len(line)-2):
			key = tuple(line[i:i+3])
			if key in threegramcon:
				threegramcon[key] +=1
			else:
				threegramcon[key] = 1
		for i in range(len(line)-1):
			key = tuple(line[i:i+2])
			if key in twogramcon:
				twogramcon[key] +=1
			else:
				twogramcon[key] = 1
	
	threegramcon_list = []
	for lex in threegramcon.keys():
		threegramcon_list.append( (lex, threegramcon[lex]) )
	threegramcon_list.sort(comp)

	twogramcon_list = []
	for lex in twogramcon.keys():
		twogramcon_list.append( (lex, twogramcon[lex]) )
	twogramcon_list.sort(comp)

	#print threegramcon_list
	threefreq = [ x[1] for x in threegramcon_list]
	twofreq = [ x[1] for x in twogramcon_list]

	def histogram(list):
		hist = {}
		for x in list:
			if x in hist:
				hist[x] += 1
			else:
				hist[x] = 1
		list = hist.values()
		list.sort()
		list.reverse()
		return list

	#print threefreq
	#print 'yo'

	
	for x in histogram(threefreq):
		print x


	


	
	#print lexicon_list 
	#print tokenlines
if __name__ == '__main__':
	main()
