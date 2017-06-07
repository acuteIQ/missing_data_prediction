from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model
import psycopg2
import random
from sklearn.cluster import KMeans
from get_range import get_range

colors = "bgrcmykw"

conn=psycopg2.connect('dbname=acuteiq')
cur=conn.cursor()

#plot=False

for work_type in [1,2]:
    print ('work_type', work_type)
    if work_type == 1:
        cur.execute('SELECT zip, industry_sic_code, number_of_employees FROM company2')
    else:
        cur.execute('SELECT zip, industry_sic_code, cast(yearly_sales as numeric) FROM company2')

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

    # for better testing / training test separation
    random.shuffle(data)

    data = np.array(data)

    data_len = len(data)
    train_data_range_limit = int(data_len*0.75)
    print ('data_len', data_len, "train_data_range_limit", train_data_range_limit)

    feature_range = (0,1)
    data_train = data[:train_data_range_limit, :]
    data_test = data[train_data_range_limit:, :]
    
    cluster_trials = [40,] #range(10,101,10) # test with 10, 20, 30, ... 100 clusters

    for n_clusters in cluster_trials:
        print ('n_clusters', n_clusters)
        n_clusters_more_than_10_len=0

        kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(data_train[:, feature_range])
        y_pred_train = kmeans.predict(data_train[:, feature_range])
        y_pred_test = kmeans.predict(data_test[:, feature_range])

        # if plot:
        #     colors = "bgrcmykw"
        #     plt.scatter(data_train[:, 0], data_train[:, 1], c=list(map(lambda x: colors[x], y_pred_train)))
        #     plt.show()

        total_rmse=0
        for cluster_index in range(n_clusters):
            print('\n\ncluster', cluster_index)
            cluster_data_train = data_train[ y_pred_train == cluster_index ]
            cluster_data_train_len = len(cluster_data_train)
            cluster_data_test = data_test[ y_pred_test == cluster_index ]
            cluster_data_test_len = len(cluster_data_test)

            print ('cluster_data_train_len', cluster_data_train_len, 'cluster_data_test_len', cluster_data_test_len)
            if cluster_data_test_len < 10 or cluster_data_train_len < 10:
                print ('abort not enough cluster data cluster_data_test_len', cluster_data_test_len, 'cluster_data_train_len', cluster_data_train_len )
                continue
            else:
                n_clusters_more_than_10_len += 1
                ols = linear_model.LinearRegression()
                ols.fit(cluster_data_train[:, feature_range], cluster_data_train[:,2])

                test_result = ols.predict( cluster_data_test[:, feature_range] )
                rsme = np.sqrt(np.mean((cluster_data_test[:, 2] - test_result)**2))
                total_rmse += rsme
                print ('RSME', rsme)

                # if plot:
                #     if len(feature_range) == 1:
                #         plt.figure()
                #         plt.scatter( cluster_data[ train_range_limit:, feature_range], cluster_data[ train_range_limit:, 2 ], color='black', marker='o' )
                #         plt.plot(cluster_data[ train_range_limit:, feature_range], test_result, color='blue', marker='*')
                #         if feature_range[0] == 0:
                #             plt.xlabel('zip')
                #         else:
                #             plt.xlabel('industry_sic_code')
                #         if work_type == 1:
                #             plt.ylabel('number_of_employees')
                #         else:
                #             plt.ylabel('yearly_sales')
                #         plt.show()

                #     elif len(feature_range) == 2:
                #         fig = plt.figure()
                #         ax = Axes3D(fig)
                #         ax.scatter(cluster_data[ train_range_limit:, 0], cluster_data[ train_range_limit:, 1], cluster_data[ train_range_limit:, 2 ], color='black', marker='o')
                #         ax.scatter(cluster_data[ train_range_limit:, 0], cluster_data[ train_range_limit:, 1], test_result, color='blue', marker='*')
                #         ax.set_xlabel('zip')
                #         ax.set_ylabel('industry_sic_code')
                #         if work_type == 1:
                #             ax.set_zlabel('number_of_employees')
                #         else:
                #             ax.set_zlabel('yearly_sales')
                #         plt.show()

        print ('average rmse', total_rmse/n_clusters_more_than_10_len, 'n_clusters', n_clusters, 'n_clusters_more_than_10_len', n_clusters_more_than_10_len)
