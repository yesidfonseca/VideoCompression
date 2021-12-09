function psnr = fun_PSNR(img,res)

[M,N,L]=size(img);
temp = 1./(M*N*L)*sum(power(img(:)-res(:),2));
psnr = 10*log10(max(power(img(:),2)/temp));
