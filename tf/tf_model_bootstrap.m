clear all;
cd /home/can/projeler/tft
setup_tft
cd /home/can/projeler/upwork/acuteiq/code/
addpath tf
addpath utils

conn = get_conn();

sql_data = csvread('data/industry_sic_code_state_NON_NULL.csv', 1, 0);

% suffle input
% sql_data=sql_data(randperm(end), : );

industry_sic_code_data = sql_data(:,1);
state_data = sql_data(:,2);
credit_score_data = sql_data(:,3);

% distinct_isc = get_single_sql_result(conn, 'SELECT count(distinct(industry_sic_code)) FROM company_tf_observation_orig');
% isc_range = 1:distinct_isc;
% isc_sorted = table2array(select(conn, 'SELECT distinct(industry_sic_code) FROM company_tf_observation_orig order by industry_sic_code;'));
% for isc_index = isc_range
%     industry_sic_code_data( industry_sic_code_data == isc_sorted(isc_index) ) = isc_index;
% end
%industry_sic_code_index = Index(max(industry_sic_code_data));

industry_sic_code_index = Index(get_single_sql_result(conn, 'SELECT max(industry_sic_code) FROM company_tf_observation_orig'));
state_index = Index(get_single_sql_result(conn, 'SELECT max(state) FROM company_tf_observation_orig'));
topic_index = Index(10);

X = Tensor(industry_sic_code_index, state_index);
X.data = ones(...
    industry_sic_code_index.cardinality, ...
    state_index.cardinality ...
    )*eps*1000;

for r_ind = 1:50000 %size(sql_data,1)
    X.data( industry_sic_code_data(r_ind), state_data(r_ind) ) = credit_score_data(r_ind);
end

A = Tensor(industry_sic_code_index, topic_index);
B = Tensor(state_index, topic_index);

A.data = rand(industry_sic_code_index.cardinality, topic_index.cardinality);
B.data = rand(state_index.cardinality, topic_index.cardinality);

pre_process();

p = [1];
phi = [1];

factorization_model = {X, {A, B}};

model = TFModel(factorization_model, p, phi);
config = TFEngineConfig(model, 10);
engine = TFDefaultEngine(config, 'gtp_mex');
engine.factorize();
plot(engine.beta_divergence');
check_divergence(engine.beta_divergence);