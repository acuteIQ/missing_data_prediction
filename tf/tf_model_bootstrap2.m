clear all;
cd /home/can/projeler/tft
setup_tft
cd /home/can/projeler/upwork/acuteiq/code/
addpath tf
addpath utils

conn = get_conn();

industry_sic_code_index = Index(get_single_sql_result(conn, 'SELECT max(industry_sic_code) FROM company_tf_observation_orig'));

state_index = Index(get_single_sql_result(conn, 'SELECT max(state) FROM company_tf_observation_orig'));

topic_index = Index(10);

load('../data/industry_sic_code_state_credit_score_NOT_NULL.mat');

X = Tensor(industry_sic_code_index, state_index);
A = Tensor(industry_sic_code_index, topic_index);
B = Tensor(state_index, topic_index);

% random initialize
A.data = rand(industry_sic_code_index.cardinality, topic_index.cardinality);
B.data = rand(state_index.cardinality, topic_index.cardinality);

pre_process();

p = [1];
phi = [1];

data_len = size(sql_data,1);
step_percentage = 2;
testing_percentage = 10;

train_data_len = floor(data_len*((100-testing_percentage)/100));
step_size = floor(train_data_len * (step_percentage / 100));

X_data_indices = ''
for tfiind = 1:length(tft_indices)
    found = false;
    for X_indices_ind = 1:length(X.indices)
        if X.indices{X_indices_ind}.id == tft_indices(tfiind).id
            found = true;
            break
        end
    end
    if found
        X_data_indices = [ X_data_indices ' : ' ];
    else
        X_data_indices = [ X_data_indices ' 1 ' ];
    end
    if tfiind ~= length(tft_indices)
        X_data_indices = [ X_data_indices ',' ];
    end
end

for range_index = 1:floor(train_data_len/step_size)
    range_start = floor((range_index-1)*step_size)+1;
    if range_index == floor(train_data_len/step_size)
        range_end = train_data_len;
    else
        range_end = range_start + step_size -1;
    end

    display( ['range: ' num2str(range_start) char(9) num2str(range_end) char(9) num2str(range_end-range_start) ] );

    display('initializing X')
    eval([ 'X.data(' X_data_indices ') = ones( industry_sic_code_index.cardinality, state_index.cardinality )*eps*1000;' ]);

    display('populating X')
    for r_ind = range_start:range_end
        X.data( ...
            sql_data{r_ind, {'industry_sic_code'}}, ...
            sql_data{r_ind, {'state'}} ...
            ) = sql_data{r_ind, {'credit_score'}}; % the indices order works with this configuration only!
    end

    display('calling tf')
    factorization_model = {X, {A, B}};

    model = TFModel(factorization_model, p, phi);
    config = TFEngineConfig(model, 10);
    engine = TFDefaultEngine(config, 'gtp_mex');
    engine.factorize();
    plot(engine.beta_divergence');
    figure()
    check_divergence(engine.beta_divergence);

    visualize_results()
    pause
end