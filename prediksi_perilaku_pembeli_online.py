# -*- coding: utf-8 -*-
"""Prediksi perilaku pembeli online.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1p56QHWboG5YlI1ZBFA1CByC_-FHdtUJ9

import library
"""

# Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report
from sklearn.model_selection import KFold
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix, classification_report
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import KFold
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier

"""## VISUALISASI DATA"""

# Importing the dataset
dataset = pd.read_csv('/content/online_shoppers_intention.csv')
dataset.head(5)

# Visualizing the data before preprocessing
sns.pairplot(dataset, hue='Revenue')
plt.title('Pairplot before Preprocessing')
plt.show()

# Display the dataset
print(dataset)

# Data types
print(dataset.dtypes)

# Statistical description
print(dataset.describe())

print("Informasi Variabel ")
# Detailed information about the DataFrame
dataset.info()

"""## PRE-PROCESING DATA

prepocesing melipupi beberapa tahap:
*   pengecekan missing value atau nilai null
*   One-Hot encoding atau pelabelan
*   penghapusan outlier pada fitur yang terdekteksi memiliki nilai outlier, oulier sndri artinya nilai yang berbeda secara signifikan dari sebagian besar data dalam dataset

checking mising values
"""

# Checking for missing values
print("Checking for missing values:")
print(dataset.isnull().sum())

"""one hot encoding"""

# Encoding categorical data
from sklearn.preprocessing import LabelEncoder
labelencoder = LabelEncoder()
dataset['Month'] = labelencoder.fit_transform(dataset['Month'])
dataset['VisitorType'] = labelencoder.fit_transform(dataset['VisitorType'])
dataset['Weekend'] = labelencoder.fit_transform(dataset['Weekend'])
dataset['Revenue'] = labelencoder.fit_transform(dataset['Revenue'])

"""visualisasi outlier"""

# Visualizing outliers using boxplot
fig, axes = plt.subplots(nrows=5, ncols=4, figsize=(20, 20))
fig.subplots_adjust(hspace=0.5)
for i, ax in enumerate(axes.flatten()):
    if i < len(dataset.columns) - 1:
        sns.boxplot(y=dataset.iloc[:, i], ax=ax)
        ax.set_title(dataset.columns[i])

plt.show()

"""persiapan untuk penanganan oulier"""

# Separating the features and the target variable
X = dataset.iloc[:, :-1].values
y = dataset.iloc[:, -1].values

"""penghapusan oulier"""

# Removing outliers using Z-score method
from scipy import stats
z_scores = np.abs(stats.zscore(X))
filtered_entries = (z_scores < 3).all(axis=1)
X = X[filtered_entries]
y = y[filtered_entries]

"""menampilkan data setelah penghapusan oulier"""

# Visualizing the data after removing outliers
sns.pairplot(pd.DataFrame(X, columns=dataset.columns[:-1]), diag_kind='kde')
plt.title('Pairplot after Removing Outliers')
plt.show()

"""## SPLITING DATA"""

# Feature Scaling
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X = sc.fit_transform(X)

# Visualizing the data after scaling
sns.pairplot(pd.DataFrame(X, columns=dataset.columns[:-1]), diag_kind='kde')
plt.title('Pairplot after Scaling')
plt.show()

# Defining the KFold Cross-Validator with 5 folds
kf = KFold(n_splits=5, shuffle=True, random_state=42)

# Lists to hold performance metrics for each fold
fold_accuracies_svm = []
fold_precisions_svm = []
fold_recalls_svm = []

fold_accuracies_rf = []
fold_precisions_rf = []
fold_recalls_rf = []

"""## MODELING"""

