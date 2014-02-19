import re,string
import random
import sys
import time
class Preprocessing():
    exclude = set(string.punctuation)
    table = string.maketrans("","")
    def split_sentences(self,x):
        y=x.split('|||')
        return y
    def tokenize(self,x):
        y=x
        z=y.strip()
        newstring = z.lower()
        p=newstring.split(' ')
        for i in range(len(p)):
            alpha=p[i]
            if alpha.isdigit():
                p[i]='NUM'
        return p
            
    
def initialize_translation(source,target):
    corpus_length=len(source)
    source_words=set()
    target_words=set()
    t={}
    for k in range(corpus_length):
        for i in range(len(source[k])):
            source_words.add(source[k][i])
        for j in range(len(target[k])):
            target_words.add(target[k][j])
    t=initialize_weights(source,target,source_words,target_words)
    return t,source_words,target_words

def initialize(source_words,target_words, count):
    for (sword,tword) in count.keys():
        count[(sword,tword)]=0.0
    return count
            
def initialize_weights(source_corpus,target_corpus,source_words,target_words):
    t={}
    denom={}
    for k in range(len(target_corpus)):
        target_sentence=target_corpus[k]
        source_sentence=source_corpus[k]
        for tword in target_sentence:
            for sword in source_sentence:   
                if (sword,tword) not in t:
                    t[(sword,tword)]=0.0
                if tword not in denom:
                    denom[tword]=0.0
                t[(sword,tword)]+=1.0
                denom[tword]+=1.0
    for (sword,tword) in t.keys():
        t[(sword,tword)]=float(t[(sword,tword)]/denom[tword])
    print "WEIGHTS INITIALIZED T"    
    return t


        

def model1(source,target,t,source_words,target_words):
    count={}
    corpus_length=len(source)
    total = {}
    length=float(len(source_words))
    for k in range(corpus_length):
        source_sentence=source[k]
        target_sentence=target[k]
        for sword in source_sentence:
            fparamdenom=float(sum([t[(sword,tword)] for tword in target_sentence]))
            #fparamdenom=float(sum([t.get((sword,tword),1.0/length) for tword in target_sentence]))
            sum_delta=0.0
            for tword in target_sentence:
                #delta=float(t.get((sword,tword),float(1.0/length)))/fparamdenom
                #delta=float(t.get((sword,tword),t[tword]))/fparamdenom
                delta=float(t[(sword,tword)])/fparamdenom
                count[(sword,tword)] = float(count.get((sword,tword),0.0)) + delta
                total[tword] = float(total.get(tword,0.0)) + delta
                #total[sword] = float(total.get(sword,0.0)) + delta
                sum_delta+=delta
            if abs(sum_delta-float(1.0)) > 0.001:
               print sum_delta
               print "EXIT"
               exit()
        if k%1000 == 0:
            print k/1000,"% done"
            sys.stdout.flush()

    for (sword,tword) in count.keys():
        t[(sword,tword)]=float(count[(sword,tword)]/total[tword])
        #t[(sword,tword)]=float(count[(sword,tword)]/total[sword])
    return t

         
def hmm(source,target,t,source_words,target_words,count,total):
    sent_total={}
    corpus_length=len(source)
    for k in range(corpus_length):
        sent_total={}
        source_sentence=source[k]
        target_sentence=target[k]
        for sword in source_sentence:
            fparam=t[sword]
            fparamdenom[tword]=float(sum(fparam[tword] for tword in target_sentence))
            for tword in target_sentence:
                delta=float(tparam[tword])/fparamdenom
                if (sword,tword) not in counts:
                    count[(sword,tword)]=0
                    total[sword]=0
                count[(sword,tword)]+=delta
                total[sword]+=delta
    for sword in source_words:
        for tword in target_words:
            t[sword][tword]=float(count[sword][tword]/total[sword])
    return t
         
def alignment_model1(source,target,t):
    corpus_length=len(source)
    length = len(target_words)
    f=open('output.test.small.txt','w+')
    for k in range(corpus_length):
        print_string=''
        #for i in range(1,len(source[k])):
        a=[]
        for i in range(len(target[k])):
            tword=target[k][i]
            (prob,sword,jans)=max((t[(source[k][j],tword)],source[k][j],j) for j in range(len(source[k])))
            #print tword,sword,prob
            if jans >= 1:
               a.append((jans-1,i))
               #print_string+=str(jans-1)+"-"+str(i)+' '
        for tup in sorted(a):
            print_string+=str(tup[0])+"-"+str(tup[1])+' '
        f.write(print_string+'\n')
    f.close()


                    


        
        
if __name__=="__main__":
    source=[]
    target=[]
    p=Preprocessing()
    with open('test.data','r+') as g:
    #with open('data/dev-test-train.de-en','r+') as g:
         for myline in g.readlines():
             source_sent=p.split_sentences(myline.strip())[0]
             target_sent=p.split_sentences(myline.strip())[1]
             es=p.tokenize(source_sent)
             es.insert(0,'NULL')
             source.append(es)
             target.append(p.tokenize(target_sent))
    g.close()
    it=1
    count = {}
    total = {}
    t,source_words,target_words=initialize_translation(source,target)
    #t={}
    print "############"
    print "################"
    print "################"
    print "################"
    print "TRANSLATION MODEL initialised"
    print "init complete"
    print "source length = ", len(source_words)
    print "target length = ", len(target_words) 
    while it < 6:
        print 'iteration num',it
        sys.stdout.flush()
        #count=initialize(source_words,target_words,count)
        print 'starting estimation'
        t=model1(source,target,t,source_words,target_words)
        ans=float(sum([t.get((',',tgt),0) for tgt in target_words]))
        print "ANS",ans
        it+=1
        sys.stdout.flush()
    alignment_model1(source,target,t)
    for tgt in target_words:
    #for src in source_words:
        #ans=float(sum([t.get((src,tgt),0) for tgt in target_words]))
        ans=float(sum([t.get((src,tgt),0) for src in source_words]))
        if abs(float(ans)-1.0) > 0.001:
           print "MISTAKE"
           print src,ans
    print "###########"
    print ans
    print "###########"

