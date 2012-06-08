'''
Created on May 10, 2011

@author: John Nabil
'''
'''
generates [n] sets of two alignments (arabic-english) & (french-english) on the same level so they have the same statements, 
i.e the english statements are common between the two alignments 

'''

import ConfigParser
import random
from CorpusReader2 import CorpusReader2
#from CorpusReader import CorpusReader
from CorpusReader import Alignment
from xml.dom.minidom import Document

phrasesPerFile = 200

CONFIG_FILE = 'config/cfg.ini'
DATA_PATH = ''
OUTPUT_PATH = ''

doc = Document()

# Create the <data> base element
data = doc.createElement("data")
doc.appendChild(data)

index = 0

def addTestCaseXML(_description, _source, _target, _golden):
    global index
    # for each Testcase
    test = doc.createElement("test")
    test.setAttribute("id", "%s" % index)
    
    description = doc.createElement("description")
    test.appendChild(description)
    descriptionText = doc.createTextNode(_description)
    description.appendChild(descriptionText)
    test.appendChild(description)
    
    source = doc.createElement("source")
    test.appendChild(source)
    sourceText = doc.createTextNode(_source)
    source.appendChild(sourceText)
    test.appendChild(source)
    
    target = doc.createElement("target")
    test.appendChild(target)
    targetText = doc.createTextNode(_target)
    target.appendChild(targetText)
    test.appendChild(target)
    
    golden = doc.createElement("golden")
    test.appendChild(golden)
    goldenText = doc.createTextNode(_golden)
    golden.appendChild(goldenText)
    test.appendChild(golden)

    data.appendChild(test)
    index = index + 1


def generateRandomList(count, min, max , allowRepeat=False):
    l = list()
    while len(l) < count:
        number = int(random.random() * (max - min) + min)
        if not allowRepeat:
            while number in l:            
                number = int(random.random() * (max - min) + min)
        l.append(number)
    return l    
    

def normalTestCase(dbName, dbSize, count, testCaseNumber, description, seperators=['\n'], numberOfARSpuriousPhrases=0, numberOfENSpuriousPhrases=0):
    addTestCaseXML(description, "arabic.small.%s.txt" % (testCaseNumber), "english.small.%s.txt" % (testCaseNumber), dbName)
    #return
    corpus_path = "%s/%s" % (DATA_PATH, dbName)
    reader = CorpusReader2.CorpusReader2(corpus_path, 'AR', 'EN', 'FR')    
    l = generateRandomList(count, 10, dbSize, True)
    arabicText = ''
    englishText = ''
    frenchText = ''
    
    for index in l:
        
        seperator = u''
        if len(seperators) > 0:
            sepIndex = int(random.random() * len(seperators))
            seperator = seperators[sepIndex]
            
        alignment = reader.alignments[index]
        if numberOfARSpuriousPhrases != 0 or numberOfENSpuriousPhrases != 0:
            insertSpuriousPhrases = random.random() > 0.5
            if insertSpuriousPhrases:
                willItBeArabic = random.random() > 0.5
                if willItBeArabic and numberOfARSpuriousPhrases > 0:
                    #print "Putting spurious arabic phrase, #: ", numberOfARSpuriousPhrases
                    arabicText = "%s %s %s" % (arabicText, seperator , alignment.source)
                    numberOfARSpuriousPhrases = numberOfARSpuriousPhrases - 1                    
                elif numberOfENSpuriousPhrases > 0:
                    #print "Putting spurious english phrase, #: ", numberOfENSpuriousPhrases
                    englishText = "%s %s %s" % (englishText, seperator, alignment.target)
                    frenchText = "%s %s %s" % (frenchText, seperator, alignment.secondTarget)
                    numberOfENSpuriousPhrases = numberOfENSpuriousPhrases - 1
            else:
                arabicText = "%s %s %s" % (arabicText, seperator , alignment.source)
                englishText = "%s %s %s" % (englishText, seperator, alignment.target)
                frenchText = "%s %s %s" % (frenchText, seperator, alignment.secondTarget)
        else:        
            arabicText = "%s %s %s" % (arabicText, seperator , alignment.source)
            englishText = "%s %s %s" % (englishText, seperator, alignment.target)
            frenchText = "%s %s %s" % (frenchText, seperator, alignment.secondTarget)
    
    
    arabicFile = open("%s/arabic.small.%s.txt" % (OUTPUT_PATH, testCaseNumber), 'w')
    englishFile = open("%s/english.small.%s.txt" % (OUTPUT_PATH, testCaseNumber), 'w')
    frenchFile = open("%s/french.small.%s.txt" % (OUTPUT_PATH, testCaseNumber), 'w')
    
    print "Writing arabic file:", "%s/arabic.small.%s.txt" % (OUTPUT_PATH, testCaseNumber)
    arabicFile.write(arabicText.encode('utf-8'))
    arabicFile.flush()
    
    print "Writing english file", "%s/english.small.%s.txt" % (OUTPUT_PATH, testCaseNumber)
    englishFile.write(englishText.encode('utf-8'))
    englishFile.flush()
    
    print "Writing french file", "%s/french.small.%s.txt" % (OUTPUT_PATH, testCaseNumber)
    frenchFile.write(frenchText.encode('utf-8'))
    frenchFile.flush()    
    
    addTestCaseXML(description, "arabic.small.%s.txt" % (testCaseNumber), "english.small.%s.txt" % (testCaseNumber), dbName)
    
