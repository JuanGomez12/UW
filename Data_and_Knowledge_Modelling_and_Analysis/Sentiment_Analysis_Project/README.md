# Sentiment Analysis of a Medication Review Website using NLTK and GloVe
The complete code of the project can be found in the five accompanying Jupyter notebooks. The order is representative with the order it is explained in the report.

- 1_ECE657A_Project_G12_ML.ipynb: Jupyter notebook with the VADER and the different machine learning classification algorithms. For it to work correctly needs to have the option of downloading NLTK files, like the stop words and the VADER sentiment classifier.

- 2_ECE657A_Project_G12_MLP.ipynb: Jupyter notebook with the Multi-Layer Perceptron Neural Network algorithm. It also needs access to the internet in order to download NLTK's stop words.

- 3_ECE 657A_Project_G12_LSTM.ipynb: Jupyter notebook with the one layer LSTM Neural Network algorithm. It also needs access to the internet in order to download NLTK's stop words.

- 4_ECE 657A_Project_G12_LSTM_Paper.ipynb: Jupyter notebook with the two layer LSTM Neural Network algorithm based on the paper by Sboev et al[1]. It also needs access to the internet in order to download NLTK's stop words.

- 5_ECE 657A_Project_G12_CNN_Paper.ipynb: Jupyter notebook with the Convolutional Neural Network (CNN) algorithm based on the paper by Zhang and Wallace[2]. It also needs access to the internet in order to download NLTK's stop words.

The dataset, formed by the files named drugsComTest_raw and drugsComTrain_raw, can be donwloaded as a zip file named drugsCom_raw.zip from https://archive.ics.uci.edu/ml/datasets/Drug+Review+Dataset+%28Drugs.com%29

The GloVe embedding text file should also be downloaded, and can be obtained from the webpage of the researchers at https://nlp.stanford.edu/projects/glove/. The specific embedding file used was the glove.6B.100d.txt found inside the downloadable glove.6B.zip file.

The dataset files and the GloVe file should be added to a folder named "data", in the same directory as the current location of the jupyter notebook.


References:
[1] Sboev, Aleksandr, et al. "Deep Learning Network Models to Categorize Texts According to Author's Gender and to Identify Text Sentiment." 2016 International Conference on Computational Science and Computational Intelligence (CSCI). IEEE, 2016.

[2] Zhang, Ye, and Byron Wallace. "A sensitivity analysis of (and practitioners' guide to) convolutional neural networks for sentence classification." arXiv preprint arXiv:1510.03820 (2015).
