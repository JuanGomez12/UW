function [ifpm, fused_img] = DWT_img_fusion_AVG(img1, img2, coeff1, coeff2)
%Perform an image fusion using two images as input and a pair of
%coefficients for the LL subband.


% Perform Single-Level Discrete wavelet decomposition on RGB channels of MRI image %  
img1_Red = (img1(:,:,1));
img1_Green = (img1(:,:,2));
img1_Blue = (img1(:,:,3));

% Perform Single-Level Discrete wavelet decomposition on RGB channels of SPECT image % 
img2_Red = (img2(:,:,1));
img2_Green = (img2(:,:,2));
img2_Blue = (img2(:,:,3));


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
LL_F = (coeff1 * LL_img1 + coeff2 * LL_img2);
LH_F = (coeff1 * LH_img1 + coeff2 * LH_img2);
HL_F = (coeff1 * HL_img1 + coeff2 * HL_img2);
HH_F = (coeff1 * HH_img1 + coeff2 * HH_img2);

% Perform Inverse Discrete Wavelet Transform on RGB channels %
fused_img_Red = idwt2(LL_F(:,:,1), LH_F(:,:,1), HL_F(:,:,1), HH_F(:,:,1),'db2');
fused_img_Green = idwt2(LL_F(:,:,2), LH_F(:,:,2), HL_F(:,:,2), HH_F(:,:,2),'db2');
fused_img_Blue = idwt2(LL_F(:,:,3), LH_F(:,:,3), HL_F(:,:,3), HH_F(:,:,3),'db2');

% Concatenate RGB channels
fused_img = cat(3,fused_img_Red,fused_img_Green,fused_img_Blue);

%Calculate the IFPM
ifpm = IFPM(im2uint8(img1), im2uint8(img2), im2uint8(fused_img));
end