# K-Fold Cross-Validation
for fold_idx, (train_index, test_index) in enumerate(kf.split(X)):
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = y[train_index], y[test_index]

    # Training SVM
    svm_model = SVC(kernel='linear')
    svm_model.fit(X_train, y_train)
    y_pred_svm = svm_model.predict(X_test)

    # Calculating metrics for SVM
    accuracy_svm = accuracy_score(y_test, y_pred_svm)
    precision_svm = precision_score(y_test, y_pred_svm)
    recall_svm = recall_score(y_test, y_pred_svm)

    fold_accuracies_svm.append(accuracy_svm)
    fold_precisions_svm.append(precision_svm)
    fold_recalls_svm.append(recall_svm)

    # Training Random Forest
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
    y_pred_rf = rf_model.predict(X_test)

    # Calculating metrics for Random Forest
    accuracy_rf = accuracy_score(y_test, y_pred_rf)
    precision_rf = precision_score(y_test, y_pred_rf)
    recall_rf = recall_score(y_test, y_pred_rf)

    fold_accuracies_rf.append(accuracy_rf)
    fold_precisions_rf.append(precision_rf)
    fold_recalls_rf.append(recall_rf)

    # Printing metrics for each fold
    print(f"Fold {fold_idx + 1}:")
    print(f"SVM Accuracy: {accuracy_svm:.2f}, Precision: {precision_svm:.2f}, Recall: {recall_svm:.2f}")
    print(f"RF Accuracy: {accuracy_rf:.2f}, Precision: {precision_rf:.2f}, Recall: {recall_rf:.2f}")
    print()

# Calculating mean and std deviation of metrics across folds
mean_accuracy_svm = np.mean(fold_accuracies_svm)
std_accuracy_svm = np.std(fold_accuracies_svm)
mean_precision_svm = np.mean(fold_precisions_svm)
std_precision_svm = np.std(fold_precisions_svm)
mean_recall_svm = np.mean(fold_recalls_svm)
std_recall_svm = np.std(fold_recalls_svm)

mean_accuracy_rf = np.mean(fold_accuracies_rf)
std_accuracy_rf = np.std(fold_accuracies_rf)
mean_precision_rf = np.mean(fold_precisions_rf)
std_precision_rf = np.std(fold_precisions_rf)
mean_recall_rf = np.mean(fold_recalls_rf)
std_recall_rf = np.std(fold_recalls_rf)

# Printing mean metrics across folds
print("Mean Metrics Across Folds:")
print(f'SVM Mean Accuracy: {mean_accuracy_svm:.2f} ± {std_accuracy_svm:.2f}')
print(f'SVM Mean Precision: {mean_precision_svm:.2f} ± {std_precision_svm:.2f}')
print(f'SVM Mean Recall: {mean_recall_svm:.2f} ± {std_recall_svm:.2f}')
print()
print(f'Random Forest Mean Accuracy: {mean_accuracy_rf:.2f} ± {std_accuracy_rf:.2f}')
print(f'Random Forest Mean Precision: {mean_precision_rf:.2f} ± {std_precision_rf:.2f}')
print(f'Random Forest Mean Recall: {mean_recall_rf:.2f} ± {std_recall_rf:.2f}')

# Function to evaluate the model using K-Fold Cross-Validation
def evaluate_model(model, X, y):
    skf = StratifiedKFold(n_splits=5, random_state=0, shuffle=True)
    accuracies = []
    conf_matrices = []
    reports = []
    for train_index, test_index in skf.split(X, y):
        X_train_fold, X_test_fold = X[train_index], X[test_index]
        y_train_fold, y_test_fold = y[train_index], y[test_index]
        print(f"Training data in fold: {len(train_index)}, Testing data in fold: {len(test_index)}")
        model.fit(X_train_fold, y_train_fold)
        y_pred_fold = model.predict(X_test_fold)
        accuracies.append(accuracy_score(y_test_fold, y_pred_fold))
        conf_matrices.append(confusion_matrix(y_test_fold, y_pred_fold))
        reports.append(classification_report(y_test_fold, y_pred_fold, output_dict=True))
    return np.array(accuracies), conf_matrices, reports

# Fitting SVM to the dataset
from sklearn.svm import SVC
classifier_svm = SVC(kernel='linear', random_state=0)

