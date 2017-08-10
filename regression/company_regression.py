from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model
import psycopg2
import random

conn=psycopg2.connect('dbname=acuteiq')
cur=conn.cursor()

for work_type in [2,1]:
    print ( 'work_type', work_type )
    for feature_range in [(0,), (1,), (0,1)]:
        print ( 'feature_range', feature_range )

        if work_type==1:
            cur.execute('SELECT zip, industry_sic_code, number_of_employees FROM company2 WHERE zip < 200000')
        else:
            cur.execute('SELECT zip, industry_sic_code, cast(yearly_sales as numeric) FROM company2 WHERE zip < 200000')

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

        # for better testing / training test separation
        random.shuffle(data)

        data = np.array(data)

        data_len = len(data)
        train_range_limit = int(data_len*0.75)
        print ('data_len', data_len, "train_range_limit", train_range_limit)
        ols = linear_model.LinearRegression()
        ols.fit(data[:train_range_limit, feature_range], data[:train_range_limit,2])

        test_result = ols.predict( data[ train_range_limit:, feature_range] )

        if len(feature_range) == 1:
            plt.figure()
            plt.scatter( data[ train_range_limit:, feature_range], data[ train_range_limit:, 2 ], color='black' )
            plt.plot(data[ train_range_limit:, feature_range], test_result, color='blue')
            if feature_range[0] == 0:
                plt.xlabel('zip')
            else:
                plt.xlabel('industry_sic_code')
            if work_type == 1:
                plt.ylabel('number_of_employees')
            else:
                plt.ylabel('yearly_sales')
            plt.show()

        elif len(feature_range) == 2:
            fig = plt.figure()
            ax = Axes3D(fig)
            ax.scatter(data[ train_range_limit:, 0], data[ train_range_limit:, 1], data[ train_range_limit:, 2 ], color='black', marker='+')
            ax.scatter(data[ train_range_limit:, 0], data[ train_range_limit:, 1], test_result, color='blue', marker='o')
            ax.set_xlabel('zip')
            ax.set_ylabel('industry_sic_code')
            if work_type == 1:
                ax.set_zlabel('number_of_employees')
            else:
                ax.set_zlabel('yearly_sales')
            plt.show()
        print (np.sqrt(np.mean((data[ train_range_limit:, 2 ] - test_result)**2)))
