# Anime Recommender Systems | Python, Surprise, Jupyter

The goal of this project was to develop a collaborative-based anime recommender system capable of generating a personalized list of unique and relevent anime recommendations based on database information comprising total user history and rating ID user feedback.The source of the data is from Kaggle.com [(Anime dataset from Kaggle)](https://www.kaggle.com/CooperUnion/anime-recommendations-database). There are two associated datasets, rating dataset and anime dataset. The rating dataset contains 7,813,737 Ratings (Rating scale: 1- 10) from 73,516 users on 12,294 anime with a density of 0.92%; the anime dataset consists of information about each anime with 7 columns (anime_id, name, genre, type, episodes, rating, and members). Using python with SUPRISE package and leveraging custom built data cleaning and model evaluation programs, I investigated different kinds of collaborative filtering (CF) algorithms including item-based KNNWithMeans, SVD, Co-clustering, and SVDpp. 

![model comparison & evalaution](/graph/recQualityPlot3.png)
<p align="center">
<img width="700" height="200" src="/graph/Screen%20Shot%202018-07-20%20at%201.56.12%20PM.png">   
</p>


* SVD performed best on recommending ranked list of relevent anime for users based on nDCG (ranking accuracy metric) without sacrificing too much speed
* KNNWithMeans performed best on finding Niche listings


### Scripts
- Jupyter NoteBook
  - [Exploratory Analysis](/Jupyter%20notebook/Jason_Anime_recommender_system-EDA_of_original_anime_datasets.ipynb)
  - [Data Preproccesing](/Jupyter%20notebook/Jason_Anime_recommender_system_Data_Preproccessing.ipynb)
  - [Model Training & Validation](/Jupyter%20notebook/Jason_Anime_recommender_system_Model%20training.ipynb)
  - [Model Evaluation & Selection](/Jupyter%20notebook/Jason_Anime_recommender_system_Model%20Evaluation_and_Comparsion.ipynb)
- Python
  - [Reusable Data Preproccesing Program](/Python%20Scripts/data_cleaning.py)
  - [Implemented Evaluation Metrics & Tools](/Python%20Scripts/Evaluation_Implemntation.py)
