README

6105 Assignment 3

1. Project Main Goal
   In this project, 5 differnent machine learning models were applied in the breast cancer (Wisconsin) dataset and iris flower dataset. 
   The accuracy of each model are compared and analysizd. Iterations are running to fine tune the parameters for each model.
   In one way, the results of different types of datasets on the same machine learning model are compared and analyzed.
   In the other way, the result for different models training on the same dataset are compared and analyzed.


2. Dataset
   Breast Cancer Wisconsin (Diagnostic) Data Set can be downloade at https://www.kaggle.com/datasets/uciml/breast-cancer-wisconsin-data .
   The dataset contains 569 cases, each has 10 features, including radius, texture, perimeter, ect.. 
   The mean, standard error and worst of each features were computed, therefore, resulting 30 attributes in total.
   At this time, I use only the mean value of each case in the model. Therefore, before the trainning in each model, 10 standard error columns and 10 worst columns were dropped.
   
   Iris flower dataset can be downloaded at https://www.kaggle.com/datasets/arshid/iris-flower-dataset/code. 
   The dataset contains a set of 150 records under 5 attributes - Petal Length, Petal Width, Sepal Length, Sepal width and Class (Species). 
   There are 3 species to be categorized (setosa, versicolor, and virginica), each has 50 entries.

3. Model
   5 models are applied in this project. They are K Nearest Neighbors(KNN), Support Vectors Machine(SVM), Decision Tree, Artificial Networks, and Gradient Boosting.

4. Setup
   The code is written in python, you'd better run it on jupyter notebook.
   When running the code, download the dataset and be aware of the dataset file retrieving path. You may need to change it depending on the location you store the file. 
   Before running the Neural Network file, you need to install keras as well as tensorflow by inputting "pip install keras" and "pip install tensorflow" on your terminal shell.

5. Conclusion
   (1))	For the breast cancer classification problem, all 5 machine learning models have great performance since their accuracy score are all above 0.9. 
   And my first lesson learned here is that a tiny difference in the accuracy score cannot be used to judge the absolute performance of models. 
   I use accuracy as an indicator to choose which model is more suitable for the problem of benign or malignant tumors. 
   But it does not mean that the highest score model will perform the best in actual situations, because, in realities, there may be larger datasets, more features, etc..
   They will affect the accuracy of the model.
   
   (2) If performances of difference models are comparable equivalent, analyzing the f1-score would help to determine the best performance model.

   (3) When training models, pay attention to outliers, models like support vector machines and gradient boosting are quite sensitive to outliers.

   (4) As presented in the KNN instance (iris dataset), small size data plays tricks in the performance. The accuracy varies drastically even when change the random state.

   (5) SVM has a stable performance not matter the size of the dataset.

   (6) When training Boosting with small size of data, overfitting can take place easily.