def PartitionedTestCase(dbName, dbSize, count, testCaseNumber, description, seperators=['\n'], numberOfARSpuriousPhrases=0, numberOfENSpuriousPhrases=0):
    normalTestCase(dbName, dbSize, count, testCaseNumber, description, seperators, numberOfARSpuriousPhrases, numberOfENSpuriousPhrases)
    return;
    numberOfFiles = count / phrasesPerFile
    numberOfARSpuriousPhrases = numberOfARSpuriousPhrases/numberOfFiles
    numberOfENSpuriousPhrases = numberOfENSpuriousPhrases/numberOfFiles 
    
    for i in range(numberOfFiles):
        testCaseNumber = testCaseNumber + 0.001
        normalTestCase(dbName, dbSize, count, testCaseNumber, description, seperators, numberOfARSpuriousPhrases, numberOfENSpuriousPhrases)    
    
    
    
def testCase0():    
	# testing without seperators nor garabage
	begin = 10
	for i in range(1, 11, 2):
		PartitionedTestCase("uncorpora_nolayout_20090710.tmx", 60000, 100 * i, begin, "%d random phrase from UN corpus without seperators"%(100*i))
		begin = begin + 1
    

def testCase1():
	#testing with seperators only
	begin = 20
	for i in range(1, 11, 2):
		PartitionedTestCase("uncorpora_nolayout_20090710.tmx", 60000, 100 * i, begin, "%d random phrase from UN corpus with newlines and tabs"%(100*i), ['\n', '\t', '   ', '.', ','])
		begin = begin + 1
		
def testCase2():
	#testing with garbage only
	begin = 30
	for i in range(1, 11, 2):
	    PartitionedTestCase("uncorpora_nolayout_20090710.tmx", 60000, 200, begin, "200 random phrase from UN corpus with spurious phrases %d arabic, %d english"%(20*i, 10*i), ['\n'], 20*i, 10*i)
        begin = begin + 1

def testCase3():
	#testing with seperators and garabage
	begin = 40
	for i in range(1, 11, 2):
		PartitionedTestCase("uncorpora_nolayout_20090710.tmx", 60000, 200, begin, "120 random phrase from UN corpus with newlines , tabs, spaces, dots , and commmas, with spurious phrases %d arabic, %d english"%(20*i, 10*i), ['\n', '\t', '   ', '.', ','], 20*i, 10*i)
		begin = begin + 1
    

if __name__ == '__main__':
    config = ConfigParser.ConfigParser()
    config.readfp(open(CONFIG_FILE))    
    DATA_PATH = config.get('main', 'input_path')
    OUTPUT_PATH = config.get('main', 'testCases_path')
    
    print "Copora Path: ", DATA_PATH
    print "TestCases Path: ", OUTPUT_PATH
    
    
    
    print "TestCase[0]:"
    testCase0()
    
    print "TestCase[1]:"
    testCase1()
    
    print "TestCase[2]:"
    testCase2()
    
    print "TestCase[3]:"
    testCase3()

    
    print "Writing %s/InputData.xml"%OUTPUT_PATH
    inputData = open('%s/InputData.xml' % OUTPUT_PATH, 'w')
    inputData.write(doc.toprettyxml(indent="  "))
    inputData.flush()
    inputData.close()
    
    
    print "Done!"
