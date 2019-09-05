Machine Learning Project
(PI: Thomas Kursar & Phyllis Coley)

In this phase, we have three stages:

**1. Making predictions with only peak data**

In this stage, we only included the *peak* data as features. We trained machine learning models in the following ways:
a). training on inga (real data), testing on inga (real data)
b). training on insilico (simulation), testing on insilico (simulation)
c). training on insilico (simulation), testing on inga (real data)

For a)., we had an accuracy (1 if all 71 labels are correct, 0 otherwise) of 76%;
For b)., we had an accuracy (1 if all 71 labels are correct, 0 otherwise) of 90%;
For c)., we had an accuracy (1 if all 71 labels are correct, 0 otherwise) of 5%;

**2. Making predictions with peak and loss data**

In this stage, we included both the *peak* and *loss* data as features. We trained machine learning models on insilico (simulation) data and tested on inga data. The purpose is to see if the accuracy could be improved. Unfortunately, the accuracy was still as low as <10%. Therefore, we drew the conclusion that the computer-generated simulation data do not have the same distribution as the real data.

**3. Training with only peak data on real data**

In the last stage, we trained a machine learning model on the peak data of real data (only 842 records) and made predictions on the unknown compound (2449 records). Trained with only <1000 data points, the model reaches acceptable performance. This indicates the underlying order of the data is predictable. However, since it takes effort to make collision of compounds and gather the information of their fractions, we might not be able to have enough data. Nevertheless, the model is reusable for future prediction if following the preprocessing procedure. 

**Please Note: **
We have 7492 features for peak data. So we preprocessed the data and converted them into sparse matrices. The machine learning models were also based on sparse matrices.
