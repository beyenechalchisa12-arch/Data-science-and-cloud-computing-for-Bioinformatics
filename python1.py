
import pandas as pd

print("Pandas version:", pd.__version__)


df = pd.read_csv("messy_data_module_2.csv")

print(df.head())
df.tail()
df.shape
df.columns
df.info()
df.describe()
df.dtypes 
#Task 2 — Missing Data 
df.isnull().sum()
#1. Calculate missing values and percentages
missing_values = df.isnull().sum()
missing_percentages = (missing_values / len(df)) * 100
print("Missing Values:")
print(missing_values)
print("\nMissing Percentages:")
print(missing_percentages)
# Create a summary table
missing_summary = pd.DataFrame({
    "Missing Values": missing_values,
    "Percentage Missing": missing_percentages})

print(missing_summary)
# Numerical variables
numerical_vars = df.select_dtypes(include=['float64', 'int64']).columns
print("Numerical Variables:")
print(numerical_vars)
print(df["Age"].describe())
print(df["Age"].isnull().sum())
print(df["GeneA"].describe())
print(df["GeneA"].isnull().sum())
print(df["GeneB"].describe())
print(df["GeneB"].isnull().sum())
print(df["GeneC"].describe())
print(df["GeneC"].isnull().sum())
# Categorical variables

categorical_columns = df.select_dtypes(
    include=["object", "category"]).columns

for col in categorical_columns:
    if df[col].isnull().sum() > 0:
        mode_value = df[col].mode()[0]
        df[col] = df[col].fillna(mode_value)
        print(f"{col}: missing values replaced with mode = {mode_value}")
# Verify treatment of missing values
print("\nMissing values after treatment:")
print(df.isnull().sum())
#Task 3 — Detect and Handle Duplicates 
# IdentifY duplicated rows
duplicated_rows = df[df.duplicated()]
print("Duplicated Rows:")
print(duplicated_rows)
#Investigate duplicated Sample_ID
sample_duplicates = df[df["Sample_ID"].duplicated(keep=False)]
print("\nDuplicated Sample_ID records:")
print(sample_duplicates)
print("\nNumber of duplicated Sample_ID entries:")
print(df["Sample_ID"].duplicated().sum())
#Check whether the duplicate is an exact duplicate
exact_duplicates = df[df.duplicated(keep=False)]
print("\nExact Duplicate Records:")
print(exact_duplicates)
#Question 1: How many duplicate records exist?
print(df.duplicated().sum())
print("Sample_ID:", df["Sample_ID"].duplicated().sum())
#Question 2: Which sample is duplicated?
duplicated_samples = df.loc[
    df["Sample_ID"].duplicated(keep=False),
    "Sample_ID"
].unique()

print("Duplicated sample(s):", duplicated_samples)
#Question 3: Is it an exact duplicate?
rows = df[df["Sample_ID"] == "S010"]

print(rows)
print(rows.iloc[0].equals(rows.iloc[1]))
#5. Should it be removed?
df = df.drop_duplicates()
#Then verify
print("Duplicates after removal:", df.duplicated().sum())
#6, In a real RNA-seq experiment, why might two apparently duplicated samples actually represent legitimate technical replicates?
#In a real RNA-seq experiment, two records with apparently the same sample identifier may represent technical replicates.
#appears twice but the rows contain different measurements, do not simply delete one row.

##The duplicate could represent:
#technical replicate
#sequencing replicate
#library replicate
#repeated measurement
#independently processed aliquot 
#Task 4 — Standardize Categorical Variables 
# 1. INVESTIGATE UNIQUE VALUES BEFORE CLEANING
print("\n--- UNIQUE VALUES BEFORE CLEANING ---")

print("\nSpecies:")
print(df["Species"].unique())

print("\nTissue:")
print(df["Tissue"].unique())

print("\nSex:")
print(df["Sex"].unique())

print("\nTreatment:")
print(df["Treatment"].unique())
# 2. FREQUENCY TABLES BEFORE CLEANING

