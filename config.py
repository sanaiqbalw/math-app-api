MIN_SAMPLE_COUNT = 10
LABEL_COLUMN = 'compensation'
FEATURE_COLUMNS = ['protected_class', 'tenure','performance']
EMPLOYEE_DB = 'employees.db'
ID_COLUMN = 'id'
COLUMNS_CONFIG = {
    'protected_class': {'dtype': 'category', 'fillna': 'mode'},
    'tenure': {'dtype': 'Int64', 'fillna': 'median'},
    'performance': {'dtype': 'Int64', 'fillna': 'median'},
    'compensation': {'dtype': 'Int64', 'fillna': 'median'}
}

