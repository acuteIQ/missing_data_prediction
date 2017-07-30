import psycopg2
import os
import csv
import sys
from zip_to_int import zip_to_int
from get_target_col_name import get_target_col_name_company_prediction
import matplotlib.pyplot as plt

conn=psycopg2.connect('dbname=acuteiq')
cur=conn.cursor()

DATA_DIR='../data/data_export_ck'
DATA_FILE_PREFIX='tbl_equifax'

company_import_col_names=['yearly_sales', 'number_of_employees', 'credit_score', 'business_risk']
histogram_data=[[]]*len(company_import_col_names)

LIMIT=''# LIMIT 1000'

for col_name in company_import_col_names:
    plt.figure()
    cur.execute('select ' + get_target_col_name_company_prediction(col_name) + ' from company_prediction where ' + get_target_col_name_company_prediction(col_name) + ' is not null ' + LIMIT)
    res = cur.fetchall()
    res_plt = list(map(lambda i: float(i[0]),res))
    plt.title(col_name)
    plt.hist(res_plt)

plt.show()
