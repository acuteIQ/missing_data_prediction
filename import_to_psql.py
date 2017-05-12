import psycopg2
import os
import csv

DATA_DIR='../data/data_export_ck'
DATA_FILE_PREFIX='tbl_company'
conn=psycopg2.connect('dbname=acuteiq')
cur=conn.cursor()

company_import_col_names=['id', 'zip', 'industry_sic_code', 'number_of_employees', 'yearly_sales']
data_line_count=0
seen_ids=[]
for filename in os.listdir(DATA_DIR):
    if filename.startswith(DATA_FILE_PREFIX):
        csv_filehandle=open(os.path.join(DATA_DIR, filename))
        csvreader=csv.reader(csv_filehandle)
        header_line=True
        file_column_names=[]
        for line in csvreader:
            sqlcmd='INSERT INTO company2 (' + ','.join(company_import_col_names) + ') VALUES (%s, %s, %s, %s, %s)'
            sqldata=[None]*len(company_import_col_names)
            if header_line:
                header_line=False
                file_column_names=line
            else:
                data_line_count+=1
                for column_index, column_data in enumerate(line):
                    column_name=file_column_names[column_index]
                    if column_name in company_import_col_names:
                        valid_data=True
                        column_data_int=0
                        try:
                            column_data_int=int(column_data)
                            if column_data_int == 0:
                                valid_data=False
                        except:
                            pass

                        if column_data == 'null':
                            valid_data=False

                        if valid_data:
                            company_import_col_names.index(column_name)
                            if column_name == 'industry_sic_code' and len(str(column_data_int))>4:
                                raise Exception('wtf ' + str(column_name) + ' ' + sqlcmd + ' ' + str(data_line_count) + ' ' + str(column_index) + ' ' + filename + ' ' + str(line) + str(column_data_int) + ' WWW' + line[column_index] + ' www1 ' + column_data + ' www2 ' + str(column_data_int) + ' file_column_names ' + str(file_column_names))
                            
                            sqldata[company_import_col_names.index(column_name)]=column_data_int

                #print sqldata
                # if sqldata[0] not in seen_ids:
                #     seen_ids.append(sqldata[0])
                #     if None not in sqldata:
                cur.execute(sqlcmd, sqldata)
                    #else:
                    #    print 'Do not insert data with None: ' + str(sqldata)
                #else:
                #    print 'duplicate id found: ' + str(sqldata)
conn.commit()
cur.close()
conn.close()

