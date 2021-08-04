#***********************************************************************
# @file
#
# Assignment_3: Feature Mining and Modeling
#
# @note None
#
# @warning  None
#
#  Created: July 25, 2021
#   Author: Bogdan Constantinescu
#**********************************************************************/
#!/usr/bin/env python

import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR

# Skipping these per your own instructions:
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC, LinearSVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import Perceptron
from sklearn.linear_model import SGDClassifier
from sklearn.ensemble import GradientBoostingClassifier

pd.set_option('display.max_rows', 100)
pd.set_option('display.min_rows', 100)
pd.options.mode.chained_assignment = None

# Since you told me to skip the cleaning of the data, I will jump to 
# using your DataFrame now:
# ... 
#cleaned_training_df = pd.read_csv('Training_Data_cleaned.csv')
cleaned_training_df = pd.read_csv('Training_Data_cleaned_no_index.csv')

print('cleaned_training_df.head():')
print(cleaned_training_df.head())
print()

print('cleaned_training_df.info():')
print(cleaned_training_df.info())
print()

# Mr. B, descriptive naming in coding, indeed in the whole engineering 
# discipline is very very important, and in software engineering even more
# so. But understandably it is very difficult to do when one is more focused
# on 'making the product work'. Still, we must try, if we are to follow
# and understand our own code after many months or years have elapsed. So,
# notice the names that I have been choosing for the DataFrame variables
# for these your Python assignments? Here:
column_headings_df = pd.read_csv('Metadata.csv')

# Makes sense, right? See, for example:
#
# https://cs.fit.edu/~kgallagher/Schtick/How%20To%20Write%20Unmaintainable%20Code.html
#
# https://deviq.com/practices/naming-things
#
# https://www.slideshare.net/pirhilton/how-to-name-things-the-hardest-problem-in-programming
print('column_headings_df.head():')
print(column_headings_df.head())
print()

# And don't worry Mr. B, I know you name your variables well; I just get
# in the habit of professional coding wherein I document each line of my
# code and explain 'the reasoning behind' why I made certain "design choices" :).
# It helps me understand and grokk things quickly too when I have to come
# back to that code after many years of being away from it.
print('column_headings_df.info():')
print(column_headings_df.info())
print()

# ======================================================================
# Support Vector Regression (SVR) Using Linear And Non-Linear Kernels
# ======================================================================

X = cleaned_training_df.drop(['X1'], axis=1)
y = cleaned_training_df['X1']

#train_X, test_X, train_y, test_y = train_test_split(X, y, train_size=0.8, test_size=0.2, stratify=y)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# Fitting the regression model...
#
# As your professor said, "... When writing the code associated with each
# model, please have the first part produce and save the model, ..."
svr_radial_basis_function = SVR(kernel='rbf', C=100, gamma=0.1, epsilon=0.1)
svr_linear = SVR(kernel='linear', C=100, gamma='auto')
svr_polynomial = SVR(kernel='poly', C=100, gamma='auto', degree=3, epsilon=0.1, coef0=1)

# "... followed by a second part that loads and applies the model."
lw = 2

the_svrs = [svr_radial_basis_function, svr_linear, svr_polynomial]
the_kernel_labels = ['RBF', 'Linear', 'Polynomial']
the_model_colors = ['m', 'c', 'g']

figure_1, axes = plt.subplots(nrows=1, ncols=3, figsize=(15, 10), sharey=True)

for index, svr in enumerate(the_svrs):
    axes[index].plot(X_train, svr.fit(X_train, y_train).predict(X_train), color=the_model_colors[index], lw=lw,
                  label='{} model'.format(the_kernel_labels[index]))
    axes[index].scatter(X_train[svr.support_], y_train[svr.support_], facecolor="none",
                     edgecolor=the_model_colors[index], s=50,
                     label='{} support vectors'.format(the_kernel_labels[index]))
    axes[index].scatter(X_train[np.setdiff1d(np.arange(len(X_train)), svr.support_)],
                     y_train[np.setdiff1d(np.arange(len(X_train)), svr.support_)],
                     facecolor="none", edgecolor="k", s=50,
                     label='other training data')
    axes[index].legend(loc='upper center', bbox_to_anchor=(0.5, 1.1),
                    ncol=1, fancybox=True, shadow=True)

figure_1.text(0.5, 0.04, 'data', ha='center', va='center')
figure_1.text(0.06, 0.5, 'target', ha='center', va='center', rotation='vertical')
figure_1.suptitle("Support Vector Regression", fontsize=14)

plt.show()
