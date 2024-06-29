'''
This script defines all the functions required to calculate the p-value for a given department and feature.
- get_employee_data: Returns the employee data for the given department from the database.
- process_column: Process the given column by filling missing values and converting data types.
- process_data: Process the data frame by filling missing values and converting data types and applying one-hot encoding to the categorical column.
- create_ols_model: Returns the OLS model for the given data frame and columns.
- get_pvalue or a feature based on whether it is numerical or categorical.

Author: Sana Iqbal
For: Syndio Take Home Assignment
'''
import sqlite3  
import os
import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.anova import anova_lm
from fastapi import HTTPException
from typing import List, Optional
from config import *
from utils import *

logger = setup_logging( script_name=os.path.basename(__file__))

def get_employee_data(department: Optional[str]) -> pd.DataFrame:
    '''Returns the employee data for the given department from the database'''
    try:
        connection = sqlite3.connect(EMPLOYEE_DB)
        if department:
            query = "SELECT * FROM employees WHERE department = ?"
            df = pd.read_sql_query(query, connection, params=(department,))
        else:
            query = "SELECT * FROM employees"
            df = pd.read_sql_query(query, connection)
        connection.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail= e)

    if df.empty:
        raise HTTPException(status_code=404, detail="No data found for the specified department")

    if len(df) < MIN_SAMPLE_COUNT:
        raise HTTPException(status_code=404, detail=f"Not sufficient data found for OLS analysis,\n need at least {MIN_SAMPLE_COUNT} data points, found {len(df)} data points.")
    logger.info(f" data for  {department} department has {len(df)} data points")
    return df


def process_column(df: pd.DataFrame, column: str) -> pd.DataFrame:
    '''
    Process the given column by filling missing values and converting data types
    '''
    config = COLUMNS_CONFIG[column]
    if config['fillna'] == 'median':
        df[column] = df[column].fillna(df[column].median())
    elif config['fillna'] == 'mode':
        df[column] = df[column].fillna(df[column].mode()[0])
    df[column] = df[column].astype(config['dtype'])
    return df


def process_data(df: pd.DataFrame,feature_columns: List[str]) -> pd.DataFrame:
    '''
    Process the data frame by filling missing values and converting data types
    and applying one-hot encoding to the categorical column
    '''
    try:
        one_hot_columns = []
        pre_one_hot = []
        df_copy = df.copy()
        for column, cfg in COLUMNS_CONFIG.items():
            df = process_column(df, column)
            if cfg['dtype'] == 'category':
                # Apply one-hot encoding to the 'protected_class' column
                df_one_hot = pd.get_dummies(df[[ID_COLUMN,column]], columns=[column], drop_first=True,dtype= float)
                one_hot_columns.extend([col for col in df_one_hot.columns if column+"_" in col])
                pre_one_hot.append(column)
                df_with_one_hot = pd.merge(df_copy, df_one_hot, on='id')
        feature_columns = [col for col in feature_columns if col not in [pre_one_hot]] + one_hot_columns
        logger.info(f"Processed data:\n one_hot_columns: {one_hot_columns}\n pre_one_hot: {pre_one_hot}")
        return df_with_one_hot,one_hot_columns,pre_one_hot
    except Exception as e:
        raise HTTPException(status_code=500, detail= f'Data not processed: \n{e}')

def create_ols_model(df: pd.DataFrame, feature_columns: List[str], label_column: str) -> Optional[sm.OLS]:
    '''Returns the OLS model for the given data frame and columns'''
    try:
        logger.info(f"Creating OLS model for data with { feature_columns, label_column}:")
        X = df[feature_columns]
        Y = df[label_column]
        X = sm.add_constant(X)
        model = sm.OLS(Y, X).fit()
        return model
    except Exception as e:
        raise HTTPException(status_code=500, detail= f'Model not created: \n{e}')

def get_pvalue_for_numerical_feature(pv_feature, processed_data,one_hot_columns,pre_one_hot ) -> Optional[float]:
    '''Returns the p-value for a numeric feature'''
    logger.info(f"Calculating p-value for numerical feature {pv_feature}")
    try:
        feature_columns_with_onehot = [col for col in FEATURE_COLUMNS if col not in pre_one_hot] + one_hot_columns
        model = create_ols_model(processed_data, feature_columns_with_onehot, LABEL_COLUMN)
        return float(round(model.pvalues[pv_feature], 3))
    except Exception as e:
        raise HTTPException(status_code=500, detail= f'PValue could not be generated: \n{e}')


def get_pvalue_for_categorical_feature(pv_feature,processed_data,one_hot_columns,pre_one_hot ) -> Optional[float]:
    '''Returns the p-value for a categorical feature aka pre_one_hot'''

    logger.info(f"Calculating p-value for categorical feature {pv_feature}")
    try:

        feature_columns_with_onehot = [col for col in FEATURE_COLUMNS if col not in pre_one_hot] + one_hot_columns
        print(feature_columns_with_onehot)
        logger.info(f"Feature columns with one-hot encoding: {feature_columns_with_onehot}")
        model_with_feature = create_ols_model(processed_data, feature_columns_with_onehot, LABEL_COLUMN)

        feature_columns_without_onehot = [col for col in FEATURE_COLUMNS if col != pv_feature] 
        logger.info(f"Feature columns without one-hot encoding: {feature_columns_without_onehot}")
        model_without_feature = create_ols_model(processed_data, feature_columns_without_onehot, LABEL_COLUMN)

        anova_results = anova_lm(model_without_feature, model_with_feature)
        combined_pvalue = anova_results['Pr(>F)'][1]
        return round(combined_pvalue, 3)
    except Exception as e:
        raise HTTPException(status_code=500, detail= f'PValue could not be generated: \n{e}')


def calculate_pvalue(department: Optional[str], pv_feature: str) -> Optional[float]:
    '''Returns the p-value for the given department and feature'''
    logger.info(f"Calculating p-value for department {department} and feature {pv_feature}")
    try:
        data = get_employee_data(department)
        processed_data,one_hot_columns,pre_one_hot = process_data(data, FEATURE_COLUMNS)
        if  pv_feature  in pre_one_hot:#categorical column
            return get_pvalue_for_categorical_feature(pv_feature,processed_data,one_hot_columns,pre_one_hot )
        else:
            return get_pvalue_for_numerical_feature(pv_feature,processed_data,one_hot_columns,pre_one_hot )
    except Exception as e:
        raise 

