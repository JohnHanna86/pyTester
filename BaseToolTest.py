'''
Created on Mar 1, 2010

@author: johnnabil
'''
from test.test_optparse import TestCount


"""
let's introduce my convension in testing the alignment tools

Every alignment tool will have it's own test module
Every test will be in seperate class (TestCase)
Every test will have it's own folder for output
 
"""
import unittest
import chardet
import subprocess, signal
import os
import sys
import time
from CorpusReader import CorpusReader
from CorpusReader import Alignment
from xml.dom import minidom
import ConfigParser
import difflib
import traceback


#TOOL_PATH

CONFIG_FILE='config/cfg.ini'

    
class BaseToolTest(unittest.TestCase):
    
    def setUp(self):
    	#setting up and initializing the internal data
    	self.initialize()        
        self.readInputData()        
        self.goldenAlignments = []
        self.actualAlignments = []
        
        
    def initialize(self):
        self.TOOL_NAME = 'default'
        
    def readInputData(self):
        config = ConfigParser.ConfigParser()
        config.readfp(open(CONFIG_FILE))
        outputPath = config.get('main', 'output_path')
        inputPath = config.get('main', 'input_path')
        inputData_xml = config.get('main', 'input_data_xml')
        self.sourceLanguageConfig = config.get('main', 'sourceLanguage')
        self.targetLanguageConfig = config.get('main', 'targetLanguage')

        self.TestList = []
        p = minidom.parse(inputData_xml)
        p = p.childNodes[0]
        for testNode in filter(lambda x: x.localName=='test', p.childNodes):
            source = os.path.join(inputPath, filter(lambda x: x.localName == 'source', testNode.childNodes)[0].childNodes[0].nodeValue.strip())
            target = os.path.join(inputPath, filter(lambda x: x.localName == 'target', testNode.childNodes)[0].childNodes[0].nodeValue.strip())
            golden = os.path.join(inputPath, filter(lambda x: x.localName == 'golden', testNode.childNodes)[0].childNodes[0].nodeValue.strip())
            self.TestList.append((source, target, golden))        
        
        self.outputFile = open('%s/summary/%s_%s.csv'%(outputPath, self.TOOL_NAME ,time.asctime().replace(' ', '_')), 'a')
        self.AlignmentFilePath = '%s/alignment/%s_%s'%(outputPath, self.TOOL_NAME ,time.asctime().replace(' ', '_'))
        
        print "OUTPUT", outputPath
                                                                           
        
    
    #this function differs from tool to another tool.

    def runWithData(self, arabic_in, english_in):    
        # perl align-sents-all.pl ../data/arabic.small.1.txt ../data/english.small.1.txt 0.5
        cmd = 'cd %s; perl %s/align-sents-all.pl %s %s 0.5'%(TOOL_PATH, TOOL_PATH, arabic_in, english_in)
        os.popen(cmd)
        
    def runCmd(self, cmd, timeout=None):
        '''
        Will execute a command, read the output and return it back.
        
        @param cmd: command to execute
        @param timeout: process timeout in seconds
        @return: a tuple of three: first stdout, then stderr, then exit code
        @raise OSError: on missing command or if a timeout was reached
        '''
        
        ph_out = None # process output
        ph_err = None # stderr
        ph_ret = None # return code
        
        p = subprocess.Popen(cmd, shell=True,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        # if timeout is not set wait for process to complete
        if not timeout:
            ph_ret = p.wait()
        else:
            fin_time = time.time() + timeout
            while p.poll() == None and fin_time > time.time():
                time.sleep(1)
        
            # if timeout reached, raise an exception
            if fin_time < time.time():
        
                # starting 2.6 subprocess has a kill() method which is preferable
                # p.kill()
                try:
                    os.kill(p.pid, signal.SIGKILL)
                except:
                    print "Process didn't start yet :)"
                    
                raise OSError("Process timeout has been reached")
        
            ph_ret = p.returncode
        
        
        ph_out, ph_err = p.communicate()
        
        return (ph_out, ph_err, ph_ret)
    
    def loadGoldenReference(self, golden):  
    	print "Begin loadGoldenReference"
        reader = CorpusReader(golden, self.sourceLanguageConfig, self.targetLanguageConfig)
        self.goldenAlignments = reader.alignments  
        print "End loadGoldenReference"
        print
    
    def loadActualData(self, arabic_in, english_in):
        pass
             

    def _doesAlignmentExistInGolden(self, actualAlignment):
		#get the original soruce
		print "_doesAlignmentExistInGolden"
		(goldenSource, index)  = self._getOriginalSource(actualAlignment.target)
		trial = 0
		while goldenSource != None:
			print "Trial [%d] at index: %d"%(trial, index)
			trial = trial + 1
			#see if the targets
			result = self.compareTwoSentences(goldenSource, actualAlignment.source)
			if result:
				print "Found"
				return True
			(goldenSource, index)  = self._getOriginalSource(actualAlignment.source, index+1)
		#if goldenSource == None:
		#	print "5eles El kalam"
		print "Not Found"
		return False
		
		
    def _getOriginalSource(self, target, beginningIndex=-1):    
    	#print "_getOriginalSource"
    	i = 0
        for orignalAlignment in self.goldenAlignments:
        	if i < beginningIndex:
        		i = i + 1
        		continue
        	i = i + 1
        	try:
        		#print "_getOriginalSource, orignalAlignment.target:", orignalAlignment.target
        		#print "_getOriginalSource, target                 :", target
        		if self.compareTwoSentences(orignalAlignment.target, target):#orignalAlignment.target == target:#orignalAlignment.target == target:# or target in orignalAlignment.target or orignalAlignment.target in target:
        			#print "Found"
        			return (orignalAlignment.source, i)
        	except UnicodeDecodeError:
        			print "_getOriginalSource: Error IN UNICODE"
        #print "NOT Found"
        return (None, i)


    def writeSummary(self):
        self.outputFile.write("%s, %s, %s, %s, %s, %s, %s\n"%(self.count, self.passedAlignment, self.failedAlignment, self.timeTaken, self.averageSentencesLengthInSource, self.averageSentencesLengthInTarget, self.successful))
        self.outputFile.flush()
        
    def compareTwoSentences(self, first, second):
    	#compare two string, whether the first is contained in the second or the second is contained in the second    	
    	#print "compare two sentences ..."
    	if first and second:
    		#print "First: ", first, "Second: ", second
    		try:
    		
    			#first = first.encode('utf-8', "ignore")
        		#second = second.encode('utf-8', "ignore")
        		first = first.strip()
        		second = second.strip()
        		
	    		if first == second:#first in second or second in first :#first in second or second in first:	    			
	    			return True
	    		elif first in second or second in first:
	    			return False
	    		else:
	    			#print "NOT MATCHING..."
	    			return False
	    	except UnicodeDecodeError:
	    		print "compareTwoSentences: Error IN UNICODE"
	    		print traceback.format_exc()
	    		return False
        #print "One/Both of two sentences is null"
        #print "First : ", first
        #print "Second: ", second
        #print 
        return False
        
    def evaluateResult(self):
    	print "Evaluate Result"
        self.passedAlignment = 0 
        self.failedAlignment = 0
            
        correctAlignmentFile = open("%s_correct_test[%s].txt"%(self.AlignmentFilePath, self.count), 'w')    
        wrongAlignmentFile = open("%s_wrong_test[%s].txt"%(self.AlignmentFilePath, self.count), 'w')
        
        self.averageSentencesLengthInSource = 0 
        self.averageSentencesLengthInTarget = 0 
        
        file = open("alignmentResult.txt", 'w')
        for actualAlignment in self.actualAlignments:
        	file.write("%s\n"% str(actualAlignment))
        file.close()
        
        print "looping over actual alignments..."
        i = 0
        for actualAlignment in self.actualAlignments:
            print "Progress: %d out of %d"%(i , len(self.actualAlignments))
            i = i + 1
            #print "evaluateResult, actualAlignment.target: ", actualAlignment.target
            #goldenSource = self._getOriginalSource(actualAlignment.target)
            #print "goldenSource: ", goldenSource
            #print "actualSource: ", actualAlignment.source
            if self._doesAlignmentExistInGolden(actualAlignment):#self.compareTwoSentences(goldenSource, actualAlignment.source):#goldenTarget and goldenTarget == actualAlignment.target:
                self.passedAlignment +=1
                correctAlignmentFile.write(actualAlignment.source)
                correctAlignmentFile.write('\n')
                correctAlignmentFile.write(actualAlignment.target)
                correctAlignmentFile.write('\n')
                
                self.averageSentencesLengthInSource += len(actualAlignment.source)
                self.averageSentencesLengthInTarget += len(actualAlignment.target)
            else:
            	#print 
            	#print "================= Failed Alignemnt ================="
            	#print "actualAlignment.source   : ", actualAlignment.source
            	#print "originalAlignment.source : ", goldenSource
                self.failedAlignment +=1
                wrongAlignmentFile.write(actualAlignment.source)
                wrongAlignmentFile.write('\n')
                wrongAlignmentFile.write(actualAlignment.target)
                wrongAlignmentFile.write('\n')
                #print "Compare: %s, %s => %0.2f"%(goldenTarget, actualAlignment.target, difflib.SequenceMatcher(None, goldenTarget, actualAlignment.target).ratio())
            #break
                
        print ''
        print 'Failed Alignments :', self.failedAlignment
        print 'Passed Alignments :', self.passedAlignment
        
        self.averageSentencesLengthInSource = (float)(self.averageSentencesLengthInSource) / (float)(self.passedAlignment)
        self.averageSentencesLengthInTarget = (float)(self.averageSentencesLengthInTarget) / (float)(self.passedAlignment)
        
        correctAlignmentFile.flush()
        correctAlignmentFile.close()
        wrongAlignmentFile.flush()
        wrongAlignmentFile.close()
            
        
        
    #can be overriden if we need to pass specific format for the tool used
    def convertToSuitableFormat(self, filePath):
        return filePath
        
    def runTest(self):
        self.count = 0
        print ''
        
        self.outputFile.write("test_number, passed_alignments, failed_alignments, time_taken, average_english_sentence_length, average_arabic_sentence_length, Successful?\n")        
        #self.outputFile.write('Tool Name: %s\n'% self.TOOL_NAME)
        for (arabic_in, english_in, golden) in self.TestList:
            #self.outputFile.write('Test[%s]:\n'%self.count)
            print 'Running test:', self.count
            startTime = time.time()
            arabic_in_run = self.convertToSuitableFormat(arabic_in)
            english_in_run = self.convertToSuitableFormat(english_in) 
            self.successful = 'Yes'
                       
            try:
                #initializing the data
                self.count = 0.0  
                self.passedAlignment = 0.0
                self.failedAlignment = 0.0
                self.timeTaken = 0.0
                self.averageSentencesLengthInSource = 0.0
                self.averageSentencesLengthInTarget = 0.0
                
                
                self.runWithData(arabic_in_run, english_in_run)
                self.loadGoldenReference(golden)
                self.actualAlignments = []
                self.loadActualData(arabic_in, english_in)
                self.evaluateResult()
            except Exception,ex:
                print 'Failed test:', self.count
                print "Exception:", ex
                print traceback.format_exc()
                self.successful = 'No'
#                raise ex
#                
            print 'Finished test:', self.count
            print '============================'
            
            endTime = time.time()            
            self.timeTaken = endTime - startTime
            
            self.writeSummary()
            
            self.count +=1
            
        
if __name__=='__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(BaseToolTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
            
        
    