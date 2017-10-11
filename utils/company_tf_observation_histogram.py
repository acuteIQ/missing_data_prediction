import psycopg2
import matplotlib.pyplot as plt

conn=psycopg2.connect('dbname=acuteiq')
cur=conn.cursor()

hist_col_names=['credit_score',]
for col_name_index, col_name in enumerate(hist_col_names):
    print (col_name)
    plt.figure()
    cur.execute('select ' + col_name + ' from company_tf_observation where ' + col_name + ' is not null ')
    print ('sql done')
    res = cur.fetchall()
    res_plt = list(map(lambda i: int(i[0]),res))
    print ('fetch done count: %s' %len(res_plt))
    print (res_plt[0:10])
    plt.title(col_name)
    hist_data = plt.hist(res_plt)
    print ( 'hist done')

    plt.figure()

    print (hist_data[0])
    print (hist_data[1])
    for ind, val in enumerate(hist_data[0]):
        if ind != 0:
            hist_data[0][len(hist_data[0])-ind-1] += hist_data[0][len(hist_data[0])-ind]

    plt.plot(hist_data[1][0:10], hist_data[0])
    plt.title('Credit Score (postgresql)')
    plt.xlabel('credit score')
    plt.ylabel('reverse cumulative distribution')
    print (hist_data[0])
    print (hist_data[1])
    plt.show()
