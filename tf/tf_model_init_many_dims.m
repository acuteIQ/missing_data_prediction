%SQL DATA EXTRACT
% \copy (SELECT industry_sic_code, state, credit_score, number_of_employees FROM company_tf_observation_orig WHERE industry_sic_code IS NOT NULL AND state IS NOT NULL AND credit_scoe IS NOT NULL and number_of_employees is not null ) TO '/tmp/industry_sic_code_state_number_of_employees_credit_score_NON_NULL.csv'  DELIMITER ',' CSV HEADER;

conn = get_conn();

%sql_data = csvread('data/industry_sic_code_state_credit_score_NON_NULL.csv', 1, 0);
sql_data = csvread('data/industry_sic_code_state_number_of_employees_business_risk_credit_score_NON_NULL.csv', 1, 0);

% suffle input
sql_data=sql_data(randperm(end), : );

industry_sic_code_data = sql_data(:,1);
state_data = sql_data(:,2);
credit_score_data = sql_data(:,3);
number_of_employees_data = sql_data(:,4)+1; % python -> matlab offset
business_risk_data = sql_data(:,5);

distinct_isc = get_single_sql_result(conn, 'SELECT count(distinct(industry_sic_code)) FROM company_tf_observation_orig WHERE industry_sic_code is not NULL');
isc_range = 1:distinct_isc;
isc_sorted = table2array(select(conn, 'SELECT distinct(industry_sic_code) FROM company_tf_observation_orig WHERE industry_sic_code is not null order by industry_sic_code;'));
for isc_index = isc_range
    industry_sic_code_data( industry_sic_code_data == isc_sorted(isc_index) ) = isc_index;
end

industry_sic_code_index = Index(max(industry_sic_code_data));
%state_index = Index(max(state_data));

%industry_sic_code_index = Index(get_single_sql_result(conn, 'SELECT max(industry_sic_code) FROM company_tf_observation_orig'));

state_index = Index(get_single_sql_result(conn, 'SELECT max(state) FROM company_tf_observation_orig'));

%state_index = Index(get_single_sql_result(conn, 'SELECT max(state) FROM company_tf_observation_orig'));

%county_index = Index(get_single_sql_result(conn, ...
%    'SELECT max(county) FROM company_tf_observation_orig'));

number_of_employees_index = Index(get_single_sql_result(conn, 'SELECT max(number_of_employees) FROM company_tf_observation_orig')+1);

%credit_score_index = Index(get_single_sql_result(conn, ...
%    'SELECT max(credit_score) FROM company_tf_observation_orig'));

business_risk_index = Index(get_single_sql_result(conn, 'SELECT max(business_risk) FROM company_tf_observation_orig'));

topic_index = Index(20);

% sql_cmd = [ 'SELECT ' ...
%             ' industry_sic_code, state, ' ...
%             ' credit_score '...
%             ' FROM company_tf_observation_orig ' ...
%             ' WHERE ' ...
%             ' industry_sic_code IS NOT NULL AND ' ...
%             ' state IS NOT NULL AND ' ...
%             ' credit_score IS NOT NULL ' ...
%             ' order by id LIMIT 50000  ' ];
% offset -> process other parts

%sql_data = select(conn, sql_cmd);

% IMPORTANT: number_of_employees, credit_score are 0 indexed on db
%            MATLAB should pre/post filter results as 1 indexed

X = Tensor(industry_sic_code_index, state_index, number_of_employees_index, business_risk_index);
X.data = ones(...
    industry_sic_code_index.cardinality, ...
    state_index.cardinality, ...
    number_of_employees_index.cardinality, ...
    business_risk_index.cardinality ...
    )*eps*1000;

for r_ind = 1:size(sql_data,1)
    X.data( industry_sic_code_data(r_ind), state_data(r_ind), number_of_employees_data(r_ind), business_risk_data(r_ind) ) = credit_score_data(r_ind);
end

A = Tensor(industry_sic_code_index, topic_index);
B = Tensor(state_index, topic_index);
C = Tensor(number_of_employees_index, topic_index);
D = Tensor(business_risk_index, topic_index);

A.data = rand(industry_sic_code_index.cardinality, topic_index.cardinality);
B.data = rand(state_index.cardinality, topic_index.cardinality);
C.data = rand(number_of_employees_index.cardinality, topic_index.cardinality);
D.data = rand(business_risk_index.cardinality, topic_index.cardinality);