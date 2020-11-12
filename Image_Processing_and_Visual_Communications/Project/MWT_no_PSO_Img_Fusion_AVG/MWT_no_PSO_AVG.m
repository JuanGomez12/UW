function [ifpm, fused_img] = MWT_no_PSO_AVG(A_RGB, B_RGB, coeff1, coeff2)

% Perform Single-Level 2D Multiwavelet decomposition on RGB channels of MRI image %  
X_Red = GHM(A_RGB(:,:,1));
X_Green = GHM(A_RGB(:,:,2));
X_Blue = GHM(A_RGB(:,:,3));

% Perform Single-Level 2D Multiwavelet decomposition on RGB channels of SPECT image % 
Y_Red = GHM(B_RGB(:,:,1));
Y_Green = GHM(B_RGB(:,:,2));
Y_Blue = GHM(B_RGB(:,:,3));

% Concatenate RGB channels
X = cat(3,X_Red,X_Green,X_Blue);
Y = cat(3,Y_Red,Y_Green,Y_Blue);

% Plot LL, LH, HL, and HH frequency sub-bands %
% figure(1);
% imshow(X);
% figure(2);
% imshow(Y);

% Extract LL, LH, HL, and HH frequency sub-bands %
[N_A,M_A]=size(A_RGB(:,:,1));
[N_B,M_B]=size(B_RGB(:,:,1));

LL_LL_X = X(1:N_A/2, 1:N_A/2, :);
LL_LH_X = X(1:N_A/2, N_A/2+1:N_A, :);
LL_HL_X = X(N_A/2+1:N_A, 1:N_A/2, :);
LL_HH_X = X(N_A/2+1:N_A, N_A/2+1:N_A, :);
LH_X = X(1:N_A, N_A+1:2*N_A, :);
HL_X = X(N_A+1:2*N_A, 1:N_A, :);
HH_X = X(N_A+1:2*N_A, N_A+1:2*N_A, :);

LL_LL_Y = Y(1:N_B/2, 1:N_B/2, :);
LL_LH_Y = Y(1:N_B/2, N_B/2+1:N_B, :);
LL_HL_Y = Y(N_B/2+1:N_B, 1:N_B/2, :);
LL_HH_Y = Y(N_B/2+1:N_B, N_B/2+1:N_B, :);
LH_Y = Y(1:N_B, N_B+1:2*N_B, :);
HL_Y = Y(N_B+1:2*N_B, 1:N_B, :);
HH_Y = Y(N_B+1:2*N_B, N_B+1:2*N_B, :);

% Average fusion of LL sub-bands %
LL_LL_F = (coeff1 * LL_LL_X + coeff2 * LL_LL_Y);
LL_LH_F = (coeff1 * LL_LH_X + coeff2 * LL_LH_Y);
LL_HL_F = (coeff1 * LL_HL_X + coeff2 * LL_HL_Y);
LL_HH_F = (coeff1 * LL_HH_X + coeff2 * LL_HH_Y);

% Average fusion of high frequency sub-bands %
LH_F = (coeff1 * LH_X + coeff2 * LH_Y);
HL_F = (coeff1 * HL_X + coeff2 * HL_Y);
HH_F = (coeff1 * HH_X + coeff2 * HH_Y);

