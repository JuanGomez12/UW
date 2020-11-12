
% Read input images %
[A,map] = imread("MRI.gif",1); 
X1 = im2uint8(ind2rgb(A,map));

[B,map] = imread("SPECT.gif",1); 
X2 = im2uint8(ind2rgb(round(B),map));

% Average fusion example %
Y = im2uint8(0.5*(X1 + X2));

% Compute IFPM %
ifpm = IFPM(X1,X2,Y);