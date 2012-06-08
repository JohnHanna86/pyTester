'''
Created on Mar 1, 2010

@author: johnnabil
'''
import xml.dom.minidom


class CorpusBuilder(object):
    
    def __init__(self, source, target, sourceLanguage, targetLanguage):
        """
        param source: is list of statements in the source language
        param target: is list of statements in the target language
        
        sourceLanguage: name of source language, e.g. AR
        targetLanguage: name of target language, e.g. EN
        """
        self.source = source
        self.target = target
        self.sourceLanguage = sourceLanguage
        self.targetLanguage = targetLanguage
        
        if len(source) != len(target):
            raise RuntimeError('length of source does not equal to length target') 
        
    def buildCorpus(self, outputPath):
        doc = xml.dom.minidom.Document()
        tmx = doc.createElement("tmx")
        tmx.setAttribute('version', '1.4')
        doc.appendChild(tmx)
        
        body = doc.createElement('body')
        tmx.appendChild(body)
        
        
        for i in range(len(self.source)):
        	print "%d out of %d"%(i, len(self.source))
            sourceSentence = self.source[i]
            targetSentence = self.target[i]
            tu = doc.createElement('tu')
            tu.setAttribute('tuid', str(i))
            body.appendChild(tu)
            
            # source tag
            tuv = doc.createElement('tuv')
            tuv.setAttribute('xml:lang', self.sourceLanguage)
            tu.appendChild(tuv)
            
            seg = doc.createElement('seg')
            tuv.appendChild(seg)
            
            srcNode = doc.createTextNode(sourceSentence)
            seg.appendChild(srcNode)
            
            # target tag
            tuv = doc.createElement('tuv')
            tuv.setAttribute('xml:lang', self.targetLanguage)
            tu.appendChild(tuv)
            
            seg = doc.createElement('seg')
            tuv.appendChild(seg)
            
            targetNode = doc.createTextNode(targetSentence)
            seg.appendChild(targetNode)
        print "Writing content ...."
        content = doc.toprettyxml(indent=' ')
        f = open(outputPath, 'w')
        print "Encoding content ..."
        content = content.encode('utf-8')
        f.write(content)
        f.close()   
        print "Finished !"
