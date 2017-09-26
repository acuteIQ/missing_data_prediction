import psycopg2
from get_range import get_revenue_range
from get_range import get_employee_range

LIMIT=''#LIMIT 100'

conn=psycopg2.connect('dbname=acuteiq')
cur=conn.cursor()

all_coded_objects = ['state', 'county', 'city']
coded_objects = {}

for coded_object_name in all_coded_objects:
    coded_objects[coded_object_name] = {}

    sqlcmd = 'SELECT id, ' + coded_object_name + ' FROM ' + coded_object_name + '_codes'
    print sqlcmd
    cur.execute(sqlcmd)
    for row in cur:
        coded_objects[coded_object_name][row[1]] = row[0]

if LIMIT:
    total_line_count = LIMIT.split(' ')[1]
else:
    sqlcmd = 'SELECT count(*) FROM company1 LEFT JOIN equifax ON company1.id=equifax.company_id ' + LIMIT
    print sqlcmd
    cur.execute(sqlcmd)
    total_line_count = cur.fetchone()[0]

print 'expecting', total_line_count, 'lines'

processed_line_count = 0
sqlcmd = 'SELECT industry_sic_code, city, state, county, id, cast(yearly_sales as numeric), number_of_employees, efx_creditperc, efx_failrate FROM company1 LEFT JOIN equifax ON company1.id=equifax.company_id ' + LIMIT
print sqlcmd
conn=psycopg2.connect('dbname=acuteiq')
cur2=conn.cursor()
cur2.execute(sqlcmd)

cur3=conn.cursor()
cur3.execute(sqlcmd)

for row in cur2:
    industry_sic_code = row[0]
    city_str = row[1]
    state_str = row[2]
    county_str = row[3]
    row_id = row[4]
    yearly_sales = row[5]
    number_of_employees = row[6]
    credit_score = row[7]
    business_risk = row[8]

    city = coded_objects['city'][city_str]
    state = coded_objects['state'][state_str]
    county = coded_objects['county'][county_str]

    
    if yearly_sales:
        yearly_sales_new = get_revenue_range(yearly_sales)
    else:
        yearly_sales_new = None
    if number_of_employees:
        number_of_employees = get_employee_range(number_of_employees)
    else:
        number_of_employees = None

    print ('yearly_sales', yearly_sales, 'yearly_sales_new', yearly_sales_new)
    #print ('row_id', row_id, 'yearly_sales', yearly_sales_new, 'number_of_employees', number_of_employees,
    #       'credit_score', credit_score, 'business_risk', business_risk, 'industry_sic_code', industry_sic_code,
    #       'city_str', city_str, 'city', city, 'state_str', state_str,
    #       'state', state, 'county_str', county_str, 'county', county)

    sqlcmd = "INSERT INTO company_tf_observation (id, yearly_sales, number_of_employees,  credit_score, business_risk, industry_sic_code,  city_str, city, state_str,  state, county_str, county) VALUES (%s, %s, %s,  %s, %s, %s,  %s, %s, %s,  %s, %s, %s )"
    sqldata = (row_id, yearly_sales_new, number_of_employees, credit_score, business_risk, industry_sic_code, city_str, city, state_str, state, county_str, county)
    #print sqlcmd, sqldata
    cur3.execute(sqlcmd, sqldata)
    
    processed_line_count += 1
    if processed_line_count % 10000 == 0:
        print 'progress', processed_line_count/float(total_line_count)*100, '%%'

conn.commit()
cur2.close()
cur.close()
conn.close()
print 'WTF'