"""## EVALUASI MODEL"""

# Evaluating SVM with K-Fold Cross-Validation
accuracies_svm, conf_matrices_svm, reports_svm = evaluate_model(classifier_svm, X, y)
print("SVM Cross-Validation Accuracies:", accuracies_svm)
print("SVM Mean Accuracy:", accuracies_svm.mean())
print("SVM Standard Deviation:", accuracies_svm.std())

# Fitting Random Forest Classification to the dataset
from sklearn.ensemble import RandomForestClassifier
classifier_rf = RandomForestClassifier(n_estimators=100, criterion='entropy', random_state=0)

# Evaluating Random Forest with K-Fold Cross-Validation
accuracies_rf, conf_matrices_rf, reports_rf = evaluate_model(classifier_rf, X, y)
print("Random Forest Cross-Validation Accuracies:", accuracies_rf)
print("Random Forest Mean Accuracy:", accuracies_rf.mean())
print("Random Forest Standard Deviation:", accuracies_rf.std())

# Printing the results
print("SVM Confusion Matrices:")
for i, cm in enumerate(conf_matrices_svm, 1):
    print(f"Fold {i}:\n", cm)

print("SVM Classification Reports:")
for i, report in enumerate(reports_svm, 1):
    print(f"Fold {i}:\n", report)

print("Random Forest Confusion Matrices:")
for i, cm in enumerate(conf_matrices_rf, 1):
    print(f"Fold {i}:\n", cm)

print("Random Forest Classification Reports:")
for i, report in enumerate(reports_rf, 1):
    print(f"Fold {i}:\n", report)

# Visualizing the importance of features for Random Forest
importances = classifier_rf.feature_importances_
indices = np.argsort(importances)[::-1]

print("Feature ranking:")
for f in range(X.shape[1]):
    print("%d. feature %s (%f)" % (f + 1, dataset.columns[indices[f]], importances[indices[f]]))

# Plotting the feature importances
plt.figure()
plt.title("Feature importances")
plt.bar(range(X.shape[1]), importances[indices], color="r", align="center")
plt.xticks(range(X.shape[1]), dataset.columns[indices], rotation=90)
plt.xlim([-1, X.shape[1]])
plt.show()

"""## EVALUSI MENGGUNAKAN HEATMAP

"""

# Plotting heatmap for SVM confusion matrices
for i, cm in enumerate(conf_matrices_svm, 1):
    plt.figure(figsize=(10, 7))
    sns.heatmap(cm, annot=True, fmt="d", cmap="YlGnBu", cbar=False)
    plt.title(f'SVM Confusion Matrix - Fold {i}')
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.show()

# Plotting heatmap for Random Forest confusion matrices
for i, cm in enumerate(conf_matrices_rf, 1):
    plt.figure(figsize=(10, 7))
    sns.heatmap(cm, annot=True, fmt="d", cmap="YlGnBu", cbar=False)
    plt.title(f'Random Forest Confusion Matrix - Fold {i}')
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.show()

"""## EVALUASI MENGGUNAKAN BAR CHARTS"""

# Plotting accuracy comparison
models = ['SVM', 'Random Forest']
accuracies = [accuracies_svm.mean(), accuracies_rf.mean()]
std_devs = [accuracies_svm.std(), accuracies_rf.std()]

x = np.arange(len(models))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, accuracies, width, label='Mean Accuracy', color='b')
rects2 = ax.bar(x + width/2, std_devs, width, label='Standard Deviation', color='orange')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_xlabel('Model')
ax.set_ylabel('Score')
ax.set_title('Accuracy and Standard Deviation by Model')
ax.set_xticks(x)
ax.set_xticklabels(models)
ax.legend()

# Add labels on the bars with smaller font size and different padding
ax.bar_label(rects1, padding=4, fontsize=10, fmt='%.2f')
ax.bar_label(rects2, padding=4, fontsize=10, fmt='%.2f')

fig.tight_layout()

plt.show()