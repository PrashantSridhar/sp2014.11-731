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

        for t in range(target):
            psi[t]={}
            sum_psi=0.0
            for i,si in enumerate(source):
                for j,sj in enumerate(source):
                    psi[t][(i,j)]=fwd[i][t]*align[j-i]*trans[source[j]][target[t+1]]*bkw[j][t+1]
                    sum_psi+=psi[t][(i,j)]
            for i,si in enumerate(source):
                for j,sj in enumerate(source):
                    psi[t][(i,j)]=psi[t][(i,j)]/sum_psi
                    corpus_psi[t][(i,j)]+=psi[t][(i,j)]
                    gamma[t][i]+=psi[t][(i,j)]
                corpus_gamma[t][i]+=gamma[t][i]

    ##UPDATING##
    for k in range(len(source_corpus)):
    for i,si in enumerate(source):
        for j,sj in enumerate(source):
            for t in range(target):
                num+=psi[t][(i,j)]
        for t,st in enumerate(target):
            den+=gamma[t][i]
            t[si][st]=gamma[t][i]
        for j,sj in enumerate(source):
            align[j-i]=num/den

            
            

