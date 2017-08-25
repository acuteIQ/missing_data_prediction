gtp(X_hat, A, B);

nnz_ind = yearly_sales_X.data > 0.1;

N = numel(X_hat.data(nnz_ind));
rmse=sqrt( sum(sum( (yearly_sales_X.data(nnz_ind) - X_hat.data(nnz_ind)).^2 ))/ N )

'mean'
mean( X_hat.data(nnz_ind) )

'std dev'
std( X_hat.data(nnz_ind) )