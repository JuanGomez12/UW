% Read MRI image and convert it to RGB format %
[A,map] = imread("MRI.gif",1); 
A_RGB = ind2rgb(A,map);

% Read SPECT image and convert it to RGB format %
[B,map] = imread("SPECT.gif",1);
B_RGB =ind2rgb(B,map);

w=[0.5 0.5 0.5 0.5 0.5 0.5 0.5 0.5];

%% Swarm based optimization
x = particleswarm(dwt_ifpm_function(A_RGB, B_RGB, w1, w2, w3, w4, w5, w6, w7, w8), 8);
%% Optimization through optimproblem (Problem based optimization)
% w1 = optimvar('w1');
% w2 = optimvar('w2');
% w3 = optimvar('w3');
% w4 = optimvar('w4');
% w5 = optimvar('w5');
% w6 = optimvar('w6');
% w7 = optimvar('w7');
% w8 = optimvar('w8');
% 
% prob = optimproblem('ObjectiveSense', 'max');
% prob.Objective = dwt_ifpm_function(A_RGB, B_RGB, w1, w2, w3, w4, w5, w6, w7, w8);
% solve(prob)

%% Show image

% img = dwt_Fusion(A_RGB, B_RGB, w(1), w(2), w(3), w(4), w(5), w(6), w(7), w(8));
% ifpm = dwt_ifpm_function(A_RGB, B_RGB, w(1), w(2), w(3), w(4), w(5), w(6), w(7), w(8));
% imshow(img)

