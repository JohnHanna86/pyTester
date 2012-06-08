'''
Created on Apr 18, 2010

@author: johnnabil
'''

from BaseToolTest import BaseToolTest

from CorpusReader import Alignment
import unittest
import os

TOOL_PATH = '/Users/macbook/Documents/workspace/pyTester/tools/bilingual-sentence-aligner'

class BilingualSentenceAligner(BaseToolTest):
    
    def initialize(self):
        self.TOOL_NAME = 'Bilingual Sentence Aligner'
    
    def runWithData(self, arabic_in, english_in):
        # perl align-sents-all.pl ../data/arabic.small.1.txt ../data/english.small.1.txt 0.5
        cmd = 'cd %s; perl %s/align-sents-all.pl %s %s 0.5'%(TOOL_PATH, TOOL_PATH, arabic_in, english_in)
        print cmd
        os.popen(cmd)
        
    def loadActualData(self, arabic_in, english_in):
        arabicResult = '%s.aligned'%arabic_in
        englishResult = '%s.aligned'%english_in
        
        self.actualAlignments = []
        
        arabicFile = open(arabicResult)
        englishFile = open(englishResult)
        
        arabicList = arabicFile.read().split('\n')
        englishList = englishFile.read().split('\n')
        
        if len(arabicList) != len(englishList):
            raise RuntimeError('Could not load actual data because len(arabicList) != len(englishList)')
        
        for i in range(len(arabicList)):
            sourceSentence = arabicList[i]
            targetSentence = englishList[i]
            
            alignment = Alignment(sourceSentence, targetSentence)
            self.actualAlignments.append(alignment)
        
        
if __name__=='__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(BilingualSentenceAligner)
    unittest.TextTestRunner(verbosity=2).run(suite)

        
    