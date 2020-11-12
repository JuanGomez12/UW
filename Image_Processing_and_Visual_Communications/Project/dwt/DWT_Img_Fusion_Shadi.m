close all
clear
clc

% Read MRI image and convert it to RGB format %
[img1,map] = imread("MRI.gif",1); 
img1_RGB = ind2rgb(img1,map);

% Read SPECT image and convert it to RGB format %
[img2,map] = imread("SPECT.gif",1);
img2_RGB = ind2rgb(img2,map);

% Perform Single-Level Discrete wavelet decomposition on RGB channels of MRI image %  
img1_Red = (img1_RGB(:,:,1));
img1_Green = (img1_RGB(:,:,2));
img1_Blue = (img1_RGB(:,:,3));

% Perform Single-Level Discrete wavelet decomposition on RGB channels of SPECT image % 
img2_Red = (img2_RGB(:,:,1));
img2_Green = (img2_RGB(:,:,2));
img2_Blue = (img2_RGB(:,:,3));

% Concatenate RGB channels
img1 = cat(3, img1_Red, img1_Green, img1_Blue);
img2 = cat(3, img2_Red, img2_Green, img2_Blue);

% Extract LL (Approximations, A), LH(Horizontal,H), HL (Vertical, V), and HH(Diagonal, D) frequency sub-bands %
[img1_A_R, img1_H_R, img1_V_R, img1_D_R] = dwt2(img1_Red, 'db2');
[img1_A_G, img1_H_G, img1_V_G, img1_D_G] = dwt2(img1_Green, 'db2');
[img1_A_B, img1_H_B, img1_V_B, img1_D_B] = dwt2(img1_Blue, 'db2');

[img2_A_R, img2_H_R, img2_V_R, img2_D_R] = dwt2(img2_Red, 'db2');
[img2_A_G, img2_H_G, img2_V_G, img2_D_G] = dwt2(img2_Green, 'db2');
[img2_A_B, img2_H_B, img2_V_B, img2_D_B] = dwt2(img2_Blue, 'db2');

LL_img1 = cat(3,img1_A_R, img1_A_G, img1_A_B);
LH_img1 = cat(3,img1_H_R, img1_H_G, img1_H_B);
HL_img1 = cat(3,img1_V_R, img1_V_G, img1_V_B);
HH_img1 = cat(3,img1_D_R, img1_D_G, img1_D_B);

LL_img2 = cat(3,img2_A_R, img2_A_G, img2_A_B);
LH_img2 = cat(3,img2_H_R, img2_H_G, img2_H_B);
HL_img2 = cat(3,img2_V_R, img2_V_G, img2_V_B);
HH_img2 = cat(3,img2_D_R, img2_D_G, img2_D_B);

% Average fusion of LL sub-band %
LL_F = 0.5*(LL_img1+LL_img2);

% Fusion based on salience measure for high frequency sub-bands (suggested by: HAI-HUI WANG)
LH_F = zeros(size(LH_img1,1),size(LH_img1,2),3);
LH_img1 = padarray(LH_img1,[1 1],0,'both');
LH_img2 = padarray(LH_img2,[1 1],0,'both');

for k=1:3
    for i=2:size(LH_img1,1)-1
        for j=2:size(LH_img1,2)-1
            S_img1 = LH_img1(i,j,k)+LH_img1(i-1,j-1,k)+LH_img1(i-1,j,k)+LH_img1(i-1,j+1,k)+LH_img1(i,j-1,k)+LH_img1(i,j+1,k)+LH_img1(i+1,j-1,k)+LH_img1(i+1,j,k)+LH_img1(i+1,j+1,k);
            S_img1 = S_img1*(LH_img1(i,j,k))^2;

            S_img2 = LH_img2(i,j,k)+LH_img2(i-1,j-1,k)+LH_img2(i-1,j,k)+LH_img2(i-1,j+1,k)+LH_img2(i,j-1,k)+LH_img2(i,j+1,k)+LH_img2(i+1,j-1,k)+LH_img2(i+1,j,k)+LH_img2(i+1,j+1,k);
            S_img2 = S_img2*(LH_img2(i,j,k))^2;

            if(S_img1 > S_img2)
                LH_F(i-1,j-1,k) = LH_img1(i,j,k);
            else
                LH_F(i-1,j-1,k) = LH_img2(i,j,k);
            end
        end
    end
