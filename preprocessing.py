import string
import nltk
from nltk.util import ngrams
nltk.download('stopwords')
nltk.download('wordnet')
wn = nltk.WordNetLemmatizer()
stopwords = nltk.corpus.stopwords.words('english')

def preprocess(question):
    question= "".join([char for char in question if char not in string.punctuation+string.digits])
    question=" ".join(word for word in question.split() if word not in stopwords)
    question= " ".join([wn.lemmatize(word.lower()) for word in question.split()])
    question=" ".join(bigram(question.split())+[question])
    return question

def bigram(lis):
    l=[]
    for word in ngrams(lis,2):
        l.append('_'.join(word))
    return l

if __name__=="__main__":
  preprocessing('question')
