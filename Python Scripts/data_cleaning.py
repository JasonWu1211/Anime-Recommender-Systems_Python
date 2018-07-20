#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  2 14:57:52 2018

@author: jasonwu
"""

#function for subsetting the anime : certain type & genre(if not None)

def Anime_subset(anime_df,rating_df,anime_type,anime_genre=None):
    '''
    input:
        anime_df: anime feature dataframe
        rating_df: anime rating dataframe         
        anime_type: anime type
        anime_genre: anime genre; default is None
    
    output:
    
        subset_anime_rating: pandas dataframe; certain kind (genre & type) of anime    
    
    
    '''

    #get anime id of certain type
    atype = anime_df.type == anime_type
    atype_id= anime_df[atype]['anime_id'].values
    
    #limit user rating data to this type of anime
    type_anime_rating= rating_df[rating_df['anime_id'].isin(atype_id)]
        
    if anime_genre == None:
        
        subset_anime_rating = type_anime_rating
        
    else:
        
        ## get certain genre  
        genre_row= anime_df.genre.str.get_dummies(sep=', ')[anime_genre]==1
        
        #get anime id for cerntain gene
        genre_aid=anime_df[genre_row]['anime_id'].values
        
        #limit user data to centain type  & genre
        type_genre_anime= type_anime_rating[type_anime_rating['anime_id'].isin(genre_aid)]
        
        subset_anime_rating = type_genre_anime
        
    return subset_anime_rating    



# Confirgure one_Scale_rater_eliminator function designed for Removing people who only give same rating to everything
def one_Scale_rater_eliminator(df,user):    
    '''
    input:
        df: pandas dataframe used
    
    output:
        no_one_Scale_rater: pandas dataframe without people who only give same rating to everything    
    '''    
    no_one_Scale_rater =df.groupby(user).filter(lambda x: (max(x['rating'])-min(x['rating']))!=0)
    
    return no_one_Scale_rater



#confirgure core_operator function designed for removing obervation(user/item) that has less than 10 rating
def core_operator(df,n,user,item=None):
    '''
    input:
        n: minimun number of item & user rating;
        df: pandas dataframe used
        user: user column
        item: item column; Default is None (only remove user who rating less than n items);
    output:
        core: n core dataframe
    
    '''
    
    if item == None:
        
        core_df = df.groupby(user).filter(lambda x: len(x)>=n)
        
    else:
        
        core_df = df.groupby(user).filter(lambda x: len(x)>=n).groupby(item).filter(lambda x: len(x)>= n)
    
    return core_df




#confirgure data_cleaner to check & clean data
def data_cleaner(df,n=10,user='user_id',item='anime_id'):
    '''
    input:
        
        df: investigated pandas data frame
        n: int, number of core; default is 10
        user: user column name; default 'user_id'
        item: item column name; default 'anime_id'; if item = None- only perform n core on user
    
    print:
        
        
         pointer of the indication and excution of cleaning functions that need to be performed 

        
    output:
        
        cleaned_data:
        
        data that meet following conditions
        
        *without one-scale rater &
        *all the obeservation(user/item) have more tan n(default is 10) rating
        
    '''
    ## check if cleaned_data is clean
    cleaned_data=df
    i=0
    
    ##conditions
    #one scale rater? True : there are one-scale raters
    #more than 10 item & user ? True : no item & user has less than 10 ratinngs and otherwise
    One_scale =(1 in cleaned_data.groupby(user).apply(lambda x: x['rating'].nunique()).values)
    if item == None:
        
        morethan10 = min(cleaned_data.groupby(user)['rating'].count())>=10
    else:
        morethan10 = min(cleaned_data.groupby(user)['rating'].count())>=10 & min(cleaned_data.groupby(item)['rating'].count())>=10
    
    #check condition iteratively
    
    while (One_scale,morethan10) != (0, 1) :
        
        i+=1
        print('## Iteration {} ##'.format(i))
        
        One_scale =(1 in cleaned_data.groupby(user).apply(lambda x: x['rating'].nunique()).values)
        
        if not One_scale:
            
            
            
            print('No one scale Rater!')
        
        else:
            
            print('There are one-scale raters!')
            
            cleaned_data=one_Scale_rater_eliminator(cleaned_data,user)
            
            print('one_Scale_rater_eliminator excuted')
        
        print('\n')

        
        if item == None:
        
            morethan10 = min(cleaned_data.groupby(user)['rating'].count())>=10
        else:
            morethan10 = min(cleaned_data.groupby(user)['rating'].count())>=10 & min(cleaned_data.groupby(item)['rating'].count())>=10
        
        if morethan10:
                        
            print( 'No item & user has less than 10 ratinngs!')
            
            cleaned_data=cleaned_data
            
        else:
            
            print('There are some user or item (if not None) has less than 10 ratings!')
            
            cleaned_data=core_operator(cleaned_data,n,user,item)
            
            print('core_operator excuted!')
            
        print('\n')
        
        print('='*70)
    

    
    
    print('Data is cleaned!')
    
    return cleaned_data

       