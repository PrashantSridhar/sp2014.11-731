import re,string
import random
import sys
import time

class Preprocessing():

    def split_sentences(self,x):
        return x.split('|||')
    def tokenize(self,y):
        z=y.strip()
        newstring = z.lower()
        p=newstring.split(' ')
        for i in range(len(p)):
            alpha=p[i]
            if alpha.isdigit():
                p[i]='NUM'
        return p
            

def initialize_translation(source, target):
	translation = {}
	for k in range(len( source)):
		
		source_sentence = source[k]
		target_sentence = target[k]

		for sword in source_sentence:
			if sword not in translation:
				translation[sword] = {}
			for tword in target_sentence:
				translation[sword][tword] = 1.0

	for sword in translation:
		length = len(translation[sword])
		for tword in translation[sword]:
			translation[sword][tword] = 1.0 / float(length)

	return translation


def model1(source, target ,translation ):
	count = {}
	total =  {}
	for i in range(len(source)):
		source_sentence = source[i]
		target_sentence = target[i]
		for sword in source_sentence:

			denom = float ( sum ( [float ( translation[sword][tword] ) for tword in target_sentence ] ) ) 
			for tword in target_sentence:

				delta = float ( translation[sword][tword] ) / float ( denom ) 
				count[(sword,tword)] = count.get((sword,tword) , 0.0) + delta
				total[sword] = total.get(sword , 0.0) + delta 

		if i % 1000 == 0:
			print str(i/1000) + "% complete"
	for (sword, tword) in  count:
		translation[sword][tword] = float(count[(sword, tword)]) / total[sword]

	return translation

def alignment_model1(source, target, translation):

	l=len(source)
	f=open('output.txt','w')
	for k in range(l):
		source_sentence = source[k]
		target_sentence = target[k]
		print_string=''
		for i in range(len(target_sentence)):
			tword=target_sentence[i]
			(prob,sword,ind)=max( [ ( translation [ source_sentence[j]][tword],source_sentence[j],j) for j in range(len(source_sentence)) ]) 
			if ind > 0:
				print tword,sword,prob
				print_string+=str(ind-1)+"-"+str(i)+' '

		f.write(print_string+'\n')
	f.close()


if __name__ == "__main__":
    source=[]
    target=[]
    p=Preprocessing()
    #with open('test.data','r+') as g:
    with open('data/dev-test-train.de-en','r+') as g:
    	i = 0
        for myline in g.readlines():
            source_sent=p.split_sentences(myline.strip())[0]
            target_sent=p.split_sentences(myline.strip())[1]
            es=p.tokenize(source_sent)
            es.insert(0,'NULL')
            source.append(es)
            target.append(p.tokenize(target_sent))
            i += 1
            if i == 5000:
            	break
    g.close()
    it=1
    t = initialize_translation(source,target)
    for sword in t:
    	assert abs(sum([t[sword][tword] for tword in t[sword]]) -1.0) < 0.0001
    while it < 6:
        print 'iteration num',it

        t=model1(source,target,t)

        it+=1
        sys.stdout.flush()
    alignment_model1(source,target,t)
