'''
Created on May 10, 2011

@author: John Nabil
'''
import ConfigParser
import random
from CorpusReader import CorpusReader
from CorpusReader import Alignment
from xml.dom.minidom import Document


CONFIG_FILE='config/cfg.ini'
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
    test.setAttribute("id", "%s"%index)
    
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


def generateRandomList(count, min, max ,allowRepeat=False):
    l = list()
    while len(l) < count:
        number = int(random.random() * (max-min) + min)
        if not allowRepeat:
            while number in l:            
                number = int(random.random() * (max-min) + min)
        l.append(number)
    return l    
    

def normalTestCase(dbName, count, testCaseNumber, description, seperators=['\n'], numberOfARSpuriousPhrases=0, numberOfENSpuriousPhrases=0):
    corpus_path = "%s/%s"%(DATA_PATH, dbName)
    reader = CorpusReader(corpus_path, 'AR', 'EN')    
    l = generateRandomList(count, 10, count, True)
    arabicText = ''
    englishText = ''
    
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
                    arabicText = "%s %s %s"%(arabicText, seperator , alignment.source)
                    numberOfARSpuriousPhrases = numberOfARSpuriousPhrases - 1                    
                elif numberOfENSpuriousPhrases > 0:
                    #print "Putting spurious english phrase, #: ", numberOfENSpuriousPhrases
                    englishText = "%s %s %s"%(englishText, seperator, alignment.target)
                    numberOfENSpuriousPhrases = numberOfENSpuriousPhrases - 1
            else:
                arabicText = "%s %s %s"%(arabicText, seperator , alignment.source)
                englishText = "%s %s %s"%(englishText, seperator, alignment.target)
        else:        
            arabicText = "%s %s %s"%(arabicText, seperator , alignment.source)
            englishText = "%s %s %s"%(englishText, seperator, alignment.target)
    
    
    arabicFile = open("%s/arabic.small.%s.txt"%(OUTPUT_PATH, testCaseNumber), 'w')
    englishFile = open("%s/english.small.%s.txt"%(OUTPUT_PATH, testCaseNumber), 'w')
    
    print "Writing arabic file:", "%s/arabic.small.%s.txt"%(OUTPUT_PATH, testCaseNumber)
    arabicFile.write(arabicText.encode('utf-8'))
    arabicFile.flush()
    
    print "Writing english file", "%s/english.small.%s.txt"%(OUTPUT_PATH, testCaseNumber)
    englishFile.write(englishText.encode('utf-8'))
    englishFile.flush()    
    
    addTestCaseXML(description, "arabic.small.%s.txt"%(testCaseNumber), "english.small.%s.txt"%(testCaseNumber), dbName)
    
def testCase0():    
    normalTestCase("arabic_english_randomSelected_UN_6399_sentence.tmx", 1000, 10, "1000 random phrase from UN corpus without seperators")
    normalTestCase("arabic_english_randomSelected_UN_9300_sentence.tmx", 1000, 11, "1000 random phrase from UN corpus without seperators")
    normalTestCase("arabic_english_randomSelected_UN_9313_sentence.tmx", 1000, 12, "1000 random phrase from UN corpus without seperators")
    normalTestCase("arabic_english_randomSelected_UN_9319_sentence.tmx", 1000, 13, "1000 random phrase from UN corpus without seperators")
    normalTestCase("arabic_english_full_Meedan_19957_sentence.tmx", 1000, 14, "1000 random phrase from UN corpus without seperators")
    normalTestCase("arabic_english_randomSelected_UN_9319_sentence.tmx", 1000, 15, "1000 random phrase from Meedan corpus without seperators")
    normalTestCase("memoire_en-US_ar.tmx", 1000, 16, "1000 random phrase from french mozilla corpus without seperators")

def testCase1():
    normalTestCase("arabic_english_randomSelected_UN_6399_sentence.tmx", 2000, 20, "2000 random phrase from UN corpus without seperators")
    normalTestCase("arabic_english_randomSelected_UN_9300_sentence.tmx", 2000, 21, "2000 random phrase from UN corpus without seperators")
    normalTestCase("arabic_english_randomSelected_UN_9313_sentence.tmx", 2000, 22, "2000 random phrase from UN corpus without seperators")
    normalTestCase("arabic_english_randomSelected_UN_9319_sentence.tmx", 2000, 23, "2000 random phrase from UN corpus without seperators")
    normalTestCase("arabic_english_full_Meedan_19957_sentence.tmx", 2000, 24, "2000 random phrase from UN corpus without seperators")
    normalTestCase("arabic_english_randomSelected_UN_9319_sentence.tmx", 2000, 25, "2000 random phrase from Meedan corpus without seperators")
    normalTestCase("memoire_en-US_ar.tmx", 1000, 26, "2000 random phrase from french mozilla corpus without seperators")
    
