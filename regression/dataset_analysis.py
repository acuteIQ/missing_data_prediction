import os
import csv
import json
DATA_DIR='../data/data_export_ck'
ALL_DATA_FILE_PREFIX=['tbl_company', 'tbl_equifax',  'tbl_exp_matches']

all_column_names={}
all_column_counts={}
data_line_count={}
extract_unique_columns= {
    'tbl_company':['Company_Name', 'city', 'zip', 'industry_sic_code'],
    'tbl_equifax':['CLIENT_NAME', 'CLIENT_CITY', 'CLIENT_ZIP', 'EFX_PRIMSIC'],
    'tbl_exp_matches':[]
}
extract_unique_columns_data={}

for DATA_FILE_PREFIX in ALL_DATA_FILE_PREFIX:
    all_column_counts[DATA_FILE_PREFIX]=0
    data_line_count[DATA_FILE_PREFIX]=0
    print 'DATA_FILE_PREFIX:', DATA_FILE_PREFIX
    for filename in os.listdir(DATA_DIR):
        if filename.startswith(DATA_FILE_PREFIX):
            print filename
            f=open(os.path.join(DATA_DIR,filename))
            csvreader=csv.reader(f)
            first_line=True
            for line in csvreader:
                if first_line: # skip first line of each file
                    first_line=False
                    if DATA_FILE_PREFIX not in all_column_names:
                        all_column_names[DATA_FILE_PREFIX]=line
                        all_column_counts[DATA_FILE_PREFIX] = [0]*len(line)
                        extract_unique_columns_data[DATA_FILE_PREFIX]={}
                else:
                    data_line_count[DATA_FILE_PREFIX]+=1
                    for column_index, column_data in enumerate(line):
                        if column_data:

                            valid_data=True
                            try:
                                column_data_int=int(column_data)
                                if column_data_int == 0:
                                    valid_data=False
                            except:
                                pass

                            if column_data == 'null':
                                valid_data=False

                            if valid_data:
                                all_column_counts[DATA_FILE_PREFIX][column_index]+=1
                                column_name=all_column_names[DATA_FILE_PREFIX][column_index]
                                if column_name in extract_unique_columns[DATA_FILE_PREFIX]:
                                    if column_name not in extract_unique_columns_data[DATA_FILE_PREFIX]:
                                        extract_unique_columns_data[DATA_FILE_PREFIX][column_name] = set()
                                    extract_unique_columns_data[DATA_FILE_PREFIX][column_name].add(column_data)
            f.close()

f=open('data_analysis.json', 'w')
# set is not json exportable
for DATA_FILE_PREFIX in ALL_DATA_FILE_PREFIX:
    for column_name in extract_unique_columns_data[DATA_FILE_PREFIX]:
        extract_unique_columns_data[DATA_FILE_PREFIX][column_name]=list(extract_unique_columns_data[DATA_FILE_PREFIX][column_name])

output={
    'all_data_file_prefix':ALL_DATA_FILE_PREFIX,
    'all_column_names':all_column_names,
    'all_column_counts':all_column_counts,
    'data_line_count':data_line_count,
    'extract_unique_columns':extract_unique_columns,
    'extract_unique_columns_data':extract_unique_columns_data
}
f.write(json.dumps(output))
f.close()
