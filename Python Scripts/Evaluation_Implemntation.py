#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 11 23:34:19 2018

@author: jasonwu
"""


import math
import copy as cp
from matplotlib import pyplot as plt 
import pandas as pd
from collections import defaultdict
import numpy as np




'''

Reccomendation Quality evaluation implementation

including: 
    
   get_top_n: that take prediction from algo.test(testset) as parameter 
   and return  a dictionary with uid as key and list of top n tuples (iid,rui,est) as values for each uid
   
   
   ndcg: that take the dict returned from get_top_n as a parameter, 
   and return two values :a dictionary of the ndcg for each user & the average ndcg.
   
   coverage: matric for evaluating how well a sytem at covering all item or user
   
   Ave_list_Pop: metric for evaluting diverisity
   
   evel_rec_plot: get value of all metric for evaluating reccomendation perforomance in df and display in a plot
   
   get_name : get name of anime in the recommended list
   
   impossible_checker: check if there is any cases tht a system is not able to make any recommendation
   
   ci_rmse: get 95 ci for test rmse use bootstraping resampleing technique.
   
*detail is uder doc-string of each function   
'''

#function to get top k recommendation
def get_top_n(predictions, n=10, threshold= 5 ,verbose=False):
    
    '''Return the top-N recommendation for each user from a set of predictions.

    Args:
        predictions(list of Prediction objects): The list of predictions, as
            returned by the test method of an algorithm.
        
        n(int): The number of recommendation to output for each user. Default
            is 10.
            
        threshold(number): minimun value of predicted rating to be considered on the list; default is 5
            
        verbose: true then print info & list of recommendation; default is False

    Returns:
        
        A dict where keys are user (raw) ids and values are lists of tuples:
        [(raw item id,tru, rating, rating estimation), ...] of size n.
    '''

    # First map the predictions to each user.
    top_n = defaultdict(list)
    for uid, iid, true_r, est, _ in predictions:
        
        if  est > threshold: # only in the considered recommendation list if est > given value
            
            top_n[uid].append((iid,true_r, est))

    # Then sort the predictions for each user and retrieve the k highest ones.
    for uid, user_ratings in top_n.items():
        user_ratings.sort(key=lambda x: x[2], reverse=True)
        top_n[uid] = user_ratings[:n]
        
    

    
    #get list of user that has no recommendation to 
    no_rec =[]
    for uid, _, _, _, _ in predictions:
        
        if uid not in top_n:
            
            no_rec.append(uid)
            
           
        
    #print info & the recommended list if True
    if verbose:
        
        if  len(no_rec) != 0:
            
            print('*find recommendation for {} users & Unable to find recommendation for {} users*\n '.format(len(top_n),len(no_rec)))

            print('== Top {} Recommendation for {} useers == \n'.format(n,len(top_n)))
                
        else:
            print('*find recommendation for all {} users*\n '.format(len(top_n)))
            print('== Top {} Recommendation for all {} useers == \n'.format(n,len(top_n)))
        
        for uid, user_ratings in top_n.items():
            print(uid,': ' ,[iid for (iid, _,_) in user_ratings])

    return top_n


#function that convert itemid in the recommend list to anime name
def get_name(rec):
    
    for k,v in rec.items():
        
        print('## Recommendation for User {} ##\n\n'.format(k),[Anime[Anime['anime_id']==int(i)]['name'].values[0] for i,_,_ in v],'\n\n','='*115,'\n')




#function to calculate ndcg on the top n recomendation for each user in test set
def ndcg(top_n_rec,threshold=5,verbose=True):
    
    '''return Ndcg_dic & Ave_Ndcg.
    
    parameters:
    
        top_n_rec: a dict object returned from get_top_n function; 
        key - raw uid,values- list of estimation-sorted (descending) tuples(raw item id,true rating, rating estimation) of size n.        
        
        threshold: minimun value of Observed rating to be considered relevent; default is 5
       
        verbose: true then print average ndcg; default is true
      
    
    return:
    
        Ndcg_dic: dictionary of ndcg for each user; (key : user raw id. value: ndcg)
        Ave_Ndcg: Mean of NDCG
        

    
    '''
    
    
    
    ## calculate dcg for each user ##
    dcg_dic={} #default dcg dic
    
    for k,l in top_n_rec.items():
        dcg =0
        for i,(item,t_r,p_r) in enumerate(l):
        
            dcg += (1/math.log(i+2,2)) if t_r > threshold  else 0 # relevent= 1, irrelevent =0
    
    
        dcg = dcg / (i+1)
        dcg_dic[k] = dcg
        
    
    
    ## calculate idcg for each user ##
    
    # sort predcition descendingly by true rating for each user
    
    rec_idcg=cp.deepcopy(top_n_rec) # make sure the original top_n_rec dict is unchanged
    
    for uid, user_ratings in rec_idcg.items():
        
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        
    #calculate idcg
    
    idcg_dic={} #default idcg dic
    
    for k,l in rec_idcg.items():
        idcg =0
        for i,(item,t_r,p_r) in enumerate(l):
        
            idcg += (1/math.log(i+2,2)) if t_r > threshold  else 0 # relevent= 1, unrelevent =0
    
    
        idcg = idcg / (i+1)
        idcg_dic[k] = idcg
        
    
    
    
    ## NDCG_dic & Ave_Ndcg ##
    ndcg_dic={k: dcg_dic[k]/idcg_dic[k] if idcg_dic[k]!=0 else 0 for k in idcg_dic}
    Ave_Ndcg = sum(ndcg_dic.values())/len(ndcg_dic)
    
    
    if verbose:
        print('Average NDCG:  {0:1.4f}'.format(Ave_Ndcg))
    
    
    
    return Ave_Ndcg,ndcg_dic





#function to compute catelog coverage & user coverage
def coverage(rec,data,verbose=True):
    
    '''return catelog coverage & user coverage
    
    parameters:
    
        rec: a dict object returned from get_top_n function; 
        key - raw uid,values- list of estimation-sorted (descending) tuples(raw item id,true rating, rating estimation) of size n.        
        
        data: surprise trainset
        
        verbose: print info; default is True
        
        
    return:
    
        cat_coverage: item recommended /total item
        user_coverage: number of user the system make recommendation to  /total user
   
    '''
    
    
    # Compute the total number of recommended items.
    all_recommended_items = set(iid for (_, user_ratings) in rec.items() for (iid, _,_) in user_ratings)
    
    cat_coverage = len(all_recommended_items) / data.n_items
    user_coverage =  len(rec)/ data.n_users
    
    
    if verbose:
        print('Catelog coverage: {} % of items are recommended'.format(round(cat_coverage*100,2)))
        print('User coverage: {} % of users are covered'.format(user_coverage*100))
        
    return  cat_coverage, user_coverage
    




# function to get Average list Popularity
def Ave_list_Pop(rec,data,verbose=False):     

    '''Return a dict (Average list Popularity for each user ) & mean of Average list Popularity

*Average list Popularity for each user = total number of rating / number of item in the list

    input:
       
        rec: dict got from
        
        data: surprise trainset
        
        varbose: print info if True; default: False
   
    output:
    
        Ave_lst_pop: a dict (Average list Popularity for each user )
        mean_alp: mean of Average list Popularity
    '''

    n_u=len(rec)

    #default averager list pop dict
    Ave_lst_pop={}

    for uid,lst in rec.items():
        
    
        #number of item for the uid
        Iu=len(lst)
    
        #default total number of rating
        total=0
        
        for iid,_,_ in lst:
            
            #add number of rating for the iid to total
            total+=len(data.ir[data.to_inner_iid(iid)])
        
        #get averager list pop dict for each user
        Ave_lst_pop[uid]= total/Iu
        

    mean_alp=sum(Ave_lst_pop.values())/n_u
    
    if verbose:
        
        print('Mean of Average list Popularity: ',  round(mean_alp,4))
    
    
    return Ave_lst_pop,mean_alp 






#function to plot & evaluate Quality of Recommendation at K
#using evaluation metrics (NDCG, Coverage & Average list Popularity)

def evel_rec_plot(prediction,rank,data,algoname):
    '''return plots & df of NDCG, Coverage & Average list Popularity at differnt k.
    
    input:
    
        prediction: surprise prediction object; 
        
        rank: list of rank to investigated
        
        data: dataset used for get average list popularity & coverage; surprise trainset object
        
        algoname: str, algorithmn name; for plot figure title
        
           
    
    output:
        
        df: dataframe of result
        figs: plots
    
    
    '''
    
    ##get statistic summary @ each rank##
    
    ave_ndcg=[] # default ave ndcg list
    mean_alp=[] # default mean of Average list Popularity
    u_cov=[] # user coverage list
    cat_cov=[] # catlog coverage list

    for k in rank:
    
        rec=get_top_n(prediction,k,5,False)# top k get rec
    
        #ndcg
        ave_ndcg.append(ndcg(rec,5,False)[0]) # append ave ndcg @k to ave_ndcg list
        
        #alp
        mean_alp.append(Ave_list_Pop(rec,data)[1]) # append mean of Average list Popularity @k to mean_alp list
        
        #catlog coverage & user coverage
        cov=coverage(rec,data,False)
        
        cat_cov.append(cov[0])
        u_cov.append(cov[1])
        
        
        #get df
        evl_df=pd.DataFrame.from_dict({'ndcg':ave_ndcg,'alp':mean_alp,'cat_cov': cat_cov,'u_cov':u_cov})
        
        
        
    ##plots##
    fig, axes = plt.subplots(2,2,figsize=(20,15))
    fig.suptitle(algoname,size=20,weight='bold')
    
    for i, ax in enumerate(fig.axes):
        
        ax.yaxis.grid(True)
        ax.set_xlabel('Top K Recommendation',size=15,weight='bold')
        ax.set_xticks(rank)
        ax.xaxis.set_tick_params(labelsize=15)
        ax.yaxis.set_tick_params(labelsize=15)
    
    
    ## plot ndcg
    axes[0,0].plot(rank ,ave_ndcg,'ro--')
    axes[0,0].set_title('Average nDCG',size=15,weight='bold')
    
    y_max=max(ave_ndcg)
    x_max=rank[ave_ndcg.index(y_max)]
    axes[0,0].vlines(x_max,0,y_max,linestyles='dashed')
    
    
    ## plot average list popularity
    axes[0,1].plot(rank ,mean_alp,'ro--')
    axes[0,1].set_title('Mean of average list popularity',size=15,weight='bold')
    
    y_min=min(mean_alp)
    x_min=rank[mean_alp.index(y_min)]
    axes[0,1].vlines(x_min,0,y_min,linestyles='dashed')
    
    
    ## plot User coverage
    axes[1,0].plot(rank ,u_cov,'ro--')
    axes[1,0].set_title('User coverage',size=15,weight='bold')
    
    y_max=max(u_cov)
    x_max=rank[u_cov.index(y_max)]
    axes[1,0].vlines(x_max,0,y_max,linestyles='dashed')
    
    
    ## plot Item coverage 
    axes[1,1].plot(rank ,cat_cov,'ro--')
    axes[1,1].set_title('Item coverage ',size=15,weight='bold')
    
    y_max=max(cat_cov)
    x_max=rank[cat_cov.index(y_max)]
    axes[1,1].vlines(x_max,0,y_max,linestyles='dashed')
    
    plt.close(fig)
    
    
    return evl_df,fig 





#function to check if there are impossible prediction item
def impossible_checker(prediction):
    
    im=[]
    for uid,iid,_,_,d in prediction:
        
        
        if d['was_impossible'] == True:
            
            im.append((uid,iid))
            
    print('Number of Obeservation the algoritmn unable to make predciton to: ',len(im))
    
    return im



#function to get 95ci of rmse
def ci_rmse(data, size=1):
    """get 95 ci of rmse"""

    # Initialize array of replicates: bs_replicates
    bs_replicates = np.empty(size)

    # Generate replicates
    for i in range(size):
        
        #resameple
        sm=np.random.choice(data, size=len(data))
        
        #get rmse array 
        bs_replicates[i] = np.sqrt((sm**2).sum()/len(sm))
        
    #get 95_ci
    ci_95=np.percentile(bs_replicates,(2.5,97.5))

    return ci_95

