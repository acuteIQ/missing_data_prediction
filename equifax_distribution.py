import psycopg2
import os
import csv
import sys
from zip_to_int import zip_to_int
import matplotlib.pyplot as plt

DATA_DIR='../data/data_export_ck'
DATA_FILE_PREFIX='tbl_equifax'

company_import_col_names=['efx_creditperc', 'efx_failrate']
company_import_col_types=['int', 'int']
histogram_data=[[], []]

data_line_count=0
seen_ids=[]
for filename in os.listdir(DATA_DIR):
    if filename.startswith(DATA_FILE_PREFIX):
        csv_filehandle=open(os.path.join(DATA_DIR, filename))
        csvreader=csv.reader(csv_filehandle)
        header_line=True
        file_column_names=[]
        for line in csvreader:
            if header_line:
                header_line=False
                file_column_names=line
                #print ('header_line', file_column_names)
            else:
                data_line_count+=1
                #print ('\nline', data_line_count)
                for column_index, column_data in enumerate(line):
                    column_name=file_column_names[column_index].lower()
                    if column_name in company_import_col_names:
                        valid_data=True
                        is_int=False
                        try:
                            column_data=int(column_data)
                            if column_data == 0:
                                valid_data=False
                            is_int=True
                        except:
                            #print ('Bad integer', 'column_name', column_name, 'column_data', column_data, 'line', line, 'file_column_names', file_column_names )
                            pass

                        if column_data == 'null' or column_data == 'NULL':
                            #print( 'found null', 'column_name', column_name, 'column_data', column_data, 'line', line, 'file_column_names', file_column_names )
                            valid_data=False

                        #print ('column_name', column_name)
                        if company_import_col_types[company_import_col_names.index(column_name)] == 'int' and is_int == False:
                            #print( 'was expecting integer, found non-integer', 'column_name', column_name, 'column_data', column_data, 'line', line, 'file_column_names', file_column_names )
                            valid_data=False

                        if column_data and is_int == False:
                            column_data = column_data.lower()

                        if valid_data:
                            insert_index = company_import_col_names.index(column_name)
                            histogram_data[insert_index].append(column_data)
                        #else:
                            #print ('WTF2', 'column_name', column_name, column_data)

print (len(histogram_data[0]))
print (len(histogram_data[1]))

plt.figure()
plt.title('Equifax: efx_creditperc')
plt.hist(histogram_data[0])

plt.figure()
plt.title('Equifax: efx_failrate')
plt.hist(histogram_data[1])

plt.show()
