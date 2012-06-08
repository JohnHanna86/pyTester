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

phrasesPerFile = 100

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
    PartitionedTestCase("uncorpora_nolayout_20090710.tmx", 6000, 1000, 10, "1000 random phrase from UN corpus without seperators")
    PartitionedTestCase("uncorpora_nolayout_20090710.tmx", 9000, 1000, 11, "1000 random phrase from UN corpus without seperators")
    PartitionedTestCase("uncorpora_nolayout_20090710.tmx", 9000, 1000, 12, "1000 random phrase from UN corpus without seperators")
    PartitionedTestCase("uncorpora_nolayout_20090710.tmx", 9000, 1000, 13, "1000 random phrase from UN corpus without seperators")
    
def testCase1():
    PartitionedTestCase("uncorpora_nolayout_20090710.tmx", 60000, 2000, 20, "2000 random phrase from UN corpus without seperators")
    PartitionedTestCase("uncorpora_nolayout_20090710.tmx", 60000, 2000, 21, "2000 random phrase from UN corpus without seperators")
    PartitionedTestCase("uncorpora_nolayout_20090710.tmx", 60000, 2000, 22, "2000 random phrase from UN corpus without seperators")
    PartitionedTestCase("uncorpora_nolayout_20090710.tmx", 60000, 2000, 23, "2000 random phrase from UN corpus without seperators")
    
def testCase2():
    PartitionedTestCase("uncorpora_nolayout_20090710.tmx", 60000, 6000, 30, "6000 random phrase from UN corpus without seperators")
    PartitionedTestCase("uncorpora_nolayout_20090710.tmx", 60000, 9000, 31, "9000 random phrase from UN corpus without seperators")
    PartitionedTestCase("uncorpora_nolayout_20090710.tmx", 60000, 9000, 32, "9000 random phrase from UN corpus without seperators")
    PartitionedTestCase("uncorpora_nolayout_20090710.tmx", 60000, 9000, 33, "9000 random phrase from UN corpus without seperators")

def testCase3():
    PartitionedTestCase("uncorpora_nolayout_20090710.tmx", 60000, 6000, 40, "6000 random phrase from UN corpus with newlines and tabs", ['\n', '\t'])
    PartitionedTestCase("uncorpora_nolayout_20090710.tmx", 60000, 9000, 41, "9000 random phrase from UN corpus with newlines and tabs", ['\n', '\t'])
    PartitionedTestCase("uncorpora_nolayout_20090710.tmx", 60000, 9000, 42, "9000 random phrase from UN corpus with newlines and tabs", ['\n', '\t'])
    PartitionedTestCase("uncorpora_nolayout_20090710.tmx", 60000, 9000, 43, "9000 random phrase from UN corpus with newlines and tabs", ['\n', '\t'])
    

def testCase4():
    PartitionedTestCase("uncorpora_nolayout_20090710.tmx", 60000, 6000, 50, "6000 random phrase from UN corpus with newlines , tabs, spaces, dots , and commmas", ['\n', '\t', '   ', '.', ','])
    PartitionedTestCase("uncorpora_nolayout_20090710.tmx", 60000, 9000, 51, "9000 random phrase from UN corpus with newlines , tabs, spaces, dots , and commmas", ['\n', '\t', '   ', '.', ','])
    PartitionedTestCase("uncorpora_nolayout_20090710.tmx", 60000, 9000, 52, "9000 random phrase from UN corpus with newlines , tabs, spaces, dots , and commmas", ['\n', '\t', '   ', '.', ','])
    PartitionedTestCase("uncorpora_nolayout_20090710.tmx", 60000, 9000, 53, "9000 random phrase from UN corpus with newlines , tabs, spaces, dots , and commmas", ['\n', '\t', '   ', '.', ','])

def testCase5():
    PartitionedTestCase("uncorpora_nolayout_20090710.tmx", 60000, 6000, 60, "6000 random phrase from UN corpus with newlines , tabs, spaces, dots , and commmas, with spurious phrases 200 arabic, 100 english", ['\n', '\t', '   ', '.', ','], 200, 100)
    PartitionedTestCase("uncorpora_nolayout_20090710.tmx", 60000, 9000, 61, "9000 random phrase from UN corpus with newlines , tabs, spaces, dots , and commmas, with spurious phrases 300 arabic, 200 english", ['\n', '\t', '   ', '.', ','], 300, 200)
    PartitionedTestCase("uncorpora_nolayout_20090710.tmx", 60000, 9000, 62, "9000 random phrase from UN corpus with newlines , tabs, spaces, dots , and commmas, with spurious phrases 300 arabic, 200 english", ['\n', '\t', '   ', '.', ','], 300, 200)
    PartitionedTestCase("uncorpora_nolayout_20090710.tmx", 60000, 9000, 63, "9000 random phrase from UN corpus with newlines , tabs, spaces, dots , and commmas, with spurious phrases 300 arabic, 200 english", ['\n', '\t', '   ', '.', ','], 300, 200)

def testCase6():
    PartitionedTestCase("uncorpora_nolayout_20090710.tmx", 60000, 1000, 70, "1000 random phrase from UN corpus with newlines , tabs, spaces, dots , and commmas, with spurious phrases 20 arabic, 10 english", ['\n', '\t', '   ', '.', ','], 20, 10)
    PartitionedTestCase("uncorpora_nolayout_20090710.tmx", 60000, 1000, 71, "1000 random phrase from UN corpus with newlines , tabs, spaces, dots , and commmas, with spurious phrases 30 arabic, 20 english", ['\n', '\t', '   ', '.', ','], 30, 20)
    PartitionedTestCase("uncorpora_nolayout_20090710.tmx", 60000, 1000, 72, "1000 random phrase from UN corpus with newlines , tabs, spaces, dots , and commmas, with spurious phrases 30 arabic, 20 english", ['\n', '\t', '   ', '.', ','], 30, 20)
    PartitionedTestCase("uncorpora_nolayout_20090710.tmx", 60000, 1000, 73, "1000 random phrase from UN corpus with newlines , tabs, spaces, dots , and commmas, with spurious phrases 30 arabic, 20 english", ['\n', '\t', '   ', '.', ','], 30, 20)

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

    print "TestCase[4]:"
    testCase4()
    
    print "TestCase[5]:"
    testCase5()
    
    print "TestCase[6]:"
    testCase6()

    print "Writing %s/InputData.xml"%OUTPUT_PATH
    inputData = open('%s/InputData.xml' % OUTPUT_PATH, 'w')
    inputData.write(doc.toprettyxml(indent="  "))
    inputData.flush()
    inputData.close()
    
    
    print "Done!"
