import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model
import psycopg2

conn=psycopg2.connect('dbname=acuteiq')
cur=conn.cursor()

work_type=2

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
print 'data_len', data_len, "train_range_limit", train_range_limit
ols = linear_model.LinearRegression()
feature_range = (1,)
ols.fit(data[:train_range_limit, feature_range], data[:train_range_limit,2])

test_result = ols.predict( data[ train_range_limit:, feature_range] )

print np.sqrt(np.mean((data[ train_range_limit:, 2 ] - test_result)**2))
