function [conn] = get_conn()
    datasource = 'acuteiq';
    username = 'can';
    password = 'tam1tam';
    driver = 'org.postgresql.Driver';
    url = 'jdbc:postgresql://localhost:5432/acuteiq';

    conn = database(datasource,username,password,driver,url);
end
