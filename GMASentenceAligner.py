'''
Created on Apr 18, 2010

@author: johnnabil
'''

from BaseToolTest import BaseToolTest
from CorpusReader import Alignment
import unittest
import os

TOOL_PATH = '/Users/macbook/Documents/workspace/pyTester/tools/GMA/gma-2.1/'

class GMASentenceAligner(BaseToolTest):
    
    def initialize(self):
        self.TOOL_NAME = 'GMA'
    
    def convertTextToAxis(self, textFile):	
		print "Opening: %s"% textFile
		sourceFile = open(textFile)
		target = '%s.axis'% (textFile)
		print "Writing: %s"% textFile
		targetFile  = open(target, 'w')
		lines = sourceFile.readlines()
		index = 0.0
		for line in lines:
			targetFile.write("%0.2f <EOS>\n"% index)
			words = line.split()
			for word in words:
				length = len(word) + 1.0
				targetFile.write("%0.2f %s\n"%(index+length/2, word))
				index = index + length
			targetFile.write("%0.2f <EOS>\n"% index)
		print "Done: %s"% target
		
    def convertToSuitableFormat(self, filePath):
        #convert the input text files into axis files
        print "Convert text to axis:", filePath
        self.convertTextToAxis(filePath)
        #cmd = "cd %s;python bin/textToAxis.py %s"%(TOOL_PATH, filePath)
        #print cmd
        #os.popen(cmd)
        #baseName = os.path.basename(filePath)
        #targetFile = "%s/testDir/%s.axis"%(TOOL_PATH, baseName)
        #targetFile = "%s/testDir/%s.axis"%(TOOL_PATH, baseName)
        targetFile = "%s.axis"%(filePath)
        print
        return targetFile
    
    
    def runWithData(self, arabic_in, english_in):
    
    	print "Begin Running ==> Source: %s, Target: %s"%(arabic_in, english_in)
    	print 
    	
    	cmd = "cd %(TOOLPATH)s"% {"TOOLPATH":TOOL_PATH}
    	print cmd
        self.runCmd(cmd, 2000)
    	
    	cmd = "export CLASSPATH=lib/gma.jar"
    	print cmd
        self.runCmd(cmd, 2000)
    	
    	cmd = "export GMApath=%(TOOLPATH)s"% {"TOOLPATH":TOOL_PATH}
    	print cmd
        self.runCmd(cmd, 2000)
    	
    	cmd = "alias java='java -DGMApath=$GMApath'"
    	print cmd
        self.runCmd(cmd, 2000)
    	
    	if self.sourceLanguageConfig == "AR":
    		cmd = """
java -Xms128m -Xmx512m gma.GMA  -properties %(TOOLPATH)s/config/GMA.config.A.E 
-xAxisFile %(SOURCEFILE)s \
-yAxisFile %(TARGETFILE)s \
-simr.outputFile %(TOOLPATH)s/bin/output/output.simr \
-gsa.outputFile %(TOOLPATH)s/bin/output/output.align
    	"""% {"TOOLPATH":TOOL_PATH, "SOURCEFILE":arabic_in,"TARGETFILE":english_in }
    	
    	elif self.sourceLanguageConfig == "FR":
    		cmd = """
java -Xms128m -Xmx512m gma.GMA  -properties %(TOOLPATH)s/config/GMA.config.F.E 
-xAxisFile %(SOURCEFILE)s \
-yAxisFile %(TARGETFILE)s \
-simr.outputFile %(TOOLPATH)s/bin/output/output.simr \
-gsa.outputFile %(TOOLPATH)s/bin/output/output.align
    	"""% {"TOOLPATH":TOOL_PATH, "SOURCEFILE":arabic_in,"TARGETFILE":english_in }
    	
    	
    	print cmd
        self.runCmd(cmd, 2000)
        
        print "Finished Running"
        print
        
        

        
        
    def loadActualData(self, arabic_in, english_in):
        #open the arabic + english files
        print "Begin loadActualData ==> Source: %s, Target: %s"%(arabic_in, english_in)
    	print 
        
        arabicFile = open(arabic_in)
        englishFile = open(english_in)
        
        
        arabicSegments = arabicFile.readlines()#[]
        englishSegments = englishFile.readlines()#[]
        
            
        #load the alignment result
        resultGSA = open("%sbin/output/output.align"% TOOL_PATH)
        resultGSALines = resultGSA.readlines()
        
        for entry in resultGSALines:
            a = entry.split(' <=> ')
            if 'omitted' in a:
                continue
            arabicList = eval(a[0])
            englishList = eval(a[1])
            
            arabicSentence = ''
            englishSentence = ''
            
            if ',' in a[0]:
                for s in arabicList:                    
                    arabicSentence = arabicSentence + ' ' + arabicSegments[s-1]
            else:
                arabicSentence = arabicSegments[arabicList-1]
                
            if ',' in a[1]:
                for s in englishList:                    
                    englishSentence = englishSentence + ' ' + englishSegments[s-1]
            else:
                englishSentence = englishSegments[englishList-1]
            
            alignment = Alignment(arabicSentence, englishSentence)
            self.actualAlignments.append(alignment)
        print "Finished loadActualData"
        print ""
	    
            


        
        
if __name__=='__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(GMASentenceAligner)
    unittest.TextTestRunner(verbosity=2).run(suite)

        
    