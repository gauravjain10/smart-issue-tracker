import pickle
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from scipy import sparse,io
import numpy as np
#from preprocessing import preprocess

def function(question):
    vectorizer = pickle.load(open("vectorizer2.pk", "rb"))
    doc_mat= io.mmread("test2.mtx")
    q=vectorizer.transform([question])
    sim=cosine_similarity(doc_mat,q)
    index=sim.argsort(axis=0)[::-1][:3]
    sim=sim.flatten()
    sim.sort()
    sim=sim[::-1]
    Score=sim[:3]
    Score=[ '%.2f' % s for s in Score ]
    df = pd.read_csv('TCovidData.csv')
    Answers=[]
    Questions=[]
    for i in index:
        Answers.append(df['answers'].iloc[i[0]])
        Questions.append(df['questions'].iloc[i[0]])
    return Answers,Questions,Score
    
def ehealthforumQAs_function(question):
    vectorizer = pickle.load(open("ehealthforumQAs.pk", "rb"))
    doc_mat= io.mmread("ehealthforumQAs.mtx")
    q=vectorizer.transform([question])
    sim=cosine_similarity(doc_mat,q)
    index=sim.argsort(axis=0)[::-1][:3]
    sim=sim.flatten()
    sim.sort()
    sim=sim[::-1]
    Score=sim[:3]
    Score=[ '%.2f' % s for s in Score ]
    df = pd.read_csv('ehealthforumQAs.csv')
    Answers=[]
    Questions=[]
    for i in index:
        Answers.append(df['answer'].iloc[i[0]])
        Questions.append(df['question'].iloc[i[0]])
    return Answers,Questions,Score

if __name__=="__main__":
    function('covid')
    ehealthforumQAs_function('ehealthforumQAs')