def testCase2():
    normalTestCase("arabic_english_randomSelected_UN_6399_sentence.tmx", 6000, 30, "6000 random phrase from UN corpus without seperators")
    normalTestCase("arabic_english_randomSelected_UN_9300_sentence.tmx", 9000, 31, "9000 random phrase from UN corpus without seperators")
    normalTestCase("arabic_english_randomSelected_UN_9313_sentence.tmx", 9000, 32, "9000 random phrase from UN corpus without seperators")
    normalTestCase("arabic_english_randomSelected_UN_9319_sentence.tmx", 9000, 33, "9000 random phrase from UN corpus without seperators")
    normalTestCase("arabic_english_full_Meedan_19957_sentence.tmx", 19000, 34, "19000 random phrase from UN corpus without seperators")
    normalTestCase("arabic_english_randomSelected_UN_9319_sentence.tmx", 9000, 35, "9000 random phrase from Meedan corpus without seperators")
    normalTestCase("memoire_en-US_ar.tmx", 12000, 36, "12000 random phrase from french mozilla corpus without seperators")

def testCase3():
    normalTestCase("arabic_english_randomSelected_UN_6399_sentence.tmx", 1000, 40, "6000 random phrase from UN corpus with newlines and tabs", ['\n', '\t'])
    normalTestCase("arabic_english_randomSelected_UN_9300_sentence.tmx", 1000, 41, "9000 random phrase from UN corpus with newlines and tabs", ['\n', '\t'])
    normalTestCase("arabic_english_randomSelected_UN_9313_sentence.tmx", 1000, 42, "9000 random phrase from UN corpus with newlines and tabs", ['\n', '\t'])
    normalTestCase("arabic_english_randomSelected_UN_9319_sentence.tmx", 1000, 43, "9000 random phrase from UN corpus with newlines and tabs", ['\n', '\t'])
    normalTestCase("arabic_english_full_Meedan_19957_sentence.tmx", 1000, 44, "19000 random phrase from UN corpus with newlines and tabs", ['\n', '\t'])
    normalTestCase("arabic_english_randomSelected_UN_9319_sentence.tmx", 1000, 45, "9000 random phrase from Meedan corpus with newlines and tabs", ['\n', '\t'])
    normalTestCase("memoire_en-US_ar.tmx", 1000, 46, "1000 random phrase from french mozilla corpus with newlines and tab", ['\n', '\t'])
    

def testCase4():
    normalTestCase("arabic_english_randomSelected_UN_6399_sentence.tmx", 1000, 50, "6000 random phrase from UN corpus with newlines , tabs, spaces, dots , and commmas", ['\n', '\t', '   ', '.', ','])
    normalTestCase("arabic_english_randomSelected_UN_9300_sentence.tmx", 1000, 51, "9000 random phrase from UN corpus with newlines , tabs, spaces, dots , and commmas", ['\n', '\t', '   ', '.', ','])
    normalTestCase("arabic_english_randomSelected_UN_9313_sentence.tmx", 1000, 52, "9000 random phrase from UN corpus with newlines , tabs, spaces, dots , and commmas", ['\n', '\t', '   ', '.', ','])
    normalTestCase("arabic_english_randomSelected_UN_9319_sentence.tmx", 1000, 53, "9000 random phrase from UN corpus with newlines , tabs, spaces, dots , and commmas", ['\n', '\t', '   ', '.', ','])
    normalTestCase("arabic_english_full_Meedan_19957_sentence.tmx", 1000, 54, "19000 random phrase from UN corpus with newlines , tabs, spaces, dots , and commmas", ['\n', '\t', '   ', '.', ','])
    normalTestCase("arabic_english_randomSelected_UN_9319_sentence.tmx", 1000, 55, "9000 random phrase from UN corpus with newlines , tabs, spaces, dots , and commmas", ['\n', '\t', '   ', '.', ','])
    normalTestCase("memoire_en-US_ar.tmx", 1000, 56, "1000 random phrase from french mozilla corpus with newlines , tabs, spaces, dots , and commmas", ['\n', '\t', '   ', '.', ','])