% % Fusion based on salience measure for high frequency sub-bands (suggested by: HAI-HUI WANG)
% LH_F = zeros(size(LH_X,1),size(LH_X,2),3);
% LH_X = padarray(LH_X,[1 1],0,'both');
% LH_Y = padarray(LH_Y,[1 1],0,'both');
% 
% for k=1:3
%     for i=2:size(LH_X,1)-1
%         for j=2:size(LH_X,2)-1
%             S_x = LH_X(i,j,k)+LH_X(i-1,j-1,k)+LH_X(i-1,j,k)+LH_X(i-1,j+1,k)+LH_X(i,j-1,k)+LH_X(i,j+1,k)+LH_X(i+1,j-1,k)+LH_X(i+1,j,k)+LH_X(i+1,j+1,k);
%             S_x = S_x*(LH_X(i,j,k))^2;
% 
%             S_y = LH_Y(i,j,k)+LH_Y(i-1,j-1,k)+LH_Y(i-1,j,k)+LH_Y(i-1,j+1,k)+LH_Y(i,j-1,k)+LH_Y(i,j+1,k)+LH_Y(i+1,j-1,k)+LH_Y(i+1,j,k)+LH_Y(i+1,j+1,k);
%             S_y = S_y*(LH_Y(i,j,k))^2;
% 
%             if(S_x > S_y)
%                 LH_F(i-1,j-1,k) = LH_X(i,j,k);
%             else
%                 LH_F(i-1,j-1,k) = LH_Y(i,j,k);
%             end
%         end
%     end
% end
% 
% HL_F = zeros(size(HL_X,1),size(HL_X,2),3);
% HL_X = padarray(HL_X,[1 1],0,'both');
% HL_Y = padarray(HL_Y,[1 1],0,'both');
% 
% for k=1:3
%     for i=2:size(HL_X,1)-1
%         for j=2:size(HL_X,2)-1
%             S_x = HL_X(i,j,k)+HL_X(i-1,j-1,k)+HL_X(i-1,j,k)+HL_X(i-1,j+1,k)+HL_X(i,j-1,k)+HL_X(i,j+1,k)+HL_X(i+1,j-1,k)+HL_X(i+1,j,k)+HL_X(i+1,j+1,k);
%             S_x = S_x*(HL_X(i,j,k))^2;
% 
%             S_y = HL_Y(i,j,k)+HL_Y(i-1,j-1,k)+HL_Y(i-1,j,k)+HL_Y(i-1,j+1,k)+HL_Y(i,j-1,k)+HL_Y(i,j+1,k)+HL_Y(i+1,j-1,k)+HL_Y(i+1,j,k)+HL_Y(i+1,j+1,k);
%             S_y = S_y*(HL_Y(i,j,k))^2;
% 
%             if(S_x > S_y)
%                 HL_F(i-1,j-1,k) = HL_X(i,j,k);
%             else
%                 HL_F(i-1,j-1,k) = HL_Y(i,j,k);
%             end
%         end
%     end
% end
% 
% HH_F = zeros(size(HH_X,1),size(HH_X,2),3);
% HH_X = padarray(HH_X,[1 1],0,'both');
% HH_Y = padarray(HH_Y,[1 1],0,'both');
% 
% for k=1:3
%     for i=2:size(HH_X,1)-1
%         for j=2:size(HH_X,2)-1
%             S_x = HH_X(i,j,k)+HH_X(i-1,j-1,k)+HH_X(i-1,j,k)+HH_X(i-1,j+1,k)+HH_X(i,j-1,k)+HH_X(i,j+1,k)+HH_X(i+1,j-1,k)+HH_X(i+1,j,k)+HH_X(i+1,j+1,k);
%             S_x = S_x*(HH_X(i,j,k))^2;
% 
%             S_y = HH_Y(i,j,k)+HH_Y(i-1,j-1,k)+HH_Y(i-1,j,k)+HH_Y(i-1,j+1,k)+HH_Y(i,j-1,k)+HH_Y(i,j+1,k)+HH_Y(i+1,j-1,k)+HH_Y(i+1,j,k)+HH_Y(i+1,j+1,k);
%             S_y = S_y*(HH_Y(i,j,k))^2;
% 
%             if(S_x > S_y)
%                 HH_F(i-1,j-1,k) = HH_X(i,j,k);
%             else
%                 HH_F(i-1,j-1,k) = HH_Y(i,j,k);
%             end
%         end
%     end
% end

% Concatenate resulting sub-bands %
LL_F = [LL_LL_F, LL_LH_F; LL_HL_F, LL_HH_F];
fused_img = [LL_F,LH_F;HL_F,HH_F];

% Perform Inverse Multiwavelet transform on RGB channels %
F_Red = IGHM(fused_img(:,:,1));
F_Green = IGHM(fused_img(:,:,2));
F_Blue = IGHM(fused_img(:,:,3));

% Concatenate RGB channels
fused_img = cat(3,F_Red,F_Green,F_Blue);


% Compute IFPM %
ifpm = IFPM(im2uint8(A_RGB), im2uint8(B_RGB), im2uint8(fused_img));
