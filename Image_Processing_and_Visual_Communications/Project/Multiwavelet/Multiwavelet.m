% Read MRI image and convert it to RGB format %
[x1,map] = imread("MRI.gif",1); 
x1_RGB = ind2rgb(x1,map);

% Read SPECT image and convert it to RGB format %
[x2,map] = imread("SPECT.gif",1);
x2_RGB = ind2rgb(x2,map);

% Perform Single-Level 2D Multiwavelet decomposition on RGB channels of MRI image %  
x1_Red = GHM(x1_RGB(:,:,1));
x1_Green = GHM(x1_RGB(:,:,2));
x1_Blue = GHM(x1_RGB(:,:,3));

% Perform Single-Level 2D Multiwavelet decomposition on RGB channels of SPECT image % 
x2_Red = GHM(x2_RGB(:,:,1));
x2_Green = GHM(x2_RGB(:,:,2));
x2_Blue = GHM(x2_RGB(:,:,3));

% Concatenate RGB channels
x1 = cat(3,x1_Red,x1_Green,x1_Blue);
x2 = cat(3,x2_Red,x2_Green,x2_Blue);

% Plot LL, LH, HL, and HH frequency sub-bands %
figure(1);
imshow(x1);
figure(2);
imshow(x2);

% Extract LL, LH, HL, and HH frequency sub-bands %
[N_x1,M_x1]=size(x1_RGB(:,:,1));
[N_x2,M_x2]=size(x2_RGB(:,:,1));

LL_x1 = x1(1:N_x1, 1:N_x1, :);
LH_x1 = x1(1:N_x1, N_x1+1:2*N_x1, :);
HL_x1 = x1(N_x1+1:2*N_x1, 1:N_x1, :);
HH_x1 = x1(N_x1+1:2*N_x1, N_x1+1:2*N_x1, :);

LL_x2 = x2(1:N_x2, 1:N_x2, :);
LH_x2 = x2(1:N_x2, N_x2+1:2*N_x2, :);
HL_x2 = x2(N_x2+1:2*N_x2, 1:N_x2, :);
HH_x2 = x2(N_x2+1:2*N_x2, N_x2+1:2*N_x2, :);

% Average fusion of LL sub-band %
LL_y = 0.5*(LL_x1+LL_x2);

% Fusion based on salience measure for high frequency sub-bands (suggested by: HAI-HUI WANG)
LH_y = zeros(size(LH_x1,1),size(LH_x1,2),3);
LH_x1 = padarray(LH_x1,[1 1],0,'both');
LH_x2 = padarray(LH_x2,[1 1],0,'both');

for k=1:3
    for i=2:size(LH_x1,1)-1
        for j=2:size(LH_x1,2)-1
            S_x = LH_x1(i,j,k)+LH_x1(i-1,j-1,k)+LH_x1(i-1,j,k)+LH_x1(i-1,j+1,k)+LH_x1(i,j-1,k)+LH_x1(i,j+1,k)+LH_x1(i+1,j-1,k)+LH_x1(i+1,j,k)+LH_x1(i+1,j+1,k);
            S_x = S_x*(LH_x1(i,j,k))^2;

            S_y = LH_x2(i,j,k)+LH_x2(i-1,j-1,k)+LH_x2(i-1,j,k)+LH_x2(i-1,j+1,k)+LH_x2(i,j-1,k)+LH_x2(i,j+1,k)+LH_x2(i+1,j-1,k)+LH_x2(i+1,j,k)+LH_x2(i+1,j+1,k);
            S_y = S_y*(LH_x2(i,j,k))^2;

            if(S_x > S_y)
                LH_y(i-1,j-1,k) = LH_x1(i,j,k);
            else
                LH_y(i-1,j-1,k) = LH_x2(i,j,k);
            end
        end
    end
end

HL_y = zeros(size(HL_x1,1),size(HL_x1,2),3);
HL_x1 = padarray(HL_x1,[1 1],0,'both');
HL_x2 = padarray(HL_x2,[1 1],0,'both');

for k=1:3
    for i=2:size(HL_x1,1)-1
        for j=2:size(HL_x1,2)-1
            S_x = HL_x1(i,j,k)+HL_x1(i-1,j-1,k)+HL_x1(i-1,j,k)+HL_x1(i-1,j+1,k)+HL_x1(i,j-1,k)+HL_x1(i,j+1,k)+HL_x1(i+1,j-1,k)+HL_x1(i+1,j,k)+HL_x1(i+1,j+1,k);
            S_x = S_x*(HL_x1(i,j,k))^2;

            S_y = HL_x2(i,j,k)+HL_x2(i-1,j-1,k)+HL_x2(i-1,j,k)+HL_x2(i-1,j+1,k)+HL_x2(i,j-1,k)+HL_x2(i,j+1,k)+HL_x2(i+1,j-1,k)+HL_x2(i+1,j,k)+HL_x2(i+1,j+1,k);
            S_y = S_y*(HL_x2(i,j,k))^2;

            if(S_x > S_y)
                HL_y(i-1,j-1,k) = HL_x1(i,j,k);
            else
                HL_y(i-1,j-1,k) = HL_x2(i,j,k);
            end
        end
    end
end

HH_y = zeros(size(HH_x1,1),size(HH_x1,2),3);
HH_x1 = padarray(HH_x1,[1 1],0,'both');
HH_x2 = padarray(HH_x2,[1 1],0,'both');

for k=1:3
    for i=2:size(HH_x1,1)-1
        for j=2:size(HH_x1,2)-1
            S_x = HH_x1(i,j,k)+HH_x1(i-1,j-1,k)+HH_x1(i-1,j,k)+HH_x1(i-1,j+1,k)+HH_x1(i,j-1,k)+HH_x1(i,j+1,k)+HH_x1(i+1,j-1,k)+HH_x1(i+1,j,k)+HH_x1(i+1,j+1,k);
            S_x = S_x*(HH_x1(i,j,k))^2;

            S_y = HH_x2(i,j,k)+HH_x2(i-1,j-1,k)+HH_x2(i-1,j,k)+HH_x2(i-1,j+1,k)+HH_x2(i,j-1,k)+HH_x2(i,j+1,k)+HH_x2(i+1,j-1,k)+HH_x2(i+1,j,k)+HH_x2(i+1,j+1,k);
            S_y = S_y*(HH_x2(i,j,k))^2;

            if(S_x > S_y)
                HH_y(i-1,j-1,k) = HH_x1(i,j,k);
            else
                HH_y(i-1,j-1,k) = HH_x2(i,j,k);
            end
        end
    end
end

% Concatenate resulting sub-bands %
y = [LL_y,LH_y;HL_y,HH_y];

% Perform Inverse Multiwavelet transform on RGB channels %
y_Red = IGHM(y(:,:,1));
y_Green = IGHM(y(:,:,2));
y_Blue = IGHM(y(:,:,3));

% Concatenate RGB channels
y = cat(3,y_Red,y_Green,y_Blue);
figure(3);
imshow(y);