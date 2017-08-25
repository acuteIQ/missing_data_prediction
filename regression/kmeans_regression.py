from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from sklearn import linear_model
import psycopg2
import random
from sklearn.cluster import KMeans
from get_range import get_revenue_range
from get_range import get_employee_range
from get_target_col_name import get_target_col_name
import matplotlib.pyplot as plt

LIMIT='' # LIMIT 1000'

operation_type='predict' #'test' # predict or test
print ('operation_type', operation_type)

HIST_PLOT_RESULTS=True

#all_target_types=['credit_score',]
#all_target_types=['business_risk',]
#all_target_types=['number_of_employees',]
all_target_types=['yearly_sales',]

company_features = 'zip, industry_sic_code, city, state, county, id'
feature_range = (0,1,2,3,4) # must start from 0 and be consecutive -> np.where(np.equal(row[feature_range[0]:feature_range[-1]], None))

conn=psycopg2.connect('dbname=acuteiq')
cur=conn.cursor()

def filter_vector_nans(data):
    if sum(data.shape[1:]) > 0:
        raise Exception('Can only filter vectors')
    else:
        return np.array([ x for x in data if x is not None ])

def none_to_feature_mean(data):
    feature_means = []
    for feature_index in feature_range:
        feature_means.append( filter_vector_nans(data[:, feature_index]).mean() )
    feature_means = np.array(feature_means)

    for row_index, row in enumerate(data):
        none_indices = np.where(np.equal(row[feature_range[0]:feature_range[-1]], None))
        data[row_index][none_indices] = feature_means[none_indices]

    return data

cur.execute('select distinct county from company1 union select distinct county from company3')
counties = {}
for c in cur:
    if c:
        counties[c[0]] = len(counties)

cur.execute('select distinct city from company1 union select distinct city from company3')
cities = {}
for c in cur:
    if c:
        cities[c[0]] = len(cities)

cur.execute('select state state from company1 union select distinct state from company3')
states = {}
for c in cur:
    if c:
        states[c[0]] = len(states)

def get_data(conn, db_name, target_type, get_null_targets=False):
    data = [];
    if target_type not in all_target_types:
        raise Exception( str('unknown target_type: ' + target_type) )

    target_col = get_target_col_name(target_type)

    filter_str = ''
    if get_null_targets:
        filter_str = ' WHERE ' + target_col + ' is null '
    else:
        filter_str = ' WHERE ' + target_col + ' is not null '

    if target_type in ['yearly_sales', 'number_of_employees']:
        sqlcmd = 'SELECT ' + company_features + ',' + target_col + ' FROM ' + db_name + ' ' + filter_str + ' ' +  LIMIT
    elif target_type in ['business_risk', 'credit_score']:
        sqlcmd = 'SELECT ' + company_features + ',' + target_col + ' FROM ' + db_name + ' INNER JOIN equifax ON ' + db_name + '.id = equifax.company_id ' + LIMIT

    print ('get_data',sqlcmd)
    cur.execute(sqlcmd)

    row = cur.fetchone()
    while row:
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

        if target_type=='yearly_sales' and row_list[-1] is not None: # for prediction target may be none
            row_list[-1] = get_revenue_range(row_list[-1])

        if target_type=='number_of_employees' and row_list[-1] is not None: # for prediction target may be none
            row_list[-1] = get_employee_range(row_list[-1])

        data.append(row_list)
        row = cur.fetchone()

    # for better testing / training test separation
    random.shuffle(data)

    return np.array(data)

def filter_prediction(target_type, prediction):
    if target_type == 'credit_score':
        if prediction < 0:
            prediction = 0
        elif prediction > 100:
            prediction = 100

    elif target_type == 'business_risk':
        if prediction < 1:
            prediction = 1
        elif prediction > 9:
            prediction = 9

    elif target_type == 'number_of_employees':
        if prediction < 0:
            prediction = 0
        elif prediction >= len(employee_ranges):
            prediction = len(employee_ranges)-1

    elif target_type == 'yearly_sales':
        if prediction < 0:
            prediction = 0
        elif prediction >= len(sales_ranges):
            prediction = len(sales_ranges)-1

    return prediction

