import os
import csv
import json
DATA_DIR='../data/data_export_ck'

all_column_names=[]
all_column_counts=[]
data_line_count=0
extract_unique_columns=['Company_Name', 'city', 'zip', 'industry_sic_code']
extract_unique_columns_data={}

for filename in os.listdir(DATA_DIR):
    print filename
    if filename.startswith('tbl_company'):
        f=open(os.path.join(DATA_DIR,filename))
        csvreader=csv.reader(f)
        first_line=True
        for line in csvreader:
            if first_line: # skip first line of each file
                first_line=False
                if not all_column_names:
                    all_column_names=line
                    all_column_counts = [0]*len(line)
            else:
                data_line_count+=1
                for column_index, column_data in enumerate(line):
                    if column_data:
                        all_column_counts[column_index]+=1
                        column_name=all_column_names[column_index]
                        if column_name in extract_unique_columns:
                            if column_name not in extract_unique_columns_data:
                                extract_unique_columns_data[column_name] = set()
                            extract_unique_columns_data[column_name].add(column_data)
        f.close()

#print 'data_line_count', data_line_count
#print all_column_counts
f=open('company_all_column_counts.json', 'w')
# set is not json exportable
for column_name in extract_unique_columns_data:
    extract_unique_columns_data[column_name]=list(extract_unique_columns_data[column_name])
output={
    'all_column_names':all_column_names,
    'all_column_counts':all_column_counts,
    'data_line_count':data_line_count,
    'extract_unique_columns':extract_unique_columns,
    'extract_unique_columns_data':extract_unique_columns_data
    }
f.write(json.dumps(output))
f.close()
