function ifpm_val = dwt_ifpm_function(X1, X2, w1, w2, w3, w4, w5, w6, w7, w8)

Y = im2uint8(dwt_Fusion(X1, X2, w1, w2, w3, w4, w5, w6, w7, w8));

X1 = im2uint8(X1);
X2 = im2uint8(X2);

% Separate RGB channels for images %
X1_Red = X1(:,:,1);
X1_Green = X1(:,:,2);
X1_Blue = X1(:,:,3);

X2_Red = X2(:,:,1);
X2_Green = X2(:,:,2);
X2_Blue = X2(:,:,3);

Y_Red = Y(:,:,1);
Y_Green = Y(:,:,2);
Y_Blue = Y(:,:,3);

% Compute joint entropy of X1 and X2 %
Hx1x2_Red = jointEntropy(X1_Red, X2_Red);
Hx1x2_Green = jointEntropy(X1_Green, X2_Green);
Hx1x2_Blue = jointEntropy(X1_Blue, X2_Blue);

Hx1x2 = (Hx1x2_Red + Hx1x2_Green + Hx1x2_Blue) / 3;

% Compute joint entropy of X1 and X2 given the fused image %
Hx1x2y_Red = jointCondEntropy(X1_Red, X2_Red, Y_Red);
Hx1x2y_Green = jointCondEntropy(X1_Green, X2_Green, Y_Green);
Hx1x2y_Blue = jointCondEntropy(X1_Blue, X2_Blue, Y_Blue);

Hx1x2y = (Hx1x2y_Red + Hx1x2y_Green + Hx1x2y_Blue) / 3;

% Compute final IFPM value %
CI = Hx1x2 - Hx1x2y;
ifpm_val = CI / Hx1x2;

end