print("\n--- FREQUENCY TABLES BEFORE CLEANING ---")

print("\nSpecies:")
print(df["Species"].value_counts(dropna=False))

print("\nTissue:")
print(df["Tissue"].value_counts(dropna=False))

print("\nSex:")
print(df["Sex"].value_counts(dropna=False))

print("\nTreatment:")
print(df["Treatment"].value_counts(dropna=False))

# 3.1 STANDARDIZE TISSUE

df["Tissue"] = (
    df["Tissue"]
    .astype("string")
    .str.strip()
    .str.lower())

# 3.2. STANDARDIZE SEX


df["Sex"] = (
    df["Sex"]
    .astype("string")
    .str.strip()
    .str.lower())

df["Sex"] = df["Sex"].replace({
    "m": "male",
    "male": "male",
    "f": "female",
    "female": "female"})


# 3.3. STANDARDIZE TREATMENT

df["Treatment"] = (
    df["Treatment"]
    .astype("string")
    .str.strip()
    .str.lower())

df["Treatment"] = df["Treatment"].replace({
    "control": "control",
    "ctrl": "control",
    "treated": "treated",
    "trt": "treated"})


# 3.4. STANDARDIZE SPECIES

df["Species"] = (
    df["Species"]
    .astype("string")
    .str.strip()
    .str.lower())


# 7. UNIQUE VALUES AFTER CLEANING

print("\n--- UNIQUE VALUES AFTER CLEANING ---")

print("\nSpecies:")
print(df["Species"].unique())

print("\nTissue:")
print(df["Tissue"].unique())

print("\nSex:")
print(df["Sex"].unique())

print("\nTreatment:")
print(df["Treatment"].unique())





# 8. FREQUENCY TABLES AFTER CLEANING

print("\n--- FREQUENCY TABLES AFTER CLEANING ---")

print("\nSpecies:")
print(df["Species"].value_counts(dropna=False))

print("\nTissue:")
print(df["Tissue"].value_counts(dropna=False))

print("\nSex:")
print(df["Sex"].value_counts(dropna=False))

print("\nTreatment:")
print(df["Treatment"].value_counts(dropna=False))

#9,duplicated categories should represent one category. 
# 10. SAVE CLEANED DATASET
df["Tissue"] = df["Tissue"].str.strip().str.lower() 
df["Sex"] = df["Sex"].str.strip().str.lower() 
df["Treatment"] = df["Treatment"].str.strip().str.lower() 
df["Species"] = df["Species"].str.strip().str.lower() 

df.to_csv("messy_data_module_2_standardized.csv", index=False)

print("\nCleaned dataset saved as:")
print("messy_data_module_2_standardized.csv")

###Produce frequency tables before and after cleaning. 
import pandas as pd

# Load original dataset
df = pd.read_csv("messy_data_module_2.csv")

# Keep a copy BEFORE cleaning
df_before = df.copy()

# FUNCTION TO CREATE FREQUENCY TABLE


def frequency_table(data, column):
    result = data[column].value_counts(dropna=False).reset_index()
    result.columns = ["Category", "Frequency"]
    result.insert(0, "Variable", column)
    return result


# FREQUENCY TABLES BEFORE CLEANING


before = pd.concat([frequency_table(df_before, "Species"),frequency_table(df_before, "Tissue"),frequency_table(df_before, "Sex"),
                    frequency_table(df_before, "Treatment")], ignore_index=True)



# STANDARDIZE VARIABLES


df["Species"] = (
    df["Species"]
    .astype("string")
    .str.strip()
    .str.lower())

df["Tissue"] = (df["Tissue"]
    .astype("string")
    .str.strip()
    .str.lower())

df["Sex"] = (df["Sex"]
    .astype("string")
    .str.strip()
    .str.lower())

df["Sex"] = df["Sex"].replace({
    "m": "male",
    "male": "male",
    "f": "female",
    "female": "female"})

