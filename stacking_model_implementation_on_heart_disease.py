# -*- coding: utf-8 -*-
"""Stacking model Implementation on Heart Disease

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ObAa8IcI6a2zjGPy0b8gFDuVLj5EqaKK

# Step 1: Import Necessary Libraries
"""

# Import necessary libraries
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.preprocessing import MinMaxScaler
from imblearn.over_sampling import SMOTE
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, StackingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

"""# Step 2: Read Dataset"""

# Load dataset
df = pd.read_csv('heart.csv')

# Seperate target variable and input variables
X = df.drop(columns=['target'])  # Features
y = df['target']  # Target variable

# Head of the dataset
print(df.head())

# Tail of the dataset
print(df.tail())

"""# Sanity Check of Data"""

# shape of the dataset
df.shape

# info about the dataset
df.info()

# Checking for missing values
print("Missing values count:")
print(df.isnull().sum())

"""# Exploratory Data Analysis"""

# Descriptive Statistics of numerical features
df.describe().T

# Histogram to Understand the distribution of data of numerical columns
import warnings
warnings.filterwarnings('ignore')
df.hist(figsize=(15,15))
plt.show()

# Boxplot to identify outliers
import warnings
warnings.filterwarnings('ignore')
df.boxplot(figsize=(15,15))
plt.show()

"""## Outliers Treatment"""

def wiskers(col):
    q1, q3 = np.percentile(col, [25, 75])
    iqr = q3 - q1
    lower_bound = q1 - (1.5 * iqr)
    upper_bound = q3 + (1.5 * iqr)
    return lower_bound, upper_bound

# lower and upper bound of trestbps
wiskers(df['trestbps'])

# Define features to exclude from outlier detection
exclude_features = ['fbs']

# Iterate over columns and apply outlier removal, skipping excluded features
for i in df:
    if i not in exclude_features:  # Skip 'fbs'
        lower_bound, upper_bound = wiskers(df[i])
        df = df[(df[i] >= lower_bound) & (df[i] <= upper_bound)]

for i in df:
  sns.boxplot(df[i])
  plt.show()

df.select_dtypes(include='number').columns

# Scatter plot to understand the relationship of the numerical features with target variable (num)
for i in ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach',
       'exang', 'oldpeak', 'slope', 'ca', 'thal',]:
    sns.scatterplot(x=df[i], y=df['target'])
    plt.show()

# Step 4: Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

# Step 5: Handle class imbalance using SMOTE
smote = SMOTE(random_state=42)
X_train_balanced, y_train_balanced = smote.fit_resample(X_train, y_train)

"""# Feature Scaling"""

numerical_features = ['age', 'cp', 'trestbps', 'fbs', 'chol', 'thalach', 'oldpeak', 'slope', 'ca', 'thal']
scaler = MinMaxScaler()
df[numerical_features] = scaler.fit_transform(df[numerical_features])

print(df.head())

# Correlation
corr = df.select_dtypes(include='number').corr()
corr

# Correlation
corr = df.select_dtypes(include='number').corr()
corr

plt.figure(figsize=(12, 10))  # Adjust the figure size here
sns.heatmap(corr, annot=True, cmap='coolwarm')
plt.show()

"""# Support Vector Machine

"""

from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Train the SVM model
svm_model = SVC(kernel='linear', C=1.0, random_state=42)
svm_model.fit(X_train, y_train)

# Predict on the test data
y_test_pred = svm_model.predict(X_test)

# Predict on the training data
y_train_pred = svm_model.predict(X_train)

# cross validation
cv_scores_svm = cross_val_score(svm_model, X, y, cv=5, scoring='accuracy')
print("Cross-Validation Scores (SVM):", cv_scores_svm)
print("Average Cross-Validation Score (SVM):", np.mean(cv_scores_svm))


# Evaluate the model on test data
print("\nIn-Sample Accuracy (Training Data):", accuracy_score(y_train, y_train_pred))
print("Out-Sample Accuracy (Test Data):", accuracy_score(y_test, y_test_pred))

