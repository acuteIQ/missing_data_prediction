import json
f=open('data_analysis.json')
input_data=json.loads(f.read())
f.close()

for DATA_FILE_PREFIX in input_data['all_data_file_prefix']:
    print "DATA_FILE_PREFIX:", DATA_FILE_PREFIX
    print 'total number of rows', input_data['data_line_count'][DATA_FILE_PREFIX]
    result=[]
    for company_name_index, company_name in enumerate(input_data['all_column_names'][DATA_FILE_PREFIX]):
        result.append( (company_name, input_data['all_column_counts'][DATA_FILE_PREFIX][company_name_index]) )

    print 'column_name', 'number of occurrence', 'occurrence percentage'
    for r in sorted(result, key=lambda x:x[1], reverse=True):
        print r[0], r[1], '%.0f'%(r[1]/float(input_data['data_line_count'][DATA_FILE_PREFIX])*100)

    print 'column_name', 'number of unique data'
    for extract_unique_column in input_data['extract_unique_columns'][DATA_FILE_PREFIX]:
        print extract_unique_column, len(input_data['extract_unique_columns_data'][DATA_FILE_PREFIX][extract_unique_column])
