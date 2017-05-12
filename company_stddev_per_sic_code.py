import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model
import psycopg2
from datetime import datetime
import random

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
        found_stddev=0
        for sic_code in all_sic_codes:
            if sic_code:
                sic_code_digit_num = len(str(sic_code))
                if significant_digits == all_significant_digits[-1]:
                    reduced_sic_codes.add(sic_code)
                else:
                    reduced_sic_codes.add( int(str(sic_code)[0:significant_digits]+('0'*(sic_code_digit_num-significant_digits))) )

        #start_time=datetime.now()
        #print ('start date', start_time)
        total_stddev=0
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
            total_stddev += np.std(data)
            found_stddev += 1
            print ('sic_code_lower_bound', sic_code_lower_bound, 'stddev %2.f'% np.std(data), )

        if found_stddev == 0:
            print( 'stddev found is 0!')
        else:
            print ('average stddev %.2f' % ( total_stddev/found_stddev), 'found_stdde', found_stddev)
        print ('total number of sic_codes', len(all_sic_codes), 'total number of reduces sic_codes', len(reduced_sic_codes))
