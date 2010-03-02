'''
Created on 26 fevr. 2010

@author: Adrien Dessy
'''

import math

class Model:
	'''
	Smoothed model of Laplace. Enables general estimations of probabilities (li
	nes, texts, ngram) and can perform a shannon game to determine the next wor
	d given some history.
	'''
	
	def __init__(self,training,order):
		'''
		Model building from a list of lines, each line corresponding to a list 
		tokens and for some order (i.e. size of the considered ngrams).
		'''
		self.order = order
		self.training = training
		
		self.histoCount = {}
		if order > 1:
			self.histoCount = self.__ngramCount(training,order-1) # histo lexicon
		self.ngCount = self.__ngramCount(training, order)	 # ngram lexicon
		self.lexicon = self.__ngramCount(training, 1)		  # token lexicon  
		self.n = len(self.lexicon)					   # token lexicin size
		self.trainLength = self.__length(training)
		
	def shannon_game(self,histo):
		'''Try to determine the word that most likely appear after the histo histo 
		ry. Return an ordered list of pairs (probability, predicted word) sorted
		according to the probability in decreasing order.
		'''

		propositions = []

		for word in self.lexicon.keys() :   
			propositions.append((self.probNG(word[0],histo),word[0]))

		propositions.sort(reverse=True)
		return propositions
		
		
	def probNG(self,word,histo):
		''' 
		Compute the conditional probability according to a laplacian model of s
		ome word word given a history histo
		'''
		sentence = histo + (word,)
		# Respective counts
		cSentence = 0
		cHisto = (self.order ==1)*self.trainLength
		
		
		if histo	in self.histoCount.keys() : 
			cHisto = self.histoCount[histo]
		if sentence in self.ngCount.keys() : 
			cSentence = self.ngCount[sentence]
			
		print str(sentence) + " " + str(cSentence)
		print str(histo) + " " + str(cHisto)
		print "prob : " + str((cSentence+1)/(1.0 * cHisto + self.n) ) 
		
		print self.n
		
		return (cSentence+1)/(1.0 * cHisto + self.n) 
	
	
	def __ngramCount(self,tokenlines,order) :
		''' Enables to compute the different lexicons according to the order '''
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
	
	def probText(self,testlines):
		''' 
		Compute the log probability of a text (given as a list of lists of toke
		ns) according to the laplacian model
		'''
		length = 0
		logprob = 0
		for line in testlines :
			probinc, lengthinc = self.probLine(line) 
			logprob += probinc
			length  += lengthinc
		
		return logprob, length 	
			
	def probLine(self,line):
		'''
		Compute the log probability of line (a list of tokens=strings) according
		to the laplacian model
		'''
		
		line =  ['<text_start>']*(self.order-1) + line[1:]
		logprob = 0
		i = 0
		for word in line[self.order-1:]:
			histo = tuple(line[i:(i+self.order-1)])
			prob = self.probNG(word,histo)
			logprob += math.log(prob,2) 
			i+=1
		
		return logprob,i
			
	def perplexity(self,testset):
		'''
		Compute the perplexity of a text according to the laplacian model.
		'''
		
		prob,N = self.probText(testset)
		return 2**(-prob/N)
		
	def __length(self,tokenlines):
		size = 0
		for lines in tokenlines : 
			size += len(lines)
		
		return size
		
		