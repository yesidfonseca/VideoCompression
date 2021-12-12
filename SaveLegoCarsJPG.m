clear all
close all hidden
load LegoCars.mat
x = rescale(hyperimg,0,1);
x = x*255;
x = uint8(x);
x = x(:,:,[8,4,2]+1);
imwrite(x,'LegoCars.jpg');

x_ = imread('LegoCars.jpg');


fun_PSNR(rescale(single(x)),rescale(single(x_)))

err = power(sum(power(x_-x,2),3),.5)./power(sum(power(x,2),3),.5);

figure, imagesc(err), colormap('hot'), axis equal

figure, imshow(x)
figure, imshow(x_)