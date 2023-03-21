# Triage

This repo contains the code used to build a cohort and predictive model for triaging patients admitted to the hospital from the Emergency Department. 
The R codebase of this repo is not up to date with the R codebase that was used to produce the final work in the published paper. Due to an unresolved campus compute server crash, we are still not able to recover/push the latest version of the R code base. The R codebase currently in this repo is only a draft, prelim version of the final R codebase, lacking 8 months of work.
Code contributors: Minh Nguyen, Conor K Corbin, Tiffany Eulalio, Nicolai P Ostberg, and Gautam Machiraju https://github.com/gmachiraju

## SQL
SQL was used to pull data for 
1. Building the cohort
2. Collecting features
3. Feature Counts

## Notebooks
Jupyter notebooks were used for
1. Cohort Building
2. Data Cleaning
3. Featurization
4. Generating Labels
5. Model building and training
6. Processing Results

## More details:
The order of the R ipynb notebooks for data cleaning:

### 1. cohort_demographicR1: 
* read original init cohort, filter form 2015 - 2019
* add ESI, filter code status, and demographic variables
* update the cohort, with labels 
* impute HW with indicators
* combine with first vital sign values (-GCS) to impute ESI, with indicator

### 2. features_vitals_cleanR2:
* clean vital sign, use the updated cohort
* extract first sets of vital signs, including GCS
* to remove GCS later when combined with demographic to impute ESI
* GCS was not used

--> final output: vitals_clean, in long format

### 3. features_labs_cleanR3:
* clean labs, joined with cohort

--> final output: labs_clean, in long format

### 4. features_joinR4:
* demographics, height and weight, ESI, other patient specific variables
* vitals and labs: change recorded_time and result_time to time
* row binds all 3 features, one hot coding as appropriate
* get simple set of data

## Complex features:
* get all counts from SQL
* quantile bin labs and vitals
* get complex set of data

## Modeling:
* logistic regression with ESI only as the baseline
* ML with same set of algorithms for both simple and complex datasets: elastic net, random forest, gbm, and feed forward neural net


