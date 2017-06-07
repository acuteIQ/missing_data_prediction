from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model
import psycopg2
from datetime import datetime
import random

sales_ranges=[
    {'min': 0, 'max': 499, 'symbol': 'A'},
    {'min': 500, 'max': 999, 'symbol': 'B'},
    {'min': 1000, 'max': 2499, 'symbol': 'C'},
    {'min': 2500, 'max': 4999, 'symbol': 'D'},
    {'min': 5000, 'max': 9999, 'symbol': 'E'},
    {'min': 10000, 'max': 19999, 'symbol': 'F'},
    {'min': 20000, 'max': 49999, 'symbol': 'G'},
    {'min': 50000, 'max': 99999, 'symbol': 'H'},
    {'min': 100000, 'max': 499999, 'symbol': 'I'},
    {'min': 500000, 'max': 999999, 'symbol': 'J'},
    {'min': 1000000, 'max': float('inf'), 'symbol': 'K'}
    ]

def get_range(value, range_type='index'):
    for sr_index, sr in enumerate(sales_ranges):
        if sr['min'] <= value and value <= sr['max']:
            if range_type == 'index':
                return sr_index
            else:
                return sr['symbol']

    raise Exception( str('get_range broke! ' + str(value) + ' sales_ranges ' + str(sales_ranges)) )

conn=psycopg2.connect('dbname=acuteiq')
cur=conn.cursor()

cur.execute('SELECT DISTINCT industry_sic_code FROM company2')
all_sic_codes = list(map( lambda x: x[0], cur.fetchall() ))

lens={}
for s in all_sic_codes:
     try:
         lens[len(str(s))] += 1
     except KeyError:
         lens[len(str(s))] = 1
     except Exception as e:
         print (s)
         print (e)
print (lens)

all_work_types=[2,1]
for work_type in all_work_types:
    print("work_type", work_type)
    all_significant_digits=[1,2,3,4]
    for significant_digits in all_significant_digits:
        print ("significant_digits", significant_digits)
        reduced_sic_codes = set()
        for sic_code in all_sic_codes:
            if sic_code:
                sic_code_digit_num = len(str(sic_code))
                if significant_digits == all_significant_digits[-1]:
                    reduced_sic_codes.add(sic_code)
                else:
                    reduced_sic_codes.add( int(str(sic_code)[0:significant_digits]+('0'*(sic_code_digit_num-significant_digits))) )

        #start_time=datetime.now()
        #print ('start date', start_time)
        total_rmse=0
        rmse_found_count=0
        for sic_code_index, sic_code_lower_bound in enumerate(list(reduced_sic_codes)):
            percent_done = sic_code_index*100.0/len(reduced_sic_codes)
            sic_code_digit_num = len(str(sic_code_lower_bound))
            sic_code_upper_bound = int(str(int(str(sic_code_lower_bound)[0:significant_digits])+1)+('0'*(sic_code_digit_num-significant_digits)))
            print ("processing sci_code_lower_bound", sic_code_lower_bound, "sic_code_upper_bound", sic_code_upper_bound, "complete %.2f percent"%(percent_done))

            if work_type==1:
                if significant_digits == all_significant_digits[-1]:
                    cur.execute('SELECT zip, industry_sic_code, number_of_employees FROM company2 WHERE industry_sic_code = %s', (sic_code_lower_bound,))
                else:
                    cur.execute('SELECT zip, industry_sic_code, number_of_employees FROM company2 WHERE industry_sic_code >= %s AND industry_sic_code < %s', (sic_code_lower_bound, sic_code_upper_bound))
            else:
                if significant_digits == all_significant_digits[-1]:
                    cur.execute('SELECT zip, industry_sic_code, cast(yearly_sales as numeric) FROM company2 WHERE industry_sic_code = %s', (sic_code_lower_bound,))
                else:
                    cur.execute('SELECT zip, industry_sic_code, cast(yearly_sales as numeric) FROM company2 WHERE industry_sic_code >= %s AND industry_sic_code < %s', (sic_code_lower_bound, sic_code_upper_bound))


            data = [];
            row = cur.fetchone()
            while row:
                if None not in row:
                    if work_type==1:
                        data.append(row)
                    else:
                        row_list = list(row)
                        row_list[2] = int(row_list[2])
                        row_list[-1] = get_range(row_list[-1])
                        data.append(row_list)

                row = cur.fetchone()

            data_len = len(data)
            #print ("found data_len", data_len,)
            if data_len<10:
                print ("abort", data_len, data)
                continue

            # for better testing / training test separation
            random.shuffle(data)

            data = np.array(data)

            train_range_limit = int(data_len*0.75)

            ols = linear_model.LinearRegression()
            feature_range = (0,1) 
            ols.fit(data[:train_range_limit, feature_range], data[:train_range_limit,2])

            test_result = ols.predict( data[ train_range_limit:, feature_range] )
            test_ground_truth = data[ train_range_limit:, 2 ]
            rmse = np.sqrt(np.mean((test_ground_truth - test_result)**2))
            total_rmse += rmse
            rmse_found_count += 1
            print ('sic_code_lower_bound', sic_code_lower_bound, 'RMSE %2.f'% rmse, 'number of test data', test_ground_truth.size, 'min', min(test_ground_truth), 'max', max(test_ground_truth), 'mean %.2f'% (sum(test_ground_truth)/float(test_ground_truth.size) ))

        if rmse_found_count == 0:
            print( 'rmse_found_count is 0!')
        else:
            print ('average rmse %.2f' % ( total_rmse/float(rmse_found_count)), 'rmse_found_count', rmse_found_count)
        print ('total number of sic_codes', len(all_sic_codes), 'total number of reduces sic_codes', len(reduced_sic_codes))