def testCase5():
    normalTestCase("arabic_english_randomSelected_UN_6399_sentence.tmx", 1000, 60, "6000 random phrase from UN corpus with newlines , tabs, spaces, dots , and commmas, with spurious phrases 30 arabic, 20 english", ['\n', '\t', '   ', '.', ','], 30, 20)
    normalTestCase("arabic_english_randomSelected_UN_9300_sentence.tmx", 1000, 61, "9000 random phrase from UN corpus with newlines , tabs, spaces, dots , and commmas, with spurious phrases 30 arabic, 20 english", ['\n', '\t', '   ', '.', ','], 30, 20)
    normalTestCase("arabic_english_randomSelected_UN_9313_sentence.tmx", 1000, 62, "9000 random phrase from UN corpus with newlines , tabs, spaces, dots , and commmas, with spurious phrases 30 arabic, 20 english", ['\n', '\t', '   ', '.', ','], 30, 20)
    normalTestCase("arabic_english_randomSelected_UN_9319_sentence.tmx", 1000, 63, "9000 random phrase from UN corpus with newlines , tabs, spaces, dots , and commmas, with spurious phrases 30 arabic, 20 english", ['\n', '\t', '   ', '.', ','], 30, 20)
    normalTestCase("arabic_english_full_Meedan_19957_sentence.tmx", 1000, 64, "19000 random phrase from UN corpus with newlines , tabs, spaces, dots , and commmas, with spurious phrases 30 arabic, 20 english", ['\n', '\t', '   ', '.', ','], 30, 20)
    normalTestCase("arabic_english_randomSelected_UN_9319_sentence.tmx", 1000, 65, "9000 random phrase from UN corpus with newlines , tabs, spaces, dots , and commmas, with spurious phrases 30 arabic, 20 english", ['\n', '\t', '   ', '.', ','], 30, 20)
    normalTestCase("memoire_en-US_ar.tmx", 1000, 66, "1000 random phrase from french mozilla corpus with newlines , tabs, spaces, dots , and commmas, with spurious phrases 30 arabic, 20 english", ['\n', '\t', '   ', '.', ','], 30, 20)

def testCase6():
    normalTestCase("arabic_english_randomSelected_UN_6399_sentence.tmx", 1000, 70, "1000 random phrase from UN corpus with newlines , tabs, spaces, dots , and commmas, with spurious phrases 90 arabic, 60 english", ['\n', '\t', '   ', '.', ','], 90, 60)
    normalTestCase("arabic_english_randomSelected_UN_9300_sentence.tmx", 1000, 71, "1000 random phrase from UN corpus with newlines , tabs, spaces, dots , and commmas, with spurious phrases 90 arabic, 60 english", ['\n', '\t', '   ', '.', ','], 90, 60)
    normalTestCase("arabic_english_randomSelected_UN_9313_sentence.tmx", 1000, 72, "1000 random phrase from UN corpus with newlines , tabs, spaces, dots , and commmas, with spurious phrases 90 arabic, 60 english", ['\n', '\t', '   ', '.', ','], 90, 60)
    normalTestCase("arabic_english_randomSelected_UN_9319_sentence.tmx", 1000, 73, "1000 random phrase from UN corpus with newlines , tabs, spaces, dots , and commmas, with spurious phrases 90 arabic, 60 english", ['\n', '\t', '   ', '.', ','], 90, 60)
    normalTestCase("arabic_english_full_Meedan_19957_sentence.tmx", 1000, 74, "1000 random phrase from UN corpus with newlines , tabs, spaces, dots , and commmas, with spurious phrases 90 arabic, 60 english", ['\n', '\t', '   ', '.', ','], 90, 60)
    normalTestCase("arabic_english_randomSelected_UN_9319_sentence.tmx", 1000, 75, "1000 random phrase from UN corpus with newlines , tabs, spaces, dots , and commmas, with spurious phrases 90 arabic, 60 english", ['\n', '\t', '   ', '.', ','], 90, 60)
    normalTestCase("memoire_en-US_ar.tmx", 1000, 76, "1000 random phrase from french mozilla corpus with newlines , tabs, spaces, dots , and commmas, with spurious phrases 90 arabic, 60 english", ['\n', '\t', '   ', '.', ','], 90, 60)


if __name__=='__main__':
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
    #testCase2()
    
    print "TestCase[3]:"
    testCase3()

    print "TestCase[4]:"
    testCase4()
    
    print "TestCase[5]:"
    testCase5()
    
    print "TestCase[6]:"
    testCase6()

    print "Writing InputData.xml"
    inputData = open('%s/InputData.xml'%OUTPUT_PATH, 'w')
    inputData.write(doc.toprettyxml(indent="  "))
    inputData.flush()
    inputData.close()
    
    
    print "Done!"