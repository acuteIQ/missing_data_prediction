import psycopg2
from get_range import get_revenue_range
from get_range import get_employee_range

conn=psycopg2.connect('dbname=acuteiq')
cur=conn.cursor()

sqlcmd = 'SELECT distinct(industry_sic_code) FROM company_tf_observation';
cur.execute(sqlcmd)
distinct_industry_sic_codes = []
for row in cur:
    distinct_industry_sic_codes.append(row)

for isc_index, isc in enumerate(distinct_industry_sic_codes):
    sqlcmd = "UPDATE company_tf_observation SET industry_sic_code = %s WHERE industry_sic_code = %s;"
    sqldata = (isc_index, isc)
    print sqlcmd, sqldata
    cur.execute(sqlcmd, sqldata)

conn.commit()
cur.close()
