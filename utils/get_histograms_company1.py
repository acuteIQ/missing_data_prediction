import psycopg2
import matplotlib.pyplot as plt

conn=psycopg2.connect('dbname=acuteiq')
cur=conn.cursor()

hist_col_names=['cast(yearly_sales as numeric)', 'number_of_employees']
for col_name_index, col_name in enumerate(hist_col_names):
    print (col_name)
    plt.figure()
    cur.execute('select ' + col_name + ' from company1 where ' + col_name + ' is not null ')
    print ('sql done')
    res = cur.fetchall()
    res_plt = list(map(lambda i: int(i[0]),res))
    print ('fetch done')
    print (res[0:10])
    plt.title(col_name)
    plt.hist(res_plt)
    print ( 'hist done')
    plt.show()
