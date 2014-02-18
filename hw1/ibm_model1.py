import re,string
import random
import sys
class Preprocessing():
    exclude = set(string.punctuation)
    table = string.maketrans("","")
    def split_sentences(self,x):
        y=x.split('|||')
        return y
    def eng_tokenize(self,x):
        y=x.translate(self.table, string.punctuation)
        z=y.strip()
        newstring = re.sub(' +', ' ',z)
        return newstring.split(' ')
    def fren_tokenize(self,x):
        y=x.translate(self.table, string.punctuation)
        z=y.strip()
        newstring = re.sub(' +', ' ',z)
        return newstring.split(' ')

    
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

    return t,source_words,target_words

def initialize(source_words,target_words, count):

    for (sword,tword) in count.keys():
        count[(sword,tword)]=0.0
    return count
            
def model1(source,target,t,source_words,target_words,count):
    total={}
    corpus_length=len(source)
    length=len(target_words)
    for k in range(corpus_length):
        source_sentence=source[k]
        target_sentence=target[k]
        for sword in source_sentence:
            #bug :fparamdenom=float(sum(t.get((sword,tword),float(1.0/corpus_length)) for tword in target_sentence))
            fparamdenom=float(sum(t.get((sword,tword),float(1.0/length)) for tword in target_sentence))
            for tword in target_sentence:
                #delta=float(t.get((sword,tword),float(1.0/corpus_length)))/fparamdenom
                delta=float(t.get((sword,tword),float(1.0/length)))/fparamdenom
                count[(sword,tword)] = count.get((sword,tword),0) + delta
                total[sword] = total.get(sword,0) + delta
        if k%1000==0:
           print k/1000,"% done"
           sys.stdout.flush()
    for (sword,tword) in count.keys():
        t[(sword,tword)]=float(count[(sword,tword)]/total[sword])
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
    
    f=open('output.test5.txt','w+')
    for k in range(corpus_length):
        print_string=''
        #for i in range(1,len(source[k])):
        for i in range(1,len(target[k])):
            tword=target[k][i]
            (prob,sword,jans)=max((t[(source[k][j],tword)],source[k][j],j) for j in range(len(source[k])))
            print tword,sword,prob
            if jans > 1:
               print_string+=str(jans-1)+"-"+str(i)+' '
        print " ".join(source[k])
        print " ".join(target[k])
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
             es=p.eng_tokenize(source_sent)
             es.insert(0,'NULL')
             source.append(es)
             target.append(p.fren_tokenize(target_sent))
    g.close()
    it=1
    count = {}
    total = {}
    t,source_words,target_words=initialize_translation(source,target)
    print "init complete"
    print "source length = ", len(source_words)
    print "target length = ", len(target_words) 
    while it < 6:
        print 'iteration num',it
        sys.stdout.flush()
        count=initialize(source_words,target_words,count)
        print 'starting estimation'
        t=model1(source,target,t,source_words,target_words,count)
        it+=1
        sys.stdout.flush()
    alignment_model1(source,target,t)

