'''
Created on 26 fevr. 2010

@author: Adrien
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
        
        self.histoCount = self.__ngramCount(training,order-1)
        self.ngCount = self.__ngramCount(training, order)
        self.lexicon = self.__ngramCount(training, 1)
        self.n = len(self.lexicon)
        
        print(len(self.lexicon))
    
    def shannon_game(self,histo):
        propositions = []
        for word in self.lexicon.keys() :   
            propositions.append((self.probNG(word[0],histo),word[0]))
      
        propositions.sort(reverse=True)
        return propositions
        
    def probNG(self,word,histo):
        sentence = histo + (word,)
        cSentence = 0
        cHisto = 0
        
        if histo    in self.histoCount.keys() : 
            cHisto = self.histoCount[histo]
            if sentence in self.ngCount.keys() : 
                cSentence = self.ngCount[sentence]
        
        
        return (cSentence+1)/(1.0 * cHisto + self.n) 
    
    def __ngramCount(self,tokenlines,order) :
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
            prob = self.probNG(word,histo)
            #print "p:"+str(prob)
            if prob>0 : 
                logprob += math.log(prob,2) 
            i+=1
            
        
        return logprob
            
    def perplexity(self,testset):
        
        prob = self.probText(testset)
        
        return 2**(prob/self.n)
         
        