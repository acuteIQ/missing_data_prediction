import json
f=open('company_all_column_counts.json')
input_data=json.loads(f.read())
f.close()

print 'total number of rows', input_data['data_line_count']
result=[]
for company_name_index, company_name in enumerate(input_data['all_column_names']):
    result.append( (company_name, input_data['all_column_counts'][company_name_index]) )

print 'column_name', 'number of occurrence', 'occurrence percentage'
for r in sorted(result, key=lambda x:x[1], reverse=True):
    print r[0], r[1], '%.0f'%(r[1]/float(input_data['data_line_count'])*100)

print 'column_name', 'number of unique data'
for extract_unique_column in input_data['extract_unique_columns']:
    print extract_unique_column, len(input_data['extract_unique_columns_data'][extract_unique_column])
