'''
Created on May 5, 2010

@author: johnnabil
'''


from BaseToolTest import BaseToolTest
from CorpusReader import Alignment
import unittest
import os

TOOL_PATH = '/Users/macbook/Documents/workspace/pyTester/tools/CTK'

class CTKSentenceAligner(BaseToolTest):
    
    def initialize(self):
        self.TOOL_NAME = 'CTK (Champollion)'
    
    def convertToSuitableFormat(self, filePath):
        return filePath
    
    
    def runWithData(self, arabic_in, english_in):        
    
        if self.sourceLanguageConfig == "AR":
            cmd = "cd %(home)s; export CTK=%(home)s;./test_installation; ./bin/champollion.EA %(english)s %(arabic)s %(arabic)s.ctk.temp.txt; perl ./scripts/ctk_align.pl %(arabic)s.ctk.temp.txt %(english)s %(arabic)s %(arabic)s.ctk.align.txt"%{'home':TOOL_PATH, 'english':english_in, 'arabic':arabic_in}
        elif self.sourceLanguageConfig == "FR":
            cmd = "cd %(home)s; export CTK=%(home)s;./test_installation; ./bin/champollion.EA %(english)s %(arabic)s %(arabic)s.ctk.temp.txt; perl ./scripts/ctk_align.pl %(arabic)s.ctk.temp.txt %(english)s %(arabic)s %(arabic)s.ctk.align.txt"%{'home':TOOL_PATH, 'english':english_in, 'arabic':arabic_in}
        
        print cmd
        os.popen(cmd)    
        #self.runCmd(cmd, 3600)    
        print "Finished !!"
        
    def loadActualData(self, arabic_in, english_in):
        
        resultFile = "%s.ctk.align.txt"%arabic_in
        
        f = open(resultFile)
        
        sentences = f.readlines()
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            if not len(sentence.split('\t')) == 2:
                continue
           
            elements = sentence.split('\t')    
            sourceSentence = elements[0]
            targetSentence = elements[1]            
            
            alignment = Alignment(targetSentence, sourceSentence)
            self.actualAlignments.append(alignment)
        
        
        
if __name__=='__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(CTKSentenceAligner)
    unittest.TextTestRunner(verbosity=2).run(suite)