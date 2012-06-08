import sys, os
sourceFile = sys.argv[1]
targetFile = sys.argv[2]

f = open(sourceFile)
content = f.read()
f.close()
ps = content.split('\n')
result = list()

for p in ps:
    result.extend(p.split())
    result.append('.EOS')
    result.append('.EOP')

f = open(targetFile, 'w')
f.write('\n'.join(result))
f.close()