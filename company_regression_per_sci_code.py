import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model
import psycopg2
from datetime import datetime


conn=psycopg2.connect('dbname=acuteiq')
cur=conn.cursor()

cur.execute('SELECT DISTINCT industry_sic_code FROM company')
all_sic_codes = list(map( lambda x: x[0], cur.fetchall() ))
print 'total number of sic_codes', len(all_sic_codes)

start_time=datetime.now()
print 'start date', start_time
for sic_code_index, sic_code in enumerate(all_sic_codes):
    percent_done = sic_code_index*100.0/len(all_sic_codes)
    print "processing sci_code", sic_code, "complete %.2f percent"%(percent_done), "time left %.2f seconds" % (((datetime.now()-start_time).total_seconds())/(percent_done+0.0001)*100.0)
    cur.execute('SELECT zip, industry_sic_code, number_of_employees FROM company WHERE industry_sic_code = %s', (sic_code,))

    data = [];
    row = cur.fetchone()
    while row:
        if None not in row:
            data.append(row)
        row = cur.fetchone()

    data_len = len(data)
    print "found data_len", data_len
    if data_len<10:
        print "abort"
        continue

    data = np.array(data)

    train_range_limit = int(data_len*0.75)

    ols = linear_model.LinearRegression()
    feature_range = (0,1) 
    ols.fit(data[:train_range_limit, feature_range], data[:train_range_limit,2])

    test_result = ols.predict( data[ train_range_limit:, feature_range] )
    test_ground_truth = data[ train_range_limit:, 2 ]
    print 'sic_code', sic_code, 'RMSE %2.f'% np.sqrt(np.mean((test_ground_truth - test_result)**2)), 'number of test data', test_ground_truth.size, 'min', min(test_ground_truth), 'max', max(test_ground_truth), 'mean %.2f'% (sum(test_ground_truth)/float(test_ground_truth.size) )
