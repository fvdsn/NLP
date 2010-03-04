'''
Created on 26 fevr. 2010

@author: fred
'''

import math
import random

class Model:
	'''
	classdocs
	'''

	def __init__(self,training,order):
		'''
		Constructor
		'''
		self.order = order
		self.training = training
		self.lexicon_set = {}

		self.probNG_KN_cache = {}			#memoization of probNG_KN(...) 
		self.probNG_KN_gamma_cache = {}			#memoization of probNG_KN(...) 
		self.probNG_KN_dc_cache = {}			#memoization of probNG_KN(...) 
		
		print "\tComputing lexicons..."
		for n in range(order):
			print "\t\tOrder :",n+1,"..."
			self.lexicon_set[n+1] = self.__ngramCount(training,n+1)
		print "\tDone"

		self.histoCount = {}
		if order > 1:
			self.lexicon_set[order-1]	
		self.ngCount = self.lexicon_set[order]		
		self.lexicon = self.lexicon_set[1]			
		self.n = len(self.lexicon)
		self.ntot = sum(self.lexicon.values())

	def shannon_game(self,histo):
		propositions = []
		for word in self.lexicon.keys() : 
			if word != ():    
				propositions.append((self.probNG_KN(word[0],histo),word[0]))
	  
		propositions.sort(reverse=True)
		return propositions
	
	def check_proba(self,order,percentage):
		rounds = int(len(self.lexicon_set[order-1].keys())*percentage)
		mean_prob = 0.0;
		for r in range(rounds):
			histo = random.choice(self.lexicon_set[order-1].keys())
			#print histo
			proba = 0.0
			for word in self.lexicon.keys():
				if word != () :
					proba += self.probNG_KN(word[0],histo)
			print proba
			mean_prob += proba * 1.0/float(rounds)
		return mean_prob

	def probNG_KN(self,word,histo):

		def dc(order):
			n1 = 0
			n2 = 0
			if order in self.probNG_KN_dc_cache:
				return self.probNG_KN_dc_cache[order]

			for n in self.lexicon_set[order].values():
				if n == 1:
					n1 += 1
				elif n == 2:
					n2 += 2
			dc = n1 / float(n1 + 2*n2)
			print "DC(",order,"):",dc
			self.probNG_KN_dc_cache[order] = dc
			return dc

		def pback(self,word,histo):
			hist_1 = histo[1:len(histo)]
			if hist_1 == ():
				if (word,) in self.lexicon_set[1]:
					return self.lexicon_set[1][(word,)] / float(self.ntot)
				else:
					#return 0.0
					return self.lexicon_set[1][('<unk>',)] / float(self.ntot)
			else:
				return self.probNG_KN(word,hist_1)

		def gamma(self,histo):
			if histo in self.probNG_KN_gamma_cache:
				return self.probNG_KN_gamma_cache[histo]
			g = 0.0
			for w in self.lexicon_set[1].keys():
				hw = histo + w
				#print hw
				if hw in self.lexicon_set[len(hw)]:
					g = g + dc(len(hw))/float(self.lexicon_set[len(histo)][histo])
			self.probNG_KN_gamma_cache[histo] = g
			return g

		prob = 0
		hw    = histo + (word,)
		order = len(hw)

		if hw in self.probNG_KN_cache:
			return self.probNG_KN_cache[hw]

		if hw in self.lexicon_set[order]: #self.lexicon_set[order][hw] > 0:
			prob = ((self.lexicon_set[order][hw] - dc(order))/float(self.lexicon_set[len(histo)][histo])) +	gamma(self,histo) * pback(self,word,histo)
		elif histo in self.lexicon_set[len(histo)]:
			prob = gamma(self,histo)  * pback(self,word,histo)
		else:
			prob = pback(self,word,histo)

		self.probNG_KN_cache[hw] = prob
		
		return prob

	def probNG_Basic(self,word,histo):
		hw = histo + (word,)
		ch = 0.0
		chw = 0.0
		if hw in self.lexicon_set[len(hw)]:
			chw = float(self.lexicon_set[len(hw)][hw])
		if histo == ():
			return chw / self.ntot
		elif histo in self.lexicon_set[len(histo)]:
			ch = float(self.lexicon_set[len(histo)][histo])
		return (chw+1)/(ch + len(self.lexicon_set[1]))
	
	def probNG_Linear(self,word,histo):
		hw = histo + (word,)
		order = len(hw)
		lambdas = self.getLambdas(order)
		prob = 0.0
		for i in range(order):
			prob += self.probNG_Basic(word,histo[-i:])*lambdas[i]
		return prob

	def makeLambdas(self,order,sample):
		print "yo"

	def getLambdas(self,order):
		v = [1.0/order]
		return v * order

	def __ngramCount(self,tokenlines,order) :
		start = ('<text_start>',)
		count = {}
		for line in tokenlines:
		
			if order > 1 : 
				for i in range(1,order):
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
			prob = self.probNG_KN(word,histo)
			logprob += math.log(prob,2) 
			i+=1
		
		return logprob,i

	def perplexity(self,testset):
		'''
		Compute the perplexity of a text according to the laplacian model.
		'''
		
		prob,N = self.probText(testset)
		return 2**(-prob/N)
