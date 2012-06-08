'''
Created on May 5, 2010

@author: johnnabil
'''

from BaseToolTest import BaseToolTest
from CorpusReader import Alignment
import unittest
import os

TOOL_PATH = '/Users/macbook/Documents/workspace/pyTester/tools/hunalign/src'

class HunalignSentenceAligner(BaseToolTest):
    
    def initialize(self):
        self.TOOL_NAME = 'Hunalign'
    
    def convertToSuitableFormat(self, filePath):        
        return filePath
    
    def runWithData(self, arabic_in, english_in):        
        cmd = "cd %s; ./hunalign ../data/null.dic %s %s -text > %s.alignment.txt"%(TOOL_PATH, arabic_in, english_in, arabic_in)
        self.runCmd(cmd, 1800)
        #os.popen(cmd)
        
    def loadActualData(self, arabic_in, english_in):
        resultFile = "%s.alignment.txt"%arabic_in
        f = open(resultFile)        
        content = f.read()
        
        alignments = filter(lambda x: x, content.split('\n'))       
        
        for alignment in alignments:             
            sourceSentence, targetSentence, _ = alignment.split('\t')            
            alignment = Alignment(sourceSentence, targetSentence)
            self.actualAlignments.append(alignment)
        
if __name__=='__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(HunalignSentenceAligner)
    unittest.TextTestRunner(verbosity=2).run(suite)

        
    