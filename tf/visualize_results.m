close all

nnz_ind=logical(credit_score_X.data > 0.1);
%plot(credit_score_X.data(nnz_ind));

hist( credit_score_X.data(nnz_ind) );
title('target');
xlabel('credit\_score');
ylabel('count');
figure
global TFT_Tensors
hist( TFT_Tensors{4}.data(nnz_ind) );
title('prediction');
xlabel('credit\_score');
ylabel('count');

'RMSE'
sqrt(mean((TFT_Tensors{4}.data(nnz_ind) -credit_score_X.data(nnz_ind)).^2))