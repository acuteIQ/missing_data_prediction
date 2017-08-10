from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model
import psycopg2
import random
from sklearn.cluster import KMeans
from get_range import get_range


LIMIT=' LIMIT 10000'

conn=psycopg2.connect('dbname=acuteiq')
cur=conn.cursor()

def none_to_feature_mean(data):
    feature_means = []
    for feature_index, d in enumerate(data[0]):
        feature_means.append( data[:, feature_index].mean() )

    for entry_index, entry in enumerate(data):
        if None in entry:
            data[entry_index][entry_index] = feature_means[entry_index]
    return data

cur.execute('select distinct county from company1')
counties = {}
for c in cur:
    if c:
        counties[c[0]] = len(counties)

cur.execute('select distinct city from company1')
cities = {}
for c in cur:
    if c:
        cities[c[0]] = len(cities)

cur.execute('select state state from company1')
states = {}
for c in cur:
    if c:
        states[c[0]] = len(states)


def get_data(cur, work_type, filter_none=True):
    data = [];
    row = cur.fetchone()
    while row:
        if filter_none == False or (filter_none == True and None not in row ):
            row_list = list(row)
            try:
                row_list[2] = cities[row_list[2]]
                row_list[3] = states[row_list[3]]
                row_list[4] = counties[row_list[4]]
            except ValueError as e:
                print ('index error', row_list)
                print ('cities', cities)
                print ('states', states)
                print ('counties', counties)
                raise e

            if work_type==1:
                pass
            else:
                row_list[-1] = get_range(row_list[-1])
                #row_list[-1] = int(row_list[-1])

            data.append(row_list)

        row = cur.fetchone()

    # for better testing / training test separation
    random.shuffle(data)

    return np.array(data)

for work_type in [1,2]:
    print ('work_type', work_type)

    if work_type == 1:
        cur.execute('SELECT zip, industry_sic_code, city, state, county, id, number_of_employees FROM company3' + LIMIT)
    else:
        cur.execute('SELECT zip, industry_sic_code, city, state, county, id, cast(yearly_sales as numeric) FROM company3' + LIMIT)

    data_dense = get_data(cur, work_type)

    if work_type == 1:
        cur.execute('SELECT zip, industry_sic_code, city, state, county, id, number_of_employees FROM company1 where number_of_employees is null' + LIMIT)
    else:
        cur.execute('SELECT zip, industry_sic_code, city, state, county, id, cast(yearly_sales as numeric) FROM company1 where yearly_sales is null' + LIMIT)

    data_sparse = get_data(cur, work_type, filter_none=False)

    data_len_dense = len(data_dense)
    #train_data_range_limit_dense = int(data_len*0.75)
    assert data_len_dense > 0, 'Error: found data_dense length 0'
    print ('data_len_dense', data_len_dense) #, "train_data_range_limit_dense", train_data_range_limit_dense)

    data_len_sparse = len(data_sparse)
    assert data_len_sparse > 0, 'Error: found data_sparse length 0'
    print ('data_len_sparse', data_len_sparse)
    
    feature_range = (0,1,2,3,4) # TODO test for test ranges -> factor analysis
    #data_train_dense = data_dense[:train_data_range_limit_dense, :]
    #data_test_dense = data_dense[train_data_range_limit_dense:, :]
    
    #cluster_trials = [40,] #range(10,101,10) # test with 10, 20, 30, ... 100 clusters

    #for n_clusters in cluster_trials:
    n_clusters = 40
    print ('n_clusters', n_clusters)

    n_clusters_more_than_10_len=0

    kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(data_dense[:, feature_range])

    #y_pred_train = kmeans.predict(data_train_dense[:, feature_range])
    y_pred_train = kmeans.predict(data_dense[:, feature_range])
    #y_pred_test = kmeans.predict(data_test_dense[:, feature_range])
    print (data_sparse)
    print (data_sparse.size)
    print (feature_range)
    data_sparse = none_to_feature_mean(data_sparse)
    y_predict = kmeans.predict(data_sparse[:, feature_range])

    for cluster_index in range(n_clusters):
        print('\n\ncluster', cluster_index)
        cluster_data_train_dense = data_dense[ y_pred_train == cluster_index ]
        cluster_data_train_len_dense = len(cluster_data_train_dense)
        cluster_data_predict_sparse = data_sparse[ y_predict == cluster_index ]
        cluster_data_predict_len_sparse = len(cluster_data_predict_sparse)

        print ('cluster_data_train_len_dense', cluster_data_train_len_dense, 'cluster_data_predict_len_sparse', cluster_data_predict_len_sparse)
        if cluster_data_train_len_dense < 10:
            print ('abort not enough cluster data cluster_data_test_len_dense', cluster_data_test_len_dense, 'cluster_data_train_len', cluster_data_train_len_dense )
            continue
        else:
            n_clusters_more_than_10_len += 1
            ols = linear_model.LinearRegression()
            ols.fit(cluster_data_train_dense[:, feature_range], cluster_data_train_dense[:,-1])
            for pred_index, prediction in enumerate(ols.predict( cluster_data_predict_sparse[:, feature_range] )):
                if work_type == 1:
                    predict_col_name = 'number_of_employees'
                else:
                    predict_col_name = 'yearly_sales'

                sqlcmd='INSERT INTO company_predict (id, ' + predict_col_name + ') VALUES (%s, %s)'

                sqldata=(cluster_data_train_dense[-2], prediction)
                cur.execute( sqlcmd, sqldata )
                
    print ('average rmse', total_rmse/n_clusters_more_than_10_len, 'n_clusters', n_clusters, 'n_clusters_more_than_10_len', n_clusters_more_than_10_len)