df["Treatment"] = (
    df["Treatment"]
    .astype("string")
    .str.strip()
    .str.lower())

df["Treatment"] = df["Treatment"].replace({
    "Control": "control",
    "control": "control",
    "ctrl": "control",
    "treated": "treated",
    "Treated": "treated",
    "trt": "treated"})


# FREQUENCY TABLES AFTER CLEANING


after = pd.concat([frequency_table(df, "Species"),frequency_table(df, "Tissue"),frequency_table(df, "Sex"),
                   frequency_table(df, "Treatment")], ignore_index=True)


# COMBINE BEFORE AND AFTER


combined = pd.merge(before,after,on=["Variable", "Category"],how="outer",suffixes=("_Before", "_After"))

# Replace missing frequencies with zero
combined["Frequency_Before"] = (combined["Frequency_Before"]
    .fillna(0)
    .astype(int))
combined["Frequency_After"] = (
    combined["Frequency_After"]
    .fillna(0)
    .astype(int))

# REORDER COLUMNS

combined = combined[["Variable","Category","Frequency_Before","Frequency_After"]]


# EXPORT ONE COMBINED EXCEL

output_file = "combined_frequency_before_after.CSV"

combined.to_csv(output_file, index=False)

# =====================================================
# FREQUENCY TABLE AFTER CLEANING
# =====================================================

after_tables = []

for column in ["Species", "Tissue", "Sex", "Treatment"]:
    table = df[column].value_counts(dropna=False).reset_index()
    table.columns = ["Category", "Frequency"]
    table.insert(0, "Variable", column)
    after_tables.append(table)

after = pd.concat(after_tables, ignore_index=True)

after_tables.append(table)

# DISPLAY
# =====================================================

print("\n========================================")
print("FREQUENCY TABLE AFTER CLEANING")
print("========================================")

print(after.to_string(index=False))



# EXPORT TO EXCEL

after.to_csv("frequency_after_cleaning.csv",index=False)

print("\nSaved successfully:")
print("frequency_after_cleaning.csv")


#Task 5 — Identify Invalid Biological Values
#  
#1. Is every age biologically reasonable? 
#2. Which sample contains an invalid age? 
#3. Could this be corrected automatically? 
#4. What should a researcher do if the original value cannot be verified? 

# #1. Examine Age
# Descriptive statistics
# Age summary
age_summary = df["Age"].describe()

# Convert to Excel-friendly table
age_summary_df = age_summary.reset_index()
age_summary_df.columns = ["Statistic", "Value"]

# Export to Excel
age_summary_df.to_csv("Age_Summary.CSV",index=False)

print("===== AGE SUMMARY =====")
print(df["Age"].describe())

print("\nCSV file created: Age_Summary.CSV") 

#2. Which sample contains an invalid age? 

print( df.loc[(df["Age"] < 0) | (df["Age"] > 120),["Sample_ID", "Age"]])
df.loc[(df["Age"] < 0) | (df["Age"] > 120),"Age"] = pd.NA

###Task 6 — Outlier Detection
import pandas as pd
import matplotlib.pyplot as plt

# 1. LOAD DATASET


df = pd.read_csv("messy_data_module_2.csv")



# 2. GENES TO INVESTIGATE


genes = ["GeneA", "GeneB", "GeneC"]



# 3. DESCRIPTIVE STATISTICS


print("\n========================================")
print("GENE EXPRESSION DESCRIPTIVE STATISTICS")
print("========================================")

statistics = df[genes].describe()

print(statistics)


# 4. IQR OUTLIER ANALYSIS


outlier_results = []

