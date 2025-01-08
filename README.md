# Urdu News Article Classification using Machine Learning

This repository contains the code and dataset for a comparative study on classifying Urdu news articles into five distinct categories: Entertainment, World, Business, Sports, and Science & Technology. The project explores the efficacy of various machine learning models, focusing on performance in a low-resource language setting.

## Technical Overview

### Dataset
- A custom dataset of 2,501 Urdu news articles was curated from prominent Pakistani news websites using a web scraping pipeline.
- The dataset underwent extensive preprocessing to handle linguistic nuances, including diacritic removal, stopword filtering (using a Kaggle dataset of 517 frequent words), and text normalization via the UrduHack library.
- Two preprocessed versions of the data were prepared to accommodate the differing input requirements of our machine learning models.

### Models
- The study implements and evaluates the performance of several machine learning models:
    -   Neural Networks (implemented in PyTorch, optimized with Adam)
    -   Logistic Regression (using Softmax regression and L2 regularization)
    -   Multinomial Naïve Bayes (using log probabilities with Laplace smoothing)
    -   Random Forest 
    -   Support Vector Machines
- Models were implemented using both the scikit-learn library and manual implementations for fine-grained control.
- Training involved techniques such as mini-batch gradient descent, dropout regularization, and careful hyperparameter tuning to optimize performance and prevent overfitting.
- Evaluation metrics: accuracy, precision, recall and F1-score.

### Key Findings
-  Multinomial Naive Bayes achieved the highest accuracy at 98.00%, showcasing its suitability for the classification task.
- Logistic Regression and Neural Networks also achieved strong results, with comparable performance in terms of all the metrics considered in the study.
-  The study highlights the potential of machine learning techniques for low resource language processing.
- The limitations of our study and potential areas for improvement are also described in detail.
