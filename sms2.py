# TODO change the modification with WILL
# insert an unknown word in the voc
# check if k could be replaced by OK 
# remove the start and end tags for the histogram computation
# new smiley ^_^

#!/usr/bin/python
import sys
import re
import mlaplace
import mkn
import token

def count(lexicons,ngram):
	"""renvoie le nombre de fois que le ngram apparait dans le texte
	   lexicons est un dico associant le degre n au lexicon des ngrammes de degre n"""
	n = len(ngram)
	if n in lexicons.keys():
		if ngram in lexicons[n]:
			return float(lexicons[n][ngram])
	return 0.0

def maximium_likelihood(lexicons, ngram, prefix):
	"""renvoie la probabilite P(w|h) avec ngram = h,w et prefix = h, lexicons: voir count"""
	if count(prefix) > 0:
		return count(lexicons,ngram)/count(lexicons,prefix)
	else:
		return 0.0

def laplacef(lexicons,ngram,prefix):
	"""renvoie la probabilite P(w|h), avec laplace smoothing avec ngram = h,w et prefix = h, lexicons: voir count"""
	wlen = len(ngram)-len(prefix)			# vaut normalement 1
	w = ngram[len(ngram)-wlen:len(ngram)]	# prendre les wlen dernier tokens de ngram
	Wcount = 0								# |W|
	if wlen in lexicons.keys():
		Wcount = len(lexicons[wlen].keys())
	
	return ( count(lexicons,ngram) + 1.0 ) / ( count(lexicons,prefix) + Wcount )

		

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
					
				
		for i in range(len(line)-order+1):
			key = tuple(line[i:i+order])
			if key in count:
				count[key] += 1
			else :
				count[key] = 1
	
	return count
							
def histogram(ngramCount):
	""" Retourne une liste de paires (nb x, nb de ngram apparaissant x fois)."""
	hist = {}
	for x in ngramCount.values():
		if x in hist:
			hist[x] += 1
		else:
			hist[x] = 1
	pairs = hist.items()
	pairs.sort(reverse=True)
	return pairs

def maxLikely(ngramCount,histoCount,word,histo):
	
	sentence = histo + (word,)
	if sentence in ngramCount.keys():
		return ngramCount[sentence]/(1.0 * histoCount[histo])
	return 0.0

def laplace(ngramCount,histoCount,word,histo,n):
	sentence = histo + (word,)
	if sentence in ngramCount.keys():
		return (ngramCount[sentence]+1)/(1.0 * histoCount[histo] + n)
	return 0.0

def main():
	if len(sys.argv) < 2:
		exit()
	
	argsNb = len(sys.argv)
	trainfile = open(sys.argv[argsNb-1])
	#testfile = open("../smstest.txt")
	
	traintokenlines = token.smartTokenizer(trainfile)
	#print traintokenlines
	
	#mod = mlaplace.Model(traintokenlines,3)
	mod = mkn.Model(traintokenlines,3)
	
	#print mod.perplexity(token.smartTokenizer(testfile))
	print mod.shannon_game(("BOTH","OF"))
	
	#print mod.probText(tokenizer(testfile))
	#str = ["<text_start>","OKKO","<dotsi>","YESLO","<dot>","<text_end>"]
	
	
	
if __name__ == '__main__':
	main()
