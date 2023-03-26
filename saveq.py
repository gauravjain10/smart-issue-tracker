import pandas as pd

def save_question(question):
    df = pd.read_csv("unanswered_q.csv")
    df.loc[-1]= question
    df.to_csv("unanswered_q.csv",index=False)
    
        
