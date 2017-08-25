clear all;
cd /home/can/projeler/tft
setup_tft
cd /home/can/projeler/upwork/acuteiq/code/
addpath tf
addpath utils

tf_model_init();

pre_process();

p = [1];
phi = [1];

factorization_model = {yearly_sales_X, {A, B}};

model = TFModel(factorization_model, p, phi);
config = TFEngineConfig(model, 10);
engine = TFDefaultEngine(config, 'gtp');
engine.factorize();
plot(engine.beta_divergence');
check_divergence(engine.beta_divergence);