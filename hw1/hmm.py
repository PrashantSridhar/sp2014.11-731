def fwd_bkw(x, states, init, a, e, end_st):
    L = len(x)
    fwd = []
    f_prev = {}
    # forward part of the algorithm
    for i, x_i in enumerate(x):
        f_curr = {}
        for j,st in enumerate(states):
            if i == 0:
                # base case for the forward part
                prev_f_sum = a_0[st]
            else:
                prev_f_sum = sum(f_prev[k]*a[k-i] for k,st0 in enumerate(states))
            f_curr[st] = e[st][x_i] * prev_f_sum
        fwd.append(f_curr)
        f_prev = f_curr
    p_fwd = sum(f_curr[k]*a[k][end_st] for k in states)
    bkw = []
    b_prev = {}
    # backward part of the algorithm
    for i, x_i_plus in enumerate(reversed(x[1:]+(None,))):
        b_curr = {}
        for j,st in enumerate(states):
            if i == 0:
                # base case for backward part
                b_curr[st] = a[st][end_st]
            else:
                b_curr[st] = sum(a[j-l]*e[l][x_i_plus]*b_prev[l] for l in states)
        bkw.insert(0,b_curr)
        b_prev = b_curr
    p_bkw = sum(a_0[l] * e[l][x[0]] * b_curr[l] for l in states)
    # merging the two parts
    posterior = {}
    for st in states:
        posterior[st] = [fwd[i][st]*bkw[i][st]/p_fwd for i in range(L)]
    assert p_fwd == p_bkw
    return fwd, bkw, posterior

def baum_welch(source_corpus,target_corpus):
    corpus_psi={}
    corpus_gamma={}
    for k in range(len(source_corpus)):
        source_sentence=source_corpus[k]
        target_sentence=target_corpus[k]
        fwd,bkw,posterior=fwd_bkw(source_sentence, states,start_probability,alignment,translation, end_st)
        #can be simplified, just computer corpus_psi[i,j]. gamma_psi[i]=sum corpus_psi[,j]:
        for t,tt in enumerate(target):
            psi={}
            #psi[t]={}
            sum_psi=0.0
            for i,si in enumerate(source):
                fparamdenom=float(sum(t.get((si,tt),float(1.0/corpus_length)) for tword in target_sentence))
                for j,sj in enumerate(source):
                    psi[(i,j)]=fwd[i][t]*align[j-i]*trans[source[j]][target[t+1]]*bkw[j][t+1]
                    sum_psi+=psi[(i,j)]
            for i,si in enumerate(source):
                for j,sj in enumerate(source):
                    psi[(i,j)]=psi[(i,j)]/sum_psi
                    corpus_psi[(i,j)]+=psi[(i,j)]

    ##UPDATING##
    for key in corpus_psi.keys():
        if key[0] not in gamma:
            gamma[key[0]]=0.0
        gamma[key[0]]+=corpus_psi[key] 
    for key in corpus_psi.keys():
        jump=key[1]-key[0]
        '''
        if jump not in align_num:
            align_num[jump]=0.0
        if jump not in align_den:
            align_den[jump]=0.0
        '''
        align[jump]+=corpus_psi[key]/gamma[key[0]] #adding each aij seperately, v.s.adding all numerators and denominators.
    normalize_jump=sum(align)
    align=[float(align[jump])/float(normalize_jump) for jump in align]
           

            
            

