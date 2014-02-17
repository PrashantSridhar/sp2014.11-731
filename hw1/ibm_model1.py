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
    sent_total = {}
    t={}
    for k in range(corpus_length):
        for i in range(len(source[k])):
            source_words.add(source[k][i])
        for j in range(len(target[k])):
            target_words.add(target[k][j])

    return t,source_words,target_words,sent_total

def initialize(source_words,target_words, count):

    for sword in count.keys():
        count_dict = count[sword]
        for tword in count_dict.keys():
            count_dict[tword]=0.0
    return count
            
def model1(source,target,t,source_words,target_words,count,sent_total):
    corpus_length=len(source)
    length = len(target_words)
    for k in range(corpus_length):

        for tword in target[k]:
            sent_total[tword]=0.0
            for sword in source[k]:
                tdict = t.get(sword,{})
                score = tdict.get(tword, float(1.0/length))
                sent_total[tword] += score
        for sword in source[k]:
            if not(sword in count.keys()):
                    count[sword] = {}
            count_dict = count[sword]
            tdict = t.get(sword,{})
            for tword in target[k]:
                score = tdict.get(tword, float(1.0/length))          
                count_dict[tword] = count_dict.get(tword,0) + float(score/sent_total[tword])
        if k%1000 == 0:
            print "sentence done ", k
            sys.stdout.flush()
    print "phase 1 done"
    sys.stdout.flush()
    for sword in count.keys():
        norm = sum(count[sword].values())
        sword_dict = count[sword]
        if not(sword in t.keys()):
            t[sword] = {}
        trans_dict = t[sword]
        for tword in sword_dict.keys():

            trans_dict[tword] = float(sword_dict[tword]/norm)

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
    
    f=open('output.txt','w+')
    for k in range(corpus_length):
        print_string=''
        for i in range(1,len(source[k])):
            if i%1000==0:
                print "sentence printed",i

            sword=source[k][i]
            (prob,tword,jans)=max((t[sword][target[k][j]],target[k][j],j) for j in range(len(target[k])))
            #print tword,sword,prob
            print_string+=str(i-1)+"-"+str(jans)+' '
        #print " ".join(source[k])
        #print " ".join(target[k])
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
    t,source_words,target_words,sent_total=initialize_translation(source,target)
    print "init complete"
    print "source length = ", len(source_words)
    print "target length = ", len(target_words) 
    while it < 6:
        print 'iteration num',it
        sys.stdout.flush()
        count=initialize(source_words,target_words,count)
        print 'starting estimation'
        t=model1(source,target,t,source_words,target_words,count,sent_total)
        it+=1
        sys.stdout.flush()
    alignment_model1(source,target,t)

