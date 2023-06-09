README

6105 Assignment 3

1. Project Main Goal
   The objective of this project is to explore how will unsupervised learners perform in clustering labelled dataset. 
   I studied how KMeans and GMM cluster datasets before and after datasets going through dimension reduction. 
   I explored how dimension reduction will affect the performance of both supervised and unsupervised learners.


2. Dataset
   Breast Cancer Wisconsin (Diagnostic) Data Set can be downloade at https://www.kaggle.com/datasets/uciml/breast-cancer-wisconsin-data .
   The dataset contains 569 cases, each has 10 features, including radius, texture, perimeter, ect.. 
   The mean, standard error and worst of each features were computed, therefore, resulting 30 attributes in total.
   At this time, I use only the mean value of each case in the model. Therefore, before the trainning in each model, 10 standard error columns and 10 worst columns were dropped.
   
   Iris flower dataset can be downloaded at https://www.kaggle.com/datasets/arshid/iris-flower-dataset/code. 
   The dataset contains a set of 150 records under 5 attributes - Petal Length, Petal Width, Sepal Length, Sepal width and Class (Species). 
   There are 3 species to be categorized (setosa, versicolor, and virginica), each has 50 entries.

3. Model
   2 unsupervised learners and 3 dimension reduction algorithms are applied in this project. 
   They are KMeans, GMM, PCA, ICA, t-SNE.

4. Setup
   The code is written in python, you'd better run it on jupyter notebook.
   When running the code, download the dataset and be aware of the dataset file retrieving path. You may need to change it depending on the location you store the file. 
   Before running the Neural Network file, you need to install keras as well as tensorflow by inputting "pip install keras" and "pip install tensorflow" on your terminal shell.

5. Conclusion
   (1) KMeans and GMM can produce reasonable and consistent clusters for the datasets which has already visible clusters.
   
   (2) It happens that KMeans and GMM cluster dataset not in accordance with the real labels. 
   At this situation, if following the real labels and let KMeans and GMM unnaturally clustering the data, overfitting appears. 
   Although it is closer to the real situation and it has higher accuracy score, it does present a worse cluster configuration in the KMeans and GMM perspective.

   (3) When doing PCA and deciding the optimal number of principal components, take 80% as the benchmark of the explained variance ratio. 
   Lower than 80% may project inadequate information into the new space, while higher than 80% may bring up overfitting.

   (4) The effect of PCA in the new space depends on the clustering configuration. 
   PCA helps improve performance in natural KMeans/GMM clusters. 
   If applying KMeans/GMM according to the original labels, PCA do further deteriorate the performance.

   (5) The number of independent components generated by the ICA should be equal to the number of observed mixtures.

   (6) t-SNE (t-Distributed Stochastic Neighbor Embedding) is more suitable for datasets with hundreds of features.

   (7) The impact of dimension reduction algorithms on supervised learning varies, it really depends on the dataset, the dimension reduction algorithms and the supervised learning algorithms.