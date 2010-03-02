'''
Created on 26 fevr. 2010

@author: fred
'''

import math

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
		self.histoCount = self.__ngramCount(training,order-1)	#ngram -1
		self.ngCount = self.__ngramCount(training, order)		#ngram
		self.lexicon = self.__ngramCount(training, 1)			#lexicon
		self.n = len(self.lexicon)
		self.ntot = sum(self.lexicon.values())
		self.lexicon_set = {}
		self.probNG_KN_cache = {}			#memoization of probNG_KN(...) 
		self.probNG_KN_gamma_cache = {}			#memoization of probNG_KN(...) 
		self.probNG_KN_dc_cache = {}			#memoization of probNG_KN(...) 
		
		for n in range(order):
			if(n+1 == order-1):
				self.lexicon_set[n+1] = self.histoCount
			elif(n+1 == order):
				self.lexicon_set[n+1] = self.ngCount
			elif(n+1 == 1):
				self.lexicon_set[1] = self.lexicon
			else:
				self.lexicon_set[n+1] = self.__ngramCount(training,n+1)

		print "computing lexicons... done"

	def shannon_game(self,histo):
		propositions = []
		for word in self.lexicon.keys() : 
			if word != ():    
				propositions.append((self.probNG_KN(word[0],histo),word[0]))
	  
		propositions.sort(reverse=True)
		return propositions
		

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
				return self.lexicon_set[1][(word,)] / float(self.ntot)
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
			prob = ((self.lexicon_set[order][hw] - dc(order))/float(self.lexicon_set[order-1][histo])) +	gamma(self,histo) * pback(self,word,histo)
		elif histo in self.lexicon_set[len(histo)]:
			prob = gamma(self,histo)  * pback(self,word,histo)
		else:
			prob = pback(self,word,histo)

		self.probNG_KN_cache[hw] = prob
		
		return prob

	def __ngramCount(self,tokenlines,order) :
		print order
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

	def probText(self,testlines): 
		logprob = 0
		for line in testlines : 
			logprob += self.probLine(line)
		
		return logprob 
			
			
	def probLine(self,line):
		line =  ['<text_start>']*(self.order-2) + line
		logprob = 0
		i = 0
		for word in line[self.order-1:]:
			histo = tuple(line[i:(i+self.order-1)])
			#print "word "  + str(word)
			#print "histo " + str(histo)
			prob = self.probNG_KN(word,histo)
			#print "p:"+str(prob)
			if prob>0 : 
				logprob += math.log(prob,2) 
			i+=1
			
		
		return logprob
			
	def perplexity(self,testset):
		
		prob = self.probText(testset)
		
		return 2**(prob/self.n)
     
   

