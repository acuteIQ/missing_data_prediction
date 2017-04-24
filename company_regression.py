import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model
import psycopg2

conn=psycopg2.connect('dbname=acuteiq')
cur=conn.cursor()

work_type=1

if work_type==1:
    cur.execute('SELECT zip, industry_sic_code, number_of_employees FROM company')
else:
    cur.execute('SELECT zip, industry_sic_code, cast(yearly_sales as numeric) FROM company')

data = [];
row = cur.fetchone()
while row:
    if None not in row:
        if work_type==1:
            data.append(row)
        else:
            row_list = list(row)
            row_list[2] = int(row_list[2])
            data.append(row_list)
            
    row = cur.fetchone()
data = np.array(data)

data_len = len(data)
train_range_limit = int(data_len*0.75)

ols = linear_model.LinearRegression()
ols.fit(data[:(-1*train_range_limit),1], data[:(-1*train_range_limit),2])

test_result = ols.predict( data[ (-1*train_range_limit), 1] )

print np.sqrt(np.mean((data[ (-1*train_range_limit), 2 ] - test_result)**2))
