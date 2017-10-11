close all

nnz_ind=logical(X.data > 0.1);
%plot(X.data(nnz_ind));

hist( X.data(nnz_ind) );
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
sqrt(mean((TFT_Tensors{4}.data(nnz_ind) - X.data(nnz_ind)).^2))