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
            
def viterbi(trans_p, start_p, emit_p, target, source):
    V = [{}]
    paths = {}
    # Initialize base cases (t == 0)
    for y in source:
        V[0][y] = start_p[y] * emit_p[y][target[0]]
        paths[y] = [y]
    # Run Viterbi for t > 0
    for t in range(1, len(target)):
        V.append({})
        newpaths = {}
        newjumps={}
        #for y in source:
        for m in range(source):
            y=source[m]
            (prob, state,l) = max((V[t-1][source[pos]] * trans_p[pos-m] * emit_p[y][target[t]], source[pos], pos) for pos in range(source))
            V[t][y] = prob
            newpaths[y] = paths[state] + [y]
            newjumps[m]= jumps[pos]+[m]

        paths=newpaths
        jumps=newjumps
    (prob, state,final) = max((V[t][source[pos]], source[pos],pos) for pos in range(source))
    return (prob, paths[state],jumps[final])

def hmm(source,target,t,source_words,target_words,count,alignment,total):
    sent_total={}
    corpus_length=len(source)
    for k in range(corpus_length):
        sent_total={}
        source_sentence=source[k]
        target_sentence=target[k]
        (prob,path,jumps)=viterbi(align,start,t,target_sentence,source_sentence)
        prev='0'
        for m in range(len(jumps)):
            a[m-prev]+=1.0
            prev=m
        total_dist=0.0
        for i in range(len(source_sentence)):
            sword=source_sentence[i]
            j=jumps[i]
            lword=target_sentence[j]
            correct_i=i-1
            fparam=t[sword]
            if (sword,tword) not in counts:
                count[(sword,tword)]=0.0
                total[sword]=0.0
            count[(sword,tword)]+=1.0
            total[sword]+=1.0
            for j in range(0,len(target_sentence))
                tword=target_sentence[j]
                delta=float(tparam[tword])/fparamdenom
                if (sword,tword) not in counts:
                    count[(sword,tword)]=0.0
                    total[sword]=0
                count[(sword,tword)]+=delta
                total[sword]+=delta
                
    for dist in a:
        total_dist+=a[dist]
    for dist in align:
        align[dist]=float(a[dist])/float(total_dist)
    for sword in source_words:
        for tword in target_words:
            t[sword][tword]=float(count[sword][tword]/total[sword])
    return t,align
         
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

