'''
Created on Apr 18, 2010

@author: johnnabil
'''

from BaseToolTest import BaseToolTest
from CorpusReader import Alignment
import unittest
import os

TOOL_PATH = '/Users/macbook/Documents/workspace/pyTester/tools/Vanilla/src'

class VanillaSentenceAligner(BaseToolTest):
    
    def initialize(self):
        self.TOOL_NAME = 'Vanilla'
    
    def readLinesEnabled(self):
    	return True
    	
    def convertToSuitableFormat(self, filePath): 
    
		#print "sourceLines: %d"% len(self.sourceLines)
		#print "targetLines: %d"% len(self.targetLines)

		maxNumberOfHardRegions = max(len(self.targetLines),  len(self.sourceLines))
		ps = self._getLines(filePath)
		result = list()
		#print "Hardregions[%s]: ==> %s"%(filePath, len(ps))
		
		for p in ps:
			result.extend(p.split())
			result.append('.EOS')
			result.append('.EOP')
			#print "Appending .EOS and .EOP to: ", p
			
		for added in range(len(ps), maxNumberOfHardRegions):
			result.append('.EOP')
	   
		targetFile = "%s.tok"%filePath  
		f = open(targetFile, 'w')
		f.write('\n'.join(result))
		f.close()
		return targetFile
    
    
    def runWithData(self, arabic_in, english_in): 
    	print "source: %s"%arabic_in
        cmd = "cd %s; ./align0 -D '.EOP' -d '.EOS' %s %s "%(TOOL_PATH, arabic_in, english_in)
        os.popen(cmd)
        
    def loadActualData(self, arabic_in, english_in):
        
        resultFile = "%s.tok.al"%arabic_in
        
        f = open(resultFile)
        
        content = f.read()
        
        alignments = map(lambda y: y.replace('.EOS', ''), filter( lambda x: x and x != '.EOP' and not x.startswith('*** Link'), content.split('\n')))
        
        for i in range(0, len(alignments), 2):
            sourceSentence = alignments[i]
            targetSentence = alignments[i+1]
            
            alignment = Alignment(sourceSentence, targetSentence)
            self.actualAlignments.append(alignment)
        
        
        
if __name__=='__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(VanillaSentenceAligner)
    unittest.TextTestRunner(verbosity=2).run(suite)

        
    