import pdb

def createGenerator():
    myList = range(3)
    for i in myList:
        pdb.set_trace()
        yield i*i
        
myGenerator = createGenerator()
print '\ncreated generator\n'
for i in myGenerator:
    print('\n\nouput: ' + str(i) + '\n')
    