end

HL_F = zeros(size(HL_img1,1),size(HL_img1,2),3);
HL_img1 = padarray(HL_img1,[1 1],0,'both');
HL_img2 = padarray(HL_img2,[1 1],0,'both');

for k=1:3
    for i=2:size(HL_img1,1)-1
        for j=2:size(HL_img1,2)-1
            S_img1 = HL_img1(i,j,k)+HL_img1(i-1,j-1,k)+HL_img1(i-1,j,k)+HL_img1(i-1,j+1,k)+HL_img1(i,j-1,k)+HL_img1(i,j+1,k)+HL_img1(i+1,j-1,k)+HL_img1(i+1,j,k)+HL_img1(i+1,j+1,k);
            S_img1 = S_img1*(HL_img1(i,j,k))^2;

            S_img2 = HL_img2(i,j,k)+HL_img2(i-1,j-1,k)+HL_img2(i-1,j,k)+HL_img2(i-1,j+1,k)+HL_img2(i,j-1,k)+HL_img2(i,j+1,k)+HL_img2(i+1,j-1,k)+HL_img2(i+1,j,k)+HL_img2(i+1,j+1,k);
            S_img2 = S_img2*(HL_img2(i,j,k))^2;

            if(S_img1 > S_img2)
                HL_F(i-1,j-1,k) = HL_img1(i,j,k);
            else
                HL_F(i-1,j-1,k) = HL_img2(i,j,k);
            end
        end
    end
end

HH_F = zeros(size(HH_img1,1),size(HH_img1,2),3);
HH_img1 = padarray(HH_img1,[1 1],0,'both');
HH_img2 = padarray(HH_img2,[1 1],0,'both');

for k=1:3
    for i=2:size(HH_img1,1)-1
        for j=2:size(HH_img1,2)-1
            S_img1 = HH_img1(i,j,k)+HH_img1(i-1,j-1,k)+HH_img1(i-1,j,k)+HH_img1(i-1,j+1,k)+HH_img1(i,j-1,k)+HH_img1(i,j+1,k)+HH_img1(i+1,j-1,k)+HH_img1(i+1,j,k)+HH_img1(i+1,j+1,k);
            S_img1 = S_img1*(HH_img1(i,j,k))^2;

            S_img2 = HH_img2(i,j,k)+HH_img2(i-1,j-1,k)+HH_img2(i-1,j,k)+HH_img2(i-1,j+1,k)+HH_img2(i,j-1,k)+HH_img2(i,j+1,k)+HH_img2(i+1,j-1,k)+HH_img2(i+1,j,k)+HH_img2(i+1,j+1,k);
            S_img2 = S_img2*(HH_img2(i,j,k))^2;

            if(S_img1 > S_img2)
                HH_F(i-1,j-1,k) = HH_img1(i,j,k);
            else
                HH_F(i-1,j-1,k) = HH_img2(i,j,k);
            end
        end
    end
end


% Perform Inverse Discrete Wavelet Transform on RGB channels %
fused_img_Red = idwt2(LL_F(:,:,1), LH_F(:,:,1), HL_F(:,:,1), HH_F(:,:,1),'db2');
fused_img_Green = idwt2(LL_F(:,:,2), LH_F(:,:,2), HL_F(:,:,2), HH_F(:,:,2),'db2');
fused_img_Blue = idwt2(LL_F(:,:,3), LH_F(:,:,3), HL_F(:,:,3), HH_F(:,:,3),'db2');

% Concatenate RGB channels
fused_img = cat(3,fused_img_Red,fused_img_Green,fused_img_Blue);
figure(3);
imshow(fused_img);