for gene in genes:

    # Remove missing values
    values = df[gene].dropna()

    # Calculate Q1 and Q3
    Q1 = values.quantile(0.25)
    Q3 = values.quantile(0.75)

    # Calculate IQR
    IQR = Q3 - Q1

    # Calculate boundaries
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # Identify outliers
    outliers = df[
        (df[gene] < lower_bound) |
        (df[gene] > upper_bound)]

    print("\n----------------------------------------")
    print(gene)
    print("----------------------------------------")

    print("Q1:", Q1)
    print("Q3:", Q3)
    print("IQR:", IQR)
    print("Lower boundary:", lower_bound)
    print("Upper boundary:", upper_bound)

    print("\nPotential outliers:")

    if len(outliers) == 0:
        print("No potential outliers detected.")
    else:
        print(outliers[["Sample_ID", gene]].to_string(index=False))

    # Save outlier information
    for _, row in outliers.iterrows():

        value = row[gene]

        if value > upper_bound:
            distance = value - upper_bound
            direction = "Above upper boundary"
        else:
            distance = lower_bound - value
            direction = "Below lower boundary"

        outlier_results.append({
            "Gene": gene,
            "Sample_ID": row["Sample_ID"],
            "Expression": value,
            "Q1": Q1,
            "Q3": Q3,
            "IQR": IQR,
            "Lower_Bound": lower_bound,
            "Upper_Bound": upper_bound,
            "Distance_From_Boundary": distance,
            "Direction": direction })


# =====================================================
# 5. CREATE OUTLIER TABLE
# =====================================================

outlier_df = pd.DataFrame(outlier_results)

print("\n========================================")
print("ALL POTENTIAL OUTLIERS")
print("========================================")

if outlier_df.empty:
    print("No IQR outliers detected.")
else:
    print(outlier_df.to_string(index=False))


# =====================================================
# 6. BOX PLOTS
# =====================================================

for gene in genes:

    plt.figure(figsize=(6, 5))

    plt.boxplot(df[gene].dropna())

    plt.ylabel("Expression Level")
    plt.title(f"{gene} Expression Distribution")

    plt.show()


# 7. EXPORT RESULTS TO EXCEL


with pd.ExcelWriter("Gene_Expression_IQR_Analysis.xlsx",engine="openpyxl") as writer:
    statistics.to_excel(writer,sheet_name="Descriptive_Statistics")
    if outlier_df.empty:
        pd.DataFrame({"Result": ["No IQR outliers detected"]
        }).to_excel(writer,sheet_name="IQR_Outliers",index=False)
    else:
        outlier_df.to_excel(writer,sheet_name="IQR_Outliers", index=False)

print("\n========================================")
print("Analysis completed successfully!")
print("excel file: Gene_Expression_IQR_Analysis.xlsx")
print("========================================")

#Task 7 — Data Transformation 

# Create average expression of the three genes
import numpy as np
df["MeanExpression"] = df[["GeneA", "GeneB", "GeneC"]].mean(axis=1)

# Create log2-transformed expression variables
df["GeneA_log2"] = np.log2(df["GeneA"] + 1)
df["GeneB_log2"] = np.log2(df["GeneB"] + 1)
df["GeneC_log2"] = np.log2(df["GeneC"] + 1)

# Display results
print("\n===== ORIGINAL AND TRANSFORMED EXPRESSION =====")

print(df[["Sample_ID",
            "GeneA",
            "GeneB",
            "GeneC",
            "MeanExpression",
            "GeneA_log2",
            "GeneB_log2",
            "GeneC_log2"]].to_string(index=False))

# Export results

df.to_excel("Gene_Expression_Transformed.xlsx",index=False)

print("\n excel file created: Gene_Expression_Transformed.xlsx")

#Hence, after log2 transformation, the distribution of gene expression values is often more normalized, which can improve the performance of statistical analysis and machine learning models.
#  Log2 transformation is particularly useful for RNA-seq data, where gene expression values can span several orders of magnitude. 
# Log2 transformation helps to reduce the impact of extreme values and makes the data more suitable for downstream analysis. 


log_genes = ["GeneA_log2", "GeneB_log2", "GeneC_log2"]
# Load Excel file
df = pd.read_excel("Gene_Expression_Transformed.xlsx")

