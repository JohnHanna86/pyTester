'''
Created on Apr 22, 2010

@author: johnnabil
'''
import sys, os
sourceFile = sys.argv[1]
targetFile = sys.argv[2]

def convert(lines):
    count = 0 
    for c in lines:
        target.write('\n%s <EOS>'%count)
        count = convertLine(c, count)
        
def convertLine(content, count):
    mid = 0
    currentWord = list()
    
    for i in range(len(content)):
        c = content[i]
        mid +=1
        currentWord.append(c)
        
        if c == ' ' or i == len(content)-1:            
            target.write('\n%s %s'%(''.join(currentWord), count + float(mid)/2.0))
            count += mid
            mid = 0
            currentWord = list()
            
    return count
            

#convert(['This is a test.', 'john was here lol.'])

f = open(sourceFile)
target = open(targetFile, 'w')
convert(f.read().split('\n'))
target.flush()
f.close()
target.close()         