import os
import csv
import json
import numpy as np

DATA_DIR='../data/data_export_ck'
ALL_DATA_FILE_PREFIX=['tbl_company', 'tbl_equifax',  'tbl_exp_matches']
DATA_FILE_PREFIX='tbl_company'

X_AXIS_COLUMN_NAME='industry_sic_code'
Y_AXIS_COLUMN_NAME='number_of_employees'

all_column_names={}
all_column_counts={}
data_line_count={}

data_points={ 'x':[], 'y':[] }

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
                            if column_name == X_AXIS_COLUMN_NAME:
                                data_points['x'].append(column_data_int)
                            elif column_name == Y_AXIS_COLUMN_NAME:
                                data_points['y'].append(column_data_int)

            if data_line_count[DATA_FILE_PREFIX] and len(data_points['x']) != len(data_points['y']):
                if len(data_points['x']) - len(data_points['y']) == 1:
                    data_points['y'].append(np.nan)
                elif len(data_points['y']) - len(data_points['x']) == 1:
                    data_points['x'].append(np.nan)
                else:
                    raise Exception('Bad data length ' + str(len(data_points['y'])) + ' ' +  str(len(data_points['x'])))

        f.close()

f=open('company_sic_vs_employee_num.json', 'wb')
output={
    'data_points':data_points
}
f.write(json.dumps(output))
f.close()