for gene in log_genes:
    plt.figure(figsize=(7, 5))
    plt.boxplot(df[gene].dropna())
    plt.ylabel("Log2(Expression + 1)")
    plt.title(gene + " Expression Distribution")
    plt.show()

# Check shape BEFORE reshaping
print("Shape before reshaping:", df.shape)

# Task 8,Convert wide format to long format

long_df = df.melt(id_vars=["Sample_ID","Tissue","Sex",
                           "Treatment"],value_vars=["GeneA","GeneB","GeneC"],
                           var_name="Gene",value_name="Expression")

# Check shape AFTER reshaping
print("Shape after reshaping:", long_df.shape)

# Display first rows
print("\n===== LONG FORMAT =====")
print(long_df.head(10))

# Save the long-format dataset
long_df.to_excel("long_format_expression.xlsx",index=False)
df.shape

print("\nexcel file created: long_format_expression.xlsx")

#Task 9 — Final Data Validation

# Keep original data BEFORE cleaning
df_before = df.copy()



# 2. FUNCTION TO COUNT INVALID AGES


def count_invalid_ages(data):
    return ((data["Age"] < 0) | (data["Age"] > 120)).sum()


# 3. COUNT POTENTIAL OUTLIERS BEFORE CLEANING


def count_gene_outliers(data):

    total_outliers = 0

    for gene in ["GeneA", "GeneB", "GeneC"]:

        values = data[gene].dropna()

        Q1 = values.quantile(0.25)
        Q3 = values.quantile(0.75)
        IQR = Q3 - Q1

        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR

        outliers = ((data[gene] < lower) |(data[gene] > upper))

        total_outliers += outliers.sum()

    return total_outliers


# 4. BEFORE CLEANING


before_rows = len(df_before)

before_duplicates = df_before.duplicated().sum()

before_missing = df_before.isnull().sum().sum()

before_invalid_age = count_invalid_ages(df_before)

before_tissue = df_before["Tissue"].nunique()

before_sex = df_before["Sex"].nunique()

before_treatment = df_before["Treatment"].nunique()

before_outliers = count_gene_outliers(df_before)



# 5. CLEAN DATA


# Standardize Species
df["Species"] = (
    df["Species"]
    .astype("string")
    .str.strip()
    .str.lower())

# Standardize Tissue
df["Tissue"] = (df["Tissue"]
    .astype("string")
    .str.strip()
    .str.lower())

# Standardize Sex
df["Sex"] = (df["Sex"]
    .astype("string")
    .str.strip()
    .str.lower())

df["Sex"] = df["Sex"].replace({"m": "male","f": "female"})

# Standardize Treatment
df["Treatment"] = (df["Treatment"]
    .astype("string")
    .str.strip()
    .str.lower())

df["Treatment"] = df["Treatment"].replace({
    "ctrl": "control",
    "trt": "treated"})

# 6. TREAT INVALID AGE


# Invalid -5 age cannot be scientifically corrected
# without checking the original record.
df.loc[(df["Age"] < 0) | (df["Age"] > 120),"Age"] = np.nan


# 7. AFTER CLEANING


after_rows = len(df)

after_duplicates = df.duplicated().sum()

after_missing = df.isnull().sum().sum()

after_invalid_age = count_invalid_ages(df)

after_tissue = df["Tissue"].nunique()

after_sex = df["Sex"].nunique()

after_treatment = df["Treatment"].nunique()

after_outliers = count_gene_outliers(df)


# 8. BEFORE-VS-AFTER SUMMARY


quality_summary = pd.DataFrame({"Quality Measure": [
        "Number of rows",
        "Duplicate records",
        "Missing values",
        "Invalid ages",
        "Tissue categories",
        "Sex categories",
        "Treatment categories",
        "Potential outliers"],"Before Cleaning": [
        before_rows,
        before_duplicates,
        before_missing,
        before_invalid_age,
        before_tissue,
        before_sex,
        before_treatment,
        before_outliers],"After Cleaning": [
        after_rows,
        after_duplicates,
        after_missing,
        after_invalid_age,
        after_tissue,
        after_sex,
        after_treatment,
        after_outliers]})



# 9. VERIFY FINAL DATASET
# =====================================================

print("\n========================================")
print("FINAL DATASET INFORMATION")
print("========================================")

df.info()


print("\n========================================")
print("MISSING VALUES")
print("========================================")

print(df.isnull().sum())


print("\n========================================")
print("DUPLICATE RECORDS")
print("========================================")

print(df.duplicated().sum())


print("\n========================================")
print("UNIQUE SPECIES")
print("========================================")

print(df["Species"].unique())


print("\n========================================")
print("UNIQUE TISSUE")
print("========================================")

print(df["Tissue"].unique())


print("\n========================================")
print("UNIQUE SEX")
print("========================================")

print(df["Sex"].unique())


print("\n========================================")
print("UNIQUE TREATMENT")
print("========================================")

print(df["Treatment"].unique())


print("\n========================================")
print("DESCRIPTIVE STATISTICS")
print("========================================")

print(df.describe())

# 10. PRINT QUALITY SUMMARY


print("\n========================================")
print("BEFORE VS AFTER DATA QUALITY SUMMARY")
print("========================================")

print(quality_summary.to_string(index=False))



# 11. EXPORT SUMMARY


quality_summary.to_csv("Before_After_Data_Quality_Summary.csv",index=False)

print("\nFile created:")
print("Before_After_Data_Quality_Summary.csv")

# CREATE FINAL CLEANED BIOINFORMATICS DATASET

# Remove exact duplicate records
df = df.drop_duplicates()

# Standardize categorical variables
df["Species"] = (
    df["Species"]
    .astype("string")
    .str.strip()
    .str.lower()
)

df["Tissue"] = (
    df["Tissue"]
    .astype("string")
    .str.strip()
    .str.lower()
)

df["Sex"] = (
    df["Sex"]
    .astype("string")
    .str.strip()
    .str.lower()
)

df["Sex"] = df["Sex"].replace({
    "m": "male",
    "f": "female"
})

df["Treatment"] = (
    df["Treatment"]
    .astype("string")
    .str.strip()
    .str.lower()
)

df["Treatment"] = df["Treatment"].replace({
    "ctrl": "control",
    "trt": "treated"
})

# Replace biologically invalid ages with missing
df.loc[
    (df["Age"] < 0) | (df["Age"] > 120),
    "Age"
] = pd.NA

# Fill missing numeric values with median
numeric_columns = df.select_dtypes(include="number").columns

for col in numeric_columns:
    if df[col].isnull().sum() > 0:
        df[col] = df[col].fillna(df[col].median())

# Fill missing categorical values with mode
categorical_columns = df.select_dtypes(
    include=["object", "category", "string"]
).columns

for col in categorical_columns:
    if df[col].isnull().sum() > 0:
        mode_value = df[col].mode()[0]
        df[col] = df[col].fillna(mode_value)

# Recalculate mean expression
df["MeanExpression"] = df[
    ["GeneA", "GeneB", "GeneC"]
].mean(axis=1)

# Recalculate log2 expression
import numpy as np

df["GeneA_log2"] = np.log2(df["GeneA"] + 1)
df["GeneB_log2"] = np.log2(df["GeneB"] + 1)
df["GeneC_log2"] = np.log2(df["GeneC"] + 1)

# =====================================================
# SAVE FINAL DATASET
# =====================================================

output_file = "cleaned_bioinformatics_data.csv"

df.to_csv(output_file, index=False)

print("========================================")
print("FINAL CLEANED DATASET")
print("========================================")
print("File created:", output_file)

# =====================================================
# FINAL VALIDATION
# =====================================================

print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate records:")
print(df.duplicated().sum())

print("\nDataset shape:")
print(df.shape)

print("\nFirst 5 rows:")
print(df.head())

