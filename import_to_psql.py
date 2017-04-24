import psycopg2
import os
import csv

DATA_DIR='../data/data_export_ck'
DATA_FILE_PREFIX='tbl_company'
conn=psycopg2.connect('dbname=acuteiq')
cur=conn.cursor()

company_import_col_names=['id', 'zip', 'industry_sic_code', 'number_of_employees', 'yearly_sales']
all_column_names=[]
first_line=True
data_line_count=0
seen_ids=[]
for filename in os.listdir(DATA_DIR):
    if filename.startswith(DATA_FILE_PREFIX):
        csv_filehandle=open(os.path.join(DATA_DIR, filename))
        csvreader=csv.reader(csv_filehandle)
        for line in csvreader:
            sqlcmd='INSERT INTO company (' + ','.join(company_import_col_names) + ') VALUES (%s, %s, %s, %s, %s)'
            sqldata=[None]*len(company_import_col_names)
            if first_line: # skip first line of each file
                first_line=False
                all_column_names=line
                for ccn in company_import_col_names:
                    if ccn not in all_column_names:
                        raise Exception('Required company_import_col_names ' + str(ccn) + ' not found in all_column_names: ' + str(all_column_names))
            else:
                data_line_count+=1
                for column_index, column_data in enumerate(line):
                    column_name=all_column_names[column_index]
                    if column_name in company_import_col_names:
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
                            company_import_col_names.index(column_name)
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

