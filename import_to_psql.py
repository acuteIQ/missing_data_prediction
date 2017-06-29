import psycopg2
import os
import csv
import sys
from zip_to_int import zip_to_int
#exitcount=1000

DATA_DIR='../data/data_export_ck'
DATA_FILE_PREFIX='tbl_company'
conn=psycopg2.connect('dbname=acuteiq')
cur=conn.cursor()

company_import_col_names=['id', 'zip', 'industry_sic_code', 'number_of_employees', 'yearly_sales', 'company_name_cleaned', 'city', 'state', 'county']
company_import_col_types=['int', 'int', 'int', 'int', 'int', 'str', 'str', 'str', 'str']
data_line_count=0
seen_ids=[]
for filename in os.listdir(DATA_DIR):
    if filename.startswith(DATA_FILE_PREFIX):
        csv_filehandle=open(os.path.join(DATA_DIR, filename))
        csvreader=csv.reader(csv_filehandle)
        header_line=True
        file_column_names=[]
        for line in csvreader:
            sqlcmd='INSERT INTO company3 (' + ','.join(company_import_col_names) + ') VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
            sqldata=[None]*len(company_import_col_names)
            if header_line:
                header_line=False
                file_column_names=line
            else:
                data_line_count+=1
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
                            pass

                        if column_data == 'null' or column_data == 'NULL':
                            valid_data=False

                        #print ('column_name', column_name)
                        if company_import_col_types[company_import_col_names.index(column_name)] == 'int' and is_int == False:
                            #print( 'was expecting integer, found non-integer', 'column_name', column_name, 'column_data', column_data, 'line', line, 'file_column_names', file_column_names )
                            valid_data=False

                        if column_name == 'zip' and is_int == False:
                            column_data = zip_to_int(column_data)

                        if column_data and is_int == False:
                            column_data = column_data.lower()

                        if valid_data:
                            company_import_col_names.index(column_name)
                            if column_name == 'industry_sic_code' and len(str(column_data))>4:
                                raise Exception('wtf ' + str(column_name) + ' ' + sqlcmd + ' ' + str(data_line_count) + ' ' + str(column_index) + ' ' + filename + ' ' + str(line) + str(column_data) + ' WWW' + line[column_index] + ' www1 ' + column_data + ' file_column_names ' + str(file_column_names))

                            #print ('WTF', 'column_name', column_name, column_data)
                            
                            sqldata[company_import_col_names.index(column_name)]=column_data
                        else:
                            break
                            #print ('WTF2', 'column_name', column_name, column_data)

                #print sqldata
                # if sqldata[0] not in seen_ids:
                #     seen_ids.append(sqldata[0])
                #     if None not in sqldata:
                # print('\n')
                # print('file_column_names', file_column_names)
                # print('line',line)
                # print('sqldata',sqldata)

                # if exitcount == 0:
                #      sys.exit(1)
                # exitcount-=1

                try:
                    if valid_data:
                        cur.execute(sqlcmd, sqldata)
                except Exception as e:
                    print('line', line)
                    print('file_column_names', file_column_names)
                    print(sqlcmd, sqldata)
                    raise e

                    #else:
                    #    print 'Do not insert data with None: ' + str(sqldata)
                #else:
                #    print 'duplicate id found: ' + str(sqldata)
conn.commit()
cur.close()
conn.close()

