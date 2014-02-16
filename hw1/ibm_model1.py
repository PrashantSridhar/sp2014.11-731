import random
class Preprocessing():
    def split_sentences(self,x):
        y=x.split('|||')
        return y
    def eng_tokenize(self,x):
        return x.split(' ')
    def fren_tokenize(self,x):
        return x.split(' ')

    
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
    length=len(target_words)
    for sword in source_words:
        t[sword]={}
        for tword in target_words:
            t[sword][tword]=float(1.0/length)
    return t,source_words,target_words

def initialize(source_words,target_words):
    count={}
    total={}
    for sword in source_words:
        count[sword]={}
        total[sword]=0.0
        for tword in target_words:
            count[sword][tword]=0.0
    return count,total
            
def model1(source,target,t,source_words,target_words,count,total):
    sent_total={}
    corpus_length=len(source)
    for k in range(corpus_length):
        sent_total={}
        for tword in target[k]:
            sent_total[tword]=0.0
            for sword in source[k]:
                sent_total[tword]+=t[sword][tword]
        for tword in target[k]:
            for sword in source[k]:
                count[sword][tword]+=float(t[sword][tword]/sent_total[tword])
                total[sword]+=float(t[sword][tword]/sent_total[tword])
    for sword in source_words:
        for tword in target_words:
            t[sword][tword]=float(count[sword][tword]/total[sword])
    return t
         
def alignment_model1(source,target,t):
    corpus_length=len(source)
    for k in range(corpus_length):
        print_string=''
        for i in range(len(source[k])):
            sword=source[k][i]
            (prob,tword,jans)=max((t[sword][target[k][j]],target[k][j],j) for j in range(len(target[k])))
            #print tword,sword,prob
            print_string+=str(i-1)+"-"+str(jans)+' '
        print " ".join(source[k])
        print " ".join(target[k])
        print print_string


                    


        
        
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
    t,source_words,target_words=initialize_translation(source,target)
    while it < 6:
        print 'iteration num',it
        count,total=initialize(source_words,target_words)
        t=model1(source,target,t,source_words,target_words,count,total)
        it+=1
    alignment_model1(source,target,t)