print("\nClassification Report (Test Data):\n", classification_report(y_test, y_test_pred))

# Confusion Matrix for test data
cm_test = confusion_matrix(y_test, y_test_pred)
print("\nConfusion Matrix (Test Data):\n", cm_test)

"""# Decision Tree Classifier"""

from sklearn.tree import DecisionTreeClassifier

# Train a Decision Tree model
dt_model = DecisionTreeClassifier(criterion='entropy', random_state=42)
dt_model.fit(X_train, y_train)

# Make predictions
y_pred = dt_model.predict(X_test)


cv_scores_dt = cross_val_score(dt_model, X, y, cv=5, scoring='accuracy')
print("Cross-Validation Scores (Decision Tree):", cv_scores_dt)
print("Average Cross-Validation Score (Decision Tree):", np.mean(cv_scores_dt))

# Evaluate the model
print("\nIn-Sample Accuracy (Training Data):", accuracy_score(y_train, y_train_pred))
print("Out-Sample Accuracy (Test Data):", accuracy_score(y_test, y_test_pred))

print("\nClassification Report:\n", classification_report(y_test, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

# Decision tree Construction

from sklearn import tree
import matplotlib.pyplot as plt

# Assuming dt_model is already trained as in the previous code
plt.figure(figsize=(20,10))
tree.plot_tree(dt_model, filled=True, feature_names=X.columns, class_names=['0','1'])
plt.show()

"""# Random Forest Classifier"""

rf_model = RandomForestClassifier(n_estimators=150, max_depth=12, random_state=42, class_weight='balanced')
rf_model.fit(X_train, y_train)

y_pred = rf_model.predict(X_test)

cv_scores_rf = cross_val_score(rf_model, X, y, cv=5, scoring='accuracy')
print("Cross-Validation Scores (Random Forest):", cv_scores_rf)
print("Average Cross-Validation Score (Random Forest):", np.mean(cv_scores_rf))

print("\nIn-Sample Accuracy (Training Data):", accuracy_score(y_train, y_train_pred))
print("Out-Sample Accuracy (Test Data):", accuracy_score(y_test, y_test_pred))

print("\nClassification Report:\n", classification_report(y_test, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

"""# K Nearest Neighbor"""

knn_model = KNeighborsClassifier(n_neighbors=5)
knn_model.fit(X_train, y_train)

y_pred = knn_model.predict(X_test)

cv_scores_knn = cross_val_score(knn_model, X, y, cv=5, scoring='accuracy')
print("Cross-Validation Scores (KNN):", cv_scores_knn)
print("Average Cross-Validation Score (KNN):", np.mean(cv_scores_knn))

print("\nIn-Sample Accuracy (Training Data):", accuracy_score(y_train, y_train_pred))
print("Out-Sample Accuracy (Test Data):", accuracy_score(y_test, y_test_pred))

print("\nClassification Report:\n", classification_report(y_test, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

"""# Boosting (XGBoost)"""

xgb_model = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42)
xgb_model.fit(X_train, y_train)

y_pred = xgb_model.predict(X_test)

cv_scores_xgb = cross_val_score(xgb_model, X, y, cv=5, scoring='accuracy')
print("Cross-Validation Scores (XGBoost):", cv_scores_xgb)
print("Average Cross-Validation Score (XGBoost):", np.mean(cv_scores_xgb))

print("\nIn-Sample Accuracy (Training Data):", accuracy_score(y_train, y_train_pred))
print("Out-Sample Accuracy (Test Data):", accuracy_score(y_test, y_test_pred))

print("\nClassification Report:\n", classification_report(y_test, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

"""# Bagging Classifier"""

bg_model = RandomForestClassifier(n_estimators=100, max_depth=8, random_state=42, class_weight='balanced')
bg_model = bg_model.fit(X_train, y_train)

y_pred = bg_model.predict(X_test)

bg_cv_scores = cross_val_score(bg_model, X, y, cv=5, scoring='accuracy')
print("Cross-Validation Scores (Bagging):", bg_cv_scores)
print("Average Cross-Validation Score (Bagging):", np.mean(bg_cv_scores))

print("\nIn-Sample Accuracy (Training Data):", accuracy_score(y_train, y_train_pred))
print("Out-Sample Accuracy (Test Data):", accuracy_score(y_test, y_test_pred))

print("\nClassification Report:\n", classification_report(y_test, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

"""# Stacking ensemble machine learning Model

1.   Random Forest
2.   SVM
3.   Decision Tree
4.   Gradient Boosting
5.   Logistic Regression (Meta Learner)


"""

# Step 7: Define base models for stacking
base_models = [
    ('rf', RandomForestClassifier(n_estimators=100, max_depth=8, random_state=42, class_weight='balanced')),
    ('svm', SVC(kernel='rbf', probability=True, C=1.0, random_state=42)),
    ('dt', DecisionTreeClassifier(criterion='entropy', random_state=42)),
    ('gb', GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42)),
]

# Meta-learner (Logistic Regression)
meta_learner = LogisticRegression(max_iter=2000, random_state=42)

# Stacking classifier
stacking_model = StackingClassifier(
    estimators=base_models,
    final_estimator=meta_learner,
    cv=StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
)

# Step 8: Train the stacking model
stacking_model.fit(X_train_balanced, y_train_balanced)

# Step 9: Evaluate the model
train_predictions = stacking_model.predict(X_train_balanced)
test_predictions = stacking_model.predict(X_test)

# Training and testing accuracy
print("Training Accuracy:", accuracy_score(y_train_balanced, train_predictions))
print("Testing Accuracy:", accuracy_score(y_test, test_predictions))

# Confusion matrix and classification report
print("\nConfusion Matrix:\n", confusion_matrix(y_test, test_predictions))
print("\nClassification Report:\n", classification_report(y_test, test_predictions))

# Cross-validation for robust evaluation
cv_scores = cross_val_score(stacking_model, X, y, cv=StratifiedKFold(n_splits=5, shuffle=True, random_state=42))
print("\nCross-Validation Scores:", cv_scores)
print("Average Cross-Validation Score:", np.mean(cv_scores))

# Import necessary libraries
from scipy.stats import ttest_rel
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Cross-validation scores for models
stacking_scores = [1.0, 1.0, 1.0, 0.980, 1.0]  # Stacking model
rf_scores = [1.0, 1.0, 0.985, 1.0, 0.975]             # Random Forest
svm_scores = [0.883, 0.868, 0.844, 0.815, 0.805]      # Support Vector Machine
knn_scores = [0.766, 0.746, 0.761, 0.712, 0.751]      # K-Nearest Neighbors
gb_scores = [0.971, 0.976, 0.951, 0.961, 0.961]       # Gradient Boosting

# Perform paired t-tests
def paired_t_test_and_plot(model1_scores, model2_scores, model1_name, model2_name, results):
    # Perform paired t-test
    t_stat, p_value = ttest_rel(model1_scores, model2_scores)
    results[model2_name] = (t_stat, p_value)

    # Print results
    print(f"\nComparison: {model1_name} vs {model2_name}")
    print(f"t-statistic: {t_stat:.4f}, p-value: {p_value:.4f}")
    if p_value < 0.05:
        print(f"The difference between {model1_name} and {model2_name} is statistically significant.\n")
    else:
        print(f"No statistically significant difference between {model1_name} and {model2_name}.\n")

# Dictionary to store t-test results
t_test_results = {}

# Comparing stacking model with other models
paired_t_test_and_plot(stacking_scores, rf_scores, "Stacking", "Random Forest", t_test_results)
paired_t_test_and_plot(stacking_scores, svm_scores, "Stacking", "SVM", t_test_results)
paired_t_test_and_plot(stacking_scores, knn_scores, "Stacking", "KNN", t_test_results)
paired_t_test_and_plot(stacking_scores, gb_scores, "Stacking", "Gradient Boosting", t_test_results)

# Plotting the accuracies
# Calculate mean accuracy for each model
models = ["Stacking", "Random Forest", "SVM", "KNN", "Gradient Boosting"]
mean_accuracies = [
    np.mean(stacking_scores),
    np.mean(rf_scores),
    np.mean(svm_scores),
    np.mean(knn_scores),
    np.mean(gb_scores)
]

# Create a bar plot
plt.figure(figsize=(10, 6))
sns.barplot(x=models, y=mean_accuracies, palette="viridis")
plt.title("Mean Cross-Validation Accuracy of Models", fontsize=16)
plt.ylabel("Mean Accuracy", fontsize=12)
plt.xlabel("Models", fontsize=12)
plt.ylim(0.7, 1.0)
for i, acc in enumerate(mean_accuracies):
    plt.text(i, acc + 0.005, f"{acc:.3f}", ha="center", fontsize=10)
plt.show()

# Print t-test results summary
print("\nSummary of Paired t-Tests:")
for model, (t_stat, p_value) in t_test_results.items():
    print(f"Stacking vs {model}: t-statistic={t_stat:.4f}, p-value={p_value:.4f}")

# Bar graph for in sample and out sample accuracy
import matplotlib.pyplot as plt
import numpy as np


models = ['SVM', 'Decision Tree', 'Random Forest', 'KNN', 'XGBoost', 'Bagging', 'Stacking']
in_sample_accuracy = [0.85, 0.92, 0.95, 0.88, 0.93, 0.94, 1.0]
out_sample_accuracy = [0.82, 0.89, 0.91, 0.85, 0.90, 0.92, 1.0]

x = np.arange(len(models))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots(figsize=(12, 6))
rects1 = ax.bar(x - width/2, in_sample_accuracy, width, label='In-Sample Accuracy')
rects2 = ax.bar(x + width/2, out_sample_accuracy, width, label='Out-Sample Accuracy')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Accuracy')
ax.set_title('In-Sample vs. Out-Sample Accuracy for Different Models')
ax.set_xticks(x)
ax.set_xticklabels(models)
ax.legend()


def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')


autolabel(rects1)
autolabel(rects2)

fig.tight_layout()
plt.show()

import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc

# Function to plot ROC Curve
def plot_roc_curve(y_test, y_probs, model_name):
    fpr, tpr, _ = roc_curve(y_test, y_probs)
    roc_auc = auc(fpr, tpr)
    plt.plot(fpr, tpr, label=f"{model_name} (AUC = {roc_auc:.2f})")
    return roc_auc

# Initialize ROC plot
plt.figure(figsize=(12, 8))

# Random Forest
rf_probs = rf_model.predict_proba(X_test)[:, 1]
plot_roc_curve(y_test, rf_probs, "Random Forest")

# KNN
knn_probs = knn_model.predict_proba(X_test)[:, 1]
plot_roc_curve(y_test, knn_probs, "KNN")

# Gradient Boosting
xgb_probs = xgb_model.predict_proba(X_test)[:, 1]
plot_roc_curve(y_test, xgb_probs, "Gradient Boosting")

# Bagging Classifier
bg_probs = bg_model.predict_proba(X_test)[:, 1]
plot_roc_curve(y_test, bg_probs, "Bagging Classifier")

# Stacking Model
stacking_probs = stacking_model.predict_proba(X_test)[:, 1]
plot_roc_curve(y_test, stacking_probs, "Stacking Model")

# SVM
svm_probs = svm_model.decision_function(X_test)
svm_probs = (svm_probs - svm_probs.min()) / (svm_probs.max() - svm_probs.min())  # Normalize decision scores
plot_roc_curve(y_test, svm_probs, "SVM")

# Decision Tree
dt_probs = dt_model.predict_proba(X_test)[:, 1]
plot_roc_curve(y_test, dt_probs, "Decision Tree")

# Plot details
plt.plot([0, 1], [0, 1], color="navy", linestyle="--", label="Random Guess")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve Comparison")
plt.legend(loc="lower right")
plt.show()