for target_type in all_target_types:
    print ('target_type', target_type)
    hist_plot_data = []

    if operation_type == 'test':
        all_data = get_data(conn, 'company3', target_type)
        train_data_range_limit = int(len(all_data)*0.75)
        train_data = all_data[:train_data_range_limit, :]
        predict_data = all_data[train_data_range_limit:, :] # test
    elif operation_type == 'predict':
        train_data = get_data(conn, 'company3', target_type)
        predict_data = get_data(cur, 'company1', target_type, get_null_targets=True) # predict, dummy target variable required to get prediction db
    else:
        raise Exception(str('Unknown operation_type ' + operation_type))

    train_data_len = len(train_data)
    predict_data_len = len(predict_data)
    print ('train_data_len', train_data_len, 'predict_data_len', predict_data_len)

    assert train_data_len > 0, 'Error: found train_data_len length 0'
    print ('train_data_len', train_data_len)

    assert predict_data_len > 0, 'Error: found predict_data_len length 0'
    print ('predict_data_len', predict_data_len)

    n_clusters = 40
    print ('feature_range', feature_range, 'n_clusters', n_clusters)

    n_clusters_more_than_10_len=0
    total_rmse=0
    number_of_rmse_values=0

    kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(train_data[:, feature_range])

    if operation_type == 'predict':
        predict_data = none_to_feature_mean(predict_data)

    lr_train = kmeans.predict(train_data[:, feature_range])
    lr_predict = kmeans.predict(predict_data[:, feature_range])
    #predict_col_name = get_target_col_name(target_type)

    for cluster_index in range(n_clusters):
        print('\n\ncluster', cluster_index)
        number_of_rmse_values_cluster = 0
        total_rmse_cluster = 0
        cluster_data_train = train_data[ lr_train == cluster_index ]
        cluster_data_train_len = len(cluster_data_train)
        cluster_data_predict = predict_data[ lr_predict == cluster_index ]
        cluster_data_predict_len = len(cluster_data_predict)

        print ('cluster_data_train_len', cluster_data_train_len, 'cluster_data_predict_len', cluster_data_predict_len)

        if cluster_data_train_len < 10 or cluster_data_predict_len == 0:
            print ('abort not enough cluster data cluster_data_train_len', cluster_data_train_len, 'cluster_data_predict_len', cluster_data_predict_len )
            continue
        else:
            n_clusters_more_than_10_len += 1
            ols = linear_model.LinearRegression()
            ols.fit(cluster_data_train[:, feature_range], cluster_data_train[:,-1])
            for pred_index, prediction in enumerate(ols.predict( cluster_data_predict[:, feature_range] )):
                prediction = filter_prediction(target_type, prediction)
                sqlcmd='UPDATE company_prediction SET ' + target_type + '=' + ' %s WHERE id=%s'
                sqldata=(int(prediction), int(cluster_data_predict[pred_index][-2]))
                if operation_type == 'test':
                    total_rmse_cluster += float(abs(prediction-cluster_data_predict[pred_index][-1]))
                    number_of_rmse_values_cluster += 1
                    if HIST_PLOT_RESULTS:
                        hist_plot_data.append(prediction)
                elif operation_type == 'predict':
                    try:
                        #print ('execute', sqlcmd, sqldata)
                        cur.execute( sqlcmd, sqldata )
                    except Exception as e:
                        print ('sqlcmd', sqlcmd, 'sqldata', sqldata)
                        print ('all results', ols.predict( cluster_data_predict[:, feature_range] ))
                        raise e
            if operation_type == 'test':
                print ('average CLUSTER rmse', total_rmse_cluster/number_of_rmse_values_cluster, 'cluster id', cluster_index)
            total_rmse += total_rmse_cluster
            number_of_rmse_values += number_of_rmse_values_cluster

    print ('n_clusters_more_than_10_len', n_clusters_more_than_10_len)
    if operation_type == 'test':
        print ('average rmse', total_rmse/number_of_rmse_values, 'n_clusters', n_clusters)

    if HIST_PLOT_RESULTS:
        plt.figure()
        plt.title('Test ' + target_type )
        plt.hist(hist_plot_data)

conn.commit()
cur.close()
conn.close()

if HIST_PLOT_RESULTS:
    plt.show()
