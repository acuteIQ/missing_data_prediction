
conn = get_conn();

industry_sic_code_index = Index(get_single_sql_result(conn, 'SELECT max(industry_sic_code) FROM company_tf_observation'));

state_index = Index(get_single_sql_result(conn, 'SELECT max(state) FROM company_tf_observation'));

%state_index = Index(get_single_sql_result(conn, 'SELECT max(state) FROM company_tf_observation'));

%county_index = Index(get_single_sql_result(conn, ...
%    'SELECT max(county) FROM company_tf_observation'));

%number_of_employees_index = Index(get_single_sql_result(conn, ...
%    'SELECT max(number_of_employees) FROM company_tf_observation'));

%credit_score_index = Index(get_single_sql_result(conn, ...
%    'SELECT max(credit_score) FROM company_tf_observation'));

%business_risk_index = Index(get_single_sql_result(conn, ...
%    'SELECT max(business_risk) FROM company_tf_observation'));

topic_index = Index(10);

sql_cmd = [ 'SELECT ' ...
            ' industry_sic_code, state, ' ...
            ' credit_score '...
            ' FROM company_tf_observation ' ...
            ' WHERE ' ...
            ' industry_sic_code IS NOT NULL AND ' ...
            ' state IS NOT NULL AND ' ...
            ' credit_score IS NOT NULL order by id ' ]; % ...
                                                        %' order by id limit 50000 offset 150000 ' ];
                                            %' order by id LIMIT 10000  ' ];
% offset -> process other parts

sql_data = select(conn, sql_cmd);

% IMPORTANT: number_of_employees, credit_score are 0 indexed on db
%            MATLAB should pre/post filter results as 1 indexed

X = Tensor(industry_sic_code_index, state_index); %, state_index); %, county_index);
% yearly sales model
X.data = ones(...
    industry_sic_code_index.cardinality, ...
    state_index.cardinality ...
    )*eps*1000;

%X_hat = Tensor(industry_sic_code_index, state_index); % used for prediction
%X_hat.data = ones(industry_sic_code_index.cardinality, ...
%                   state_index.cardinality ...
%                   )*eps*1000; 

for r_ind = 1:size(sql_data,1)
    %if isnan(sql_data{r_ind, end}) == 0
    isc = sql_data{r_ind, {'industry_sic_code'}};
    state = sql_data{r_ind, {'state'}};

    if X.data( isc, state) < 0.1
        X.data( isc, state ) = sql_data{r_ind, {'credit_score'}};
    else
        X.data( isc, state ) = (X.data( isc, state ) + sql_data{r_ind, {'credit_score'}})/2;
    end
    %end
end

A = Tensor(industry_sic_code_index, topic_index);
B = Tensor(state_index, topic_index);

A.data = rand(industry_sic_code_index.cardinality, topic_index.cardinality);
B.data = rand(state_index.cardinality, topic_index.cardinality);
