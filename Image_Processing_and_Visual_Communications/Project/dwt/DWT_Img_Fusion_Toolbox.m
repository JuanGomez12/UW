% Based on the code made by Mathworks for its Image Fusion Toolbox, found in https://www.mathworks.com/help/wavelet/gs/image-fusion.html
%clear all;

% Read MRI image and convert it to RGB format %
[A,map] = imread("MRI.gif",1); 
A_RGB = ind2rgb(A,map);

A_Red = (A_RGB(:,:,1));
A_Green = (A_RGB(:,:,2));
A_Blue = (A_RGB(:,:,3));

% Read SPECT image and convert it to RGB format %
[B,map] = imread("SPECT.gif",1);
B_RGB = ind2rgb(B,map);

B_Red = (B_RGB(:,:,1));
B_Green = (B_RGB(:,:,2));
B_Blue = (B_RGB(:,:,3));


XFUSmean_R = wfusimg(A_Red,B_Red,'db2',1,'mean','mean');
XFUSmean_G = wfusimg(A_Green,B_Green,'db2',1,'mean','mean');
XFUSmean_B = wfusimg(A_Blue,B_Blue,'db2',1,'mean','mean');

XFUSmaxmin_R = wfusimg(A_Red,B_Red,'db2',1,'max','min');
XFUSmaxmin_G = wfusimg(A_Green,B_Green,'db2',1,'max','min');
XFUSmaxmin_B = wfusimg(A_Blue,B_Blue,'db2',1,'max','min');

% Concatenate RGB channels
XFUSmean = cat(3,XFUSmean_R,XFUSmean_G,XFUSmean_B);
XFUSmaxmin = cat(3,XFUSmaxmin_R,XFUSmaxmin_G,XFUSmaxmin_B);

%colormap(map);
subplot(221), image(A_RGB), axis square, title('Mask')
subplot(222), image(B_RGB), axis square, title('Bust')
subplot(223), image(XFUSmean), axis square, 
title('Synthesized image, mean-mean')
subplot(224), image(XFUSmaxmin), axis square, 
title('Synthesized image, max-min')
