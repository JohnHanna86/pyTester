'''
Created on May 6, 2012

This module is used for manipulating the data in the UN Corpus, which is in tmx format, 
and also can be useful in any tmx parallel corpus 

@author: johnnabil
'''
import xml.dom.minidom
from xml.sax import saxutils, handler, make_parser

class CorpusHandler(handler.ContentHandler):
    def __init__(self, sourceLanguage, targetLanguage, secondTargetlanguage):
        self.sourceLang = sourceLanguage
        self.targetLang = targetLanguage
        self.secondTargetLang = secondTargetlanguage
        self.alignments = []
        self.currentLanguage = None
        self.currentSource = ''
        self.currentTarget = ''
        self.currentSecondTarget = ''
    
    def startElement(self, name, attrs):
        if name ==  'tuv':
            self.currentLanguage = attrs.get('xml:lang',"")
        elif name == 'tu':
            self.currentLanguage = None
            self.currentSource = ''            
            self.currentTarget = ''
            self.currentSecondTarget = ''
         

    
    def characters (self, ch):        
        if self.currentLanguage == self.sourceLang:
            self.currentSource += ch
        elif self.currentLanguage == self.targetLang:
            self.currentTarget += ch
        elif self.currentLanguage == self.secondTargetLang:
            self.currentSecondTarget += ch
    
    def endElement(self, name):
        if name ==  'tuv':
            self.currentLanguage = None
        elif name == 'tu':
            alignment = Alignment(self.currentSource, self.currentTarget, self.currentSecondTarget)
            self.alignments.append(alignment)
        
        
class Alignment(object):
    def __init__(self, source=None, target=None, secondTarget=None):
        self.source = source
        self.target = target
        self.secondTarget = secondTarget
        
    def __str__(self):
        return "%s \n--->\n %s \n--->\n %s"%(self.source, self.target, self.secondTarget)
        

class CorpusReader2(object):
    def __init__(self, corpusPath, sourceLanguage, targetLanguage, secondTargetlanguage):
        parser = make_parser()    
        curHandler = CorpusHandler(sourceLanguage, targetLanguage, secondTargetlanguage) 
        parser.setContentHandler(curHandler) 
        parser.parse(open(corpusPath)) 
        self.alignments = curHandler.alignments
    
        
#        self._doc = xml.dom.minidom.parse(corpusPath)
#        self.alignments = list()
#        for tu in self._doc.getElementsByTagName("tu"):
#            sourceSeg = None
#            targetSeg = None
#            for tuv in tu.getElementsByTagName('tuv'):  
#                lang = tuv.getAttribute('xml:lang')
#                if lang == sourceLanguage:
#                    sourceSeg = tuv.firstChild.firstChild.wholeText
#                if lang == targetLanguage:
#                    targetSeg = tuv.firstChild.firstChild.wholeText
#            alignment = Alignment(sourceSeg, targetSeg)
#            self.alignments.append(alignment)
                
    def sourceToString(self, numberOfSegments=None, seperator='\n'):
        """
        converts the text of the source language to plain text
        """
        count = 0
        source = ''
        for alignment in self.alignments:
            if numberOfSegments and numberOfSegments <= count:
                break
            source = "%s%s%s"%(source, seperator, alignment.source)
            count +=1
        return source
        
    def targetToString(self, numberOfSegments=None, seperator='\n'):
        """
        converts the text of the target language to plain text
        """
        count = 0
        target = ''
        for alignment in self.alignments:
            if numberOfSegments and numberOfSegments <= count:
                break
            target = "%s%s%s"%(target, seperator, alignment.target)
            count +=1
        return target

    def secondTargetToString(self, numberOfSegments=None, seperator='\n'):
        """
        converts the text of the target language to plain text
        """
        count = 0
        target = ''
        for alignment in self.alignments:
            if numberOfSegments and numberOfSegments <= count:
                break
            target = "%s%s%s"%(target, seperator, alignment.secondTarget)
            count +=1
        return target
    
    def getTargetSegment(self, sourceSegment):
        """
        get the corresponding target segment, given the source segment
        """
        result = []
        for alignment in self.alignments:
            if sourceSegment in alignment.source:
                result.append(alignment.target)
        return result
    
    def getSecondTargetSegment(self, sourceSegment):
        """
        get the corresponding target segment, given the source segment
        """
        result = []
        for alignment in self.alignments:
            if sourceSegment in alignment.source:
                result.append(alignment.secondTarget)
        return result

    def getSourceSegment(self, targetSegment):
        """
        get the corresponding source segment, given the target segnment
        """
        result = []
        for alignment in self.alignments:
            if targetSegment in alignment.target:
                result.append(alignment.source)
        return result
    
    def numberOfWordsInSource(self):
        """
        get the total number of tokens in the source language text
        """
        return float(len(self.sourceToString().split()))
    
    def numberOfWordsInTarget(self):
        """
        get the total number of tokens in the target language text
        """
        return float(len(self.targetToString().split()))
    
    def numberOfWordsInSecondTarget(self):
        """
        get the total number of tokens in the target language text
        """
        return float(len(self.secondTargetToString().split()))
    
    def countInSource(self, word):
        """
        count the number of occurences of given word in the source text
        """
        return float(self.sourceToString().count(word))
    
    def countInTarget(self, word):
        """
        count the number of occurences of given word in the target text
        """
        return float(self.targetToString().count(word))
    
    def countInSecondTarget(self, word):
        """
        count the number of occurences of given word in the target text
        """
        return float(self.secondTargetToString().count(word))
    