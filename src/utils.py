import os
import re
import numpy as np 
import pandas as pd
import warnings
import nltk

from nltk.corpus import stopwords
from sklearn.preprocessing import LabelEncoder
from sklearn.utils import resample

warnings.filterwarnings('ignore')
#nltk.download('stopwords')

def make_dir(dir_name: str):
    """Creates a new directory in the current working directory."""
    save_dir = os.path.join('./', dir_name)
    if not os.path.exists(save_dir):
            os.mkdir(save_dir)
    else:
        print(f'{save_dir}: Already exists!') 
    return save_dir

# Text Preprocessing functions
REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;:$!]')
BAD_SYMBOLS_RE = re.compile('[^0-9a-z #+_?&]')
STOPWORDS = set(stopwords.words('english'))
single_chars = re.compile(r'\s+[a-zA-Z]\s+')

def clean_text(text: str)-> str:
    """
    Preprocesses text and returns a cleaned
    piece of text with unwanted characters removed
    
    Args:
       text: a string
    Returns: 
        Preprocessed text
    """
    text = str(text).lower() # lowercase text
    text = REPLACE_BY_SPACE_RE.sub(' ', text) # replace REPLACE_BY_SPACE_RE symbols by space in text
    text = BAD_SYMBOLS_RE.sub('', text) # delete symbols which are in BAD_SYMBOLS_RE from text
    text = ' '.join(word for word in text.split() if word not in STOPWORDS) # delete stopwords from text
    text = single_chars.sub('', text) #remove single-characters
    return text

def remove_URL(text: str)-> str:
    """
    Removes URL patterns from text.
    Args:
        `text`: A string, word/sentence
    Returns:
        Text without url patterns.
    """
    url = re.compile('https?://\S+|www\.\S+')
    text = url.sub('',text)
    return text

def remove_emoji(text: str)-> str:
    """
    Remove emojis from text.
    Args:
        `text`: a string
    Returns:
        clean text with no emojis.
    """
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               "]+", flags=re.UNICODE)
    text = emoji_pattern.sub(r'', text)
    return text

def remove_html(text)-> str:
    """
    Removes html tags from text.
    Args:
        `text`: A string, word/sentence
    Returns:
        Text without html tags.
    """
    html = re.compile('<.*?>')
    text = html.sub('',text)
    return text

def load_data(data_path):
    """Load dataset from specified path."""
    train_df = pd.read_csv(data_path)
    encoder = LabelEncoder()
    train_df['label'] = encoder.fit_transform(train_df['label'])

    df_majority = train_df[train_df.label==0]
    df_minority = train_df[train_df.label==1]

    # Upsample minority class
    #df_minority_upsampled = resample(df_minority, 
     #                               replace=True,
      #                              n_samples=1200,
       #                             random_state=42)

    # Combine majority class with upsampled minority class
    #train_df = pd.concat([df_majority, df_minority_upsampled])
    train_df['Tweet'] = train_df['Tweet'].astype(str)

    train_df['Tweet'] = train_df['Tweet'].apply(remove_URL)
    train_df['Tweet'] = train_df['Tweet'].apply(remove_emoji)
    train_df['Tweet'] = train_df['Tweet'].apply(remove_html)
    train_df['Tweet'] = train_df['Tweet'].apply(clean_text)
    X = train_df['Tweet'].values
    y = train_df['label'].values
    return encoder, X, y

def count_vectorize(data: str) -> [int]:
    """
    Create word vectors/tokens for input data
    Args:
        `data`: text to be vectorized
    """
    from sklearn.feature_extraction.text import CountVectorizer

    vectorizer = CountVectorizer(min_df=3, analyzer='word',
                                 ngram_range=(1, 3))
    vectors = vectorizer.fit_transform(data)

    return vectors, vectorizer

