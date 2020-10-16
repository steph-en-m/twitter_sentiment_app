## Suicide Monitor

The suicide monitor app uses machine learning to predict suicide intent in tweets by various twitter users.

## Features
* The `home page` contains a visual map that will display a `tweet`, `its predicted suicide intent probability`i.e. `>0.7=Suicidal` or `< 0.6=Not Suicidal` and the `location` the tweet was sent from.

* The `search tool`:
The search tool will enable a user to search/fetch tweets from twitter using `keywords such as suicide..` that are related to suicide for the AI model to run predictions on. This is to cater for scenarios where the `Keyword/Rules database` doesn't contain that given keyword

* The `Sign-In` feature:
The signin feature is to allow for the app administrator to log into the `admin dashboard` where he/she will be able to:
   * View the `Keywords` in the database
   * Add new `Keywords` to the `Keyword database`
   * Download twitter stream data.i.e twitter data on which the model does predictions.
   * The admin dashboard also displays the predicted suicide intent on a visual map as in the home page

