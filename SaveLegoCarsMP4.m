clear all
close all hidden
load LegoCars.mat
x = rescale(hyperimg,0,1);
x = x*255;
x = uint8(x);
v = VideoWriter('LegoCars.mp4','MPEG-4');
v.Quality = 100;
open(v)
writeVideo(v,reshape(x,256,256,1,10))
close(v)

vidObj = VideoReader('LegoCars.mp4');
x_ = read(vidObj,[1 10]);
x_ = reshape(x_(:,:,1,:),256,256,10);


fun_PSNR(rescale(single(x)),rescale(single(x_)))

err = power(sum(power(x_-x,2),3),.5)./power(sum(power(x,2),3),.5);

figure, imagesc(err), colormap('hot'), axis equal

figure, imshow(x(:,:,[8,4,2]+1))
figure, imshow(x_(:,:,[8,4,2]+1))