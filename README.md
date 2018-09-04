**Substructure Prediction on Inga Compounds with Machine Learning Techniques**

(PI: Thomas Kursar & Phyllis Coley)

**ML_Inga_Chem1 - Stage 1**

Making predictions of 44 substructures on Inga data with peak and loss features grouped according to their apperance and distance.

**ML_Inga_Chem2 - Stage 2**

Trying different discretization strategies on peak and loss values of In Silico data and Inga data in order to reduce dimensionality and increase accuracy.

**ML_Inga_Chem3 - Stage 3**

Taking the output of Kernel Density Estimate as peak and loss features and generating sparse matrix for machine learning prediction. Trying different algorithms on In Silico data, Inga data, or training with In Silico data and predicting with Inga data. Algorithms work well on the former two but not the last one. The conclusion is In Silico data has a different distribution from Inga data which cannot help us on prediction Inga compounds. In the final result, we trained the model with known Inga compounds and made predictions on unknown Inga compounds.