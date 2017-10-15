close all

nnz_ind=logical(X.data > 0.1);
%plot(X.data(nnz_ind));

figure()
plot( min(X.data(nnz_ind)):(max(X.data(nnz_ind))-min(X.data(nnz_ind)))/9:max(X.data(nnz_ind)), flip(cumsum(flip(hist( X.data(nnz_ind) ) ) ) ) );
title('Credit Score (matlab)');
xlabel('credit score');
ylabel('reverse cumulative distribution');

figure()
hist( X.data(nnz_ind) );
title('target');
xlabel('credit\_score');
ylabel('count');

global TFT_Tensors

figure()
plot( min(TFT_Tensors{4}.data(nnz_ind)):(max(TFT_Tensors{4}.data(nnz_ind))-min(TFT_Tensors{4}.data(nnz_ind)))/9:max(TFT_Tensors{4}.data(nnz_ind)), flip(cumsum(flip(hist( TFT_Tensors{4}.data(nnz_ind) )))));
title('Credit Score (training set prediction)');
xlabel('credit score');
ylabel('reverse cumulative distribution');

figure()
hist( TFT_Tensors{4}.data(nnz_ind) );
title('prediction');
xlabel('credit\_score');
ylabel('count');


'RMSE'
sqrt(mean((TFT_Tensors{4}.data(nnz_ind) - X.data(nnz_ind)).^2))