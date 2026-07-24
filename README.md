# MoCA Score Prediction Using Machine Learning

> **Project Status:** 🚧 Work in Progress

This repository is under active development. The preprocessing pipeline, model evaluation, and external prediction workflow are still being refined.

## 📌 Overview

This project aims to predict the Montreal Cognitive Assessment (MoCA) score using machine learning models trained on virtual reality (VR)-based medical assessment data collected from real patients.

Several preprocessing strategies, feature selection methods, and regression algorithms are evaluated using Leave-One-Out Cross-Validation (LOOCV) due to the limited number of labeled samples.

The project is divided into **4 main parts**, all contributing to a unified pipeline:

1. Cleaning Basic CSV 
2. Extracting Features of Each patient
3. Data preprocessing
4. Model Desgining (combine of three different solution)
    
    4.1 solution one : Testing 7 Regression models with 8 Feautre selection methods with LeaveOneOut.
    
    4.2 solution two : Testing 7 Regression models with data augmentation methods with LeaveOneOut.
    
    4.3 solution three : Combining the best configuration of solution one with best of the solution two.

🎯 **Goal:**

* Predict the MoCA score

---

## 📂 Dataset

Data Source: Nine CSV files containing the behavioral data of each patient collected during the VR assessment.

Patients with Available MoCA Scores: 13

---

## Part 1: Cleaning Basic CSV


---

## Part 2: Extracting Features of Each patient

---

## Part 3: Data preprocessing

---

## Part 4: Model Desgining

In this part, using the properly prepared data from Part 3 with shape (13,113), we tested different regression models with various feature selection and data augmentation methods to find the best configuration — one that minimizes both overfitting and test MSE.

### Part 4: Solution one :
In this part, we tested 8 regression models and 7 feature selection methods (used to reduce the number of columns) with **5-fold cross-validation**.

**Models:** Linear Regression, Ridge, Random Forest, XGBRegressor, SVR, Lasso, Linear SVR, MLPRegressor

**Feature selection methods:** All columns, SelectKBest (50 features), SelectKBest (20 features), SelectKBest (10 features), RFECV, Variance Threshold, PCA (5 components)

However, since our dataset only included 13 patients, we replaced 5-fold cross-validation with **Leave-One-Out Cross-Validation (LOOCV)**. We also removed Linear SVR and MLPRegressor, as both require large amounts of data and failed to converge on this dataset. Similarly, we dropped SelectKBest (10 features), RFECV, and Variance Threshold, since they were computationally expensive and did not perform well with only 13 patients.

**Final models tested (LOOCV, 13 patients):** Linear Regression, Ridge, Random Forest, XGBRegressor, SVR, Lasso

**Final feature selection methods tested:** All columns, SelectKBest (50 features), SelectKBest (20 features), PCA (5 components).

- See the [MSE Results of methods and models](results_and_figures/2.MSE_results_13patients.md) for more details.

- See the [Overfitting Results of methods and models](results_and_figures/3.overfitting_score_13patients) for more details.

### Part 4: Solution two :
Following the results from Solution 1, we also tested data augmentation methods to see whether they would improve results using the same models. Again, given the very small amount of data, we selected only augmentation methods suitable for small datasets.

**Feautre selection methods chosen from solution one :** SelectKBest (20 features), PCA (5 components)

**Methods :** Gaussian noise injection, SMOTER, Copula-based or parametric simulation
---

### Models Used:
### Feature Selection Methods:

## 📊 Results (solution one):

Feel free to check the Results_figures folder to get more details about all models result
Best results of LOO + 13 real patients

| Model  | Feature selection | Test MSE |   Gap | Overfitting |
| ------ | ----------------: | -------: | ----: | ----------- |
| SVR    | All 120 Features  | 11.01    | 3.81  | Low         |
| SVR    | Select50Best      | 11.27    | 4.39  | Low         |
| SVR    | Select20Best      | 10.84    | 3.99  | Low         |
| SVR    | PCA               | 11.94    | 4.25  | Low         |

![Pipeline](results_and_figures/True_vs_predicted_MoCA_scores_13patients.png)

-------------------------------------------------------------------------------

![Pipeline](results_and_figures/scatter_plot_of_13_patients_LOO.png)


### 📊 Results (solution two):

### 📊 Results (solution three):



**For detailed results and visualizations of all evaluated models, please refer to the Results_figures folder.**
---

## 🚀 How to Run the Project

```bash
# Clone the repository
git clone git@github.com:sana-mirahsani/detection_AD_with_VR_data.git

# Install dependencies
pip install -r requirements.txt

# Run notebooks / scripts
```

---

## 🛠️ Technologies Used

* 🐍 Python
* 📊 Pandas, NumPy
* 🤖 Scikit-learn
* 📈 Matplotlib

---

## 📌 Future Improvements

* Increase the number of patients with real MoCA score

---

## 👩‍💻 Authors

* Sana Mirahsani

🔗 LinkedIn: [https://www.linkedin.com/in/sana-mirahsani](https://www.linkedin.com/in/sana-mirahsani)
💻 GitHub: [https://github.com/sana-mirahsani](https://github.com/sana-mirahsani)

---

## ⭐ Support

If you find this project useful:

* ⭐ Star the repo
* 🍴 Fork it

---