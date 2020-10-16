Suicide detection workflow:
* Steps:
    * data acquisition
    * text preprocessing and vectorization
    * model training
    * model evaluation

* Data aquisition: Labeled suicide detection datasets were sourced from a public github repository, a past text classification competition and the test data is scraped in real-time from twitter.

* The suicide detection problem is framed as a binary classification task with two target variable classes i.e. `Suicidal` and `Not Suicidal` thus implying that a tweet can be related/belong to either of these two classes.

* Since tweets and text data in general can be messy for machine learning models to learn from, the tweets are preprocessed and noise such as `emojis, punctuations, hashtags, and other non-alphabetical characters` is removed.

* Next the cleaned/preprocessed text is vectorized i.e. text is turned into numbers since computer algorithms only 'understand' numerical data using the `bag of words` approach for the xgboost model which is the highest scoring model on this task.
    * The LSTM model uses a `word embeddings` approach instead of simply vectorizing the text and feeding it into the model.

* Finally two different suicide detection models `xgboost model` on `bag of words` and the `BiLSTM model` with `word embeddings` are trained, both with the `stratified Kfold cross validation` strategy since the dataset is imbalanced and evaluated against the `f1_score` metric where `0 < f1_score < 1`(a higher f1 score is better).

The `xgboost model` achieved a significantly higher score than the `BiLSTM` model.
This large gap in performance can be attributed to the small dataset size on which deep learning models tend to perform poorly.