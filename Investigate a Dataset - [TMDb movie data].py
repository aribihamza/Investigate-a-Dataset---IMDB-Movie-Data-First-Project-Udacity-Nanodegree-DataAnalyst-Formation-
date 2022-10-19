#!/usr/bin/env python
# coding: utf-8

# 
# 
# # Project: Investigate a Dataset - [TMDb movie data]
# 
# ## Table of Contents
# <ul>
# <li><a href="#intro">Introduction</a></li>
# <li><a href="#wrangling">Data Wrangling</a></li>
# <li><a href="#eda">Exploratory Data Analysis</a></li>
# <li><a href="#conclusions">Conclusions</a></li>
# </ul>

# <a id='intro'></a>
# ## Introduction
# 
# ### Dataset Description 
# 
# This data set contains information about 10,000 movies collected from The Movie Database (TMDb), including user ratings and revenue.
# 
# We try to clean and manipulate Certain columns when we need, like ‘cast’ and ‘genres’ that contain multiple values separated by pipe (|) characters.
# The final two columns ending with “_adj” show the budget and revenue of the associated movie in terms of 2010 dollars, accounting for inflation over time.
# 
# 
# ### Question(s) for Analysis
# We will respond and try to found answers for this 2 questions : Which genres are most popular from year to year? What kinds of properties are associated with movies that have high revenue?

# In[2]:


# Use this cell to set up import statements for all of the packages that you
#   plan to use.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# Remember to include a 'magic word' so that your visualizations are plotted
#   inline with the notebook. See this page for more:
#   http://ipython.readthedocs.io/en/stable/interactive/magics.html


# In[ ]:


# Upgrade pandas to use dataframe.explode() function. 
get_ipython().system('pip install --upgrade pandas==0.25.0')


# <a id='wrangling'></a>
# ## Data Wrangling
# 
# 
# ### General Properties
# 

# In[3]:


# Load your data and print out a few lines. Perform operations to inspect data
#   types and look for instances of missing or possibly errant data.
df=pd.read_csv('tmdb-movies.csv')
df.head()


# In[3]:


df.info()


# In[4]:


df.nunique()


# In[5]:


df.info()


# In[6]:


df.dtypes


# 
# ### Data Cleaning
# 
#  

# We remove Columns 'id' , 'imdb_id', 'homepage' beacause it's not necessary for our analysis

# In[20]:


# After discussing the structure of the data and any problems that need to be
#   cleaned, perform those cleaning steps in the second part of this section.
#drop columns that not necessary for our analysis
df.drop(['id' , 'imdb_id', 'homepage'], inplace=True, axis=1)
df.head(1)


# In[8]:


#   Convert type of release_date frome object to datetime
df['release_date']= pd.to_datetime(df['release_date'])
df.dtypes


# In[9]:


# view missing value count for each feature
df.isnull().sum()


# <a id='eda'></a>
# ## Exploratory Data Analysis
# 
# We must know the more popular genres over the years because this is very important in charting the future of the films that will be produced and increasing the profits
# 
# ### Research Question 1 (Which genres are most popular from year to year?)

#  To Answer the question we need just this 3 columns 'genres','popularity' and 'release_year'.

# In[10]:


# Use this, and more code cells, to explore your data. Don't forget to add
#   Markdown cells to document your observations and findings.
dfg = df[['genres','popularity','release_year']]
dfg.head()


# We have for genres multiple values separated by '|' and for that we need to explode them to multiple rows by using function "explode"

# In[ ]:


dfg["genres"] = dfg["genres"].str.split("|")
dfg = dfg.explode("genres")


# In[12]:


dfg.head()


# Remove Rows that contains null value for column "genres"

# In[8]:


dfg.dropna(subset=['genres'],inplace=True)


# Make sure that we don't have null values for "genres"

# In[9]:


print(dfg['genres'].unique())


# In[17]:


dfge_genre_popularity=dfg.groupby(['genres','release_year']).mean()
dfge_genre_popularity.head()


# we move the index names to columns by using function "reset_index"

# In[18]:


dfge_genre_popularity = dfge_genre_popularity.reset_index()  
dfge_genre_popularity.head()


# We create a function to draw graph whatever the kind and the size of graph and year value.

# In[37]:


def graphpopularity(f,annee,genre,a,b):
    fannee=f[f['release_year']==annee]
    fannee.plot(kind=genre,x = 'genres', xlabel='Genre of movie',ylabel='Popularity',y ='popularity', title='Popularity of any movie genre',figsize=(a,b))


# # We use Graph Kind Bar because we have a categorical variable.

# In[20]:


graphpopularity(dfge_genre_popularity,2015,'bar',10,8)


# The most popular genres on 2015 are : Adventure, Western

# The least popular genres on 2015 are : Documentary, TV Movie

# In[21]:


graphpopularity(dfge_genre_popularity,2004,'bar',10,8)


# The most popular genres on 2004 are : Fantasy, Science Fiction , War

# The least popular genres on 2004 are : Documentary, TV Movie, Foreign

# In[80]:


graphpopularity(dfge_genre_popularity,2010,'bar',10,8)


# The most popular genres on 2010 are : Adventure, Mystery, Fantasy

# The least popular genres on 2010 are : Documentary, TV Movie, Foreign

# ### Research Question 2  (What kinds of properties are associated with movies that have high revenues?)

# To study the characteristics of movies that have a high revenue to apply the same things and more in upcoming movies to raise the profit to the max .

# In[23]:


# Continue to explore the data to address your additional research
#   questions. Add more headers as needed if you have more questions to
#   investigate.
df['revenue'].describe()


# We use function describe to see some features of a movie that have high revenue

# We see clearly that 75% who gain high revenue is having high popularity  and also high budget

# In[35]:


high_revenue= df.query('revenue >=1390753000')
high_revenue.describe()


# We take just 80 movies who have high revenue to apply some analysis on them

# In[66]:


dfs=df[df['revenue']>390753000].iloc[1:80]
dfs.head()


# => We draw scatter graph with parametrs budget and revenue to see the impact of budget on revenue.

# In[72]:


dfs.plot(kind = 'scatter', x = 'budget', y ='revenue',title="The relation between budget and revenue")


# in this chart we see that the revenue gets high as the budget is high also

# => We draw scatter graph with parametrs popularity and revenue to see the impact of popularity on revenue.

# In[82]:


dfs.plot(kind = 'scatter', x = 'popularity', y ='revenue',title="The relation between budget and revenue")


# The popularity have a big impact on revenue as we see on graph the more popular the movie, the more revenue it will make.

# => We draw scatter graph with parametrs vote average and revenue to see the impact of vote average on revenue.

# In[83]:


dfs.plot(kind = 'scatter', x = 'vote_average', y ='revenue',title="The relation between budget and revenue")


# We see clearly that the vote average has a little impact on revenue.

# <a id='conclusions'></a>
# ## Conclusions
# Results : Our data suggest that
# 
# 1. The most popular genres of Movies changes from year to year, but over the years there are categories that are always very popular, such as Action, Crime, War.
# 
# 2. The least popular genres of Movies over years are : Tv Movies, Documentary.
# 3. The Features of movies who have hight revenue :
#         - High Budget
#         - High Popularity

# Limitaions : There are a couple of limitions on our data :
#   1. Most of our variables are categorical such as Genres and Cast and Production Companies, which does not allow for a high level of statistical method that can be used to provide correlations etc
#   2. The statistics used here are descriptive statistics, not inferential, meaning that we did not create any hypotheses or controlled experiments or inferences with our data.
#   3. We do not have a lot of details for certain factors to draw conclusions.

# In[ ]:




