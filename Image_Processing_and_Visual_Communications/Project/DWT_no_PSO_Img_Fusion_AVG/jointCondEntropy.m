function z = jointCondEntropy(x1, x2, y)
% Computes joint conditional entropy H(x1,x1|y)

% Flatten images %
n = numel(x1);
x1 = double(reshape(x1,1,n));
x2 = double(reshape(x2,1,n));
y_reshape = double(reshape(y,1,n));

% Compute joint pdf of x1, x2, and y % 
freq = zeros(256,256,256);
for i=1:size(x1,2)
    freq(x1(i)+1,x2(i)+1,y_reshape(i)+1) = freq(x1(i)+1,x2(i)+1,y_reshape(i)+1) + 1;
end
joint = freq/n;

% Compute pdf of y %
[y_counts, grayLevels] = imhist(y,256);
y_pdf = y_counts / numel(y);

% Compute joint conditional entropy %
Hx1x2y = 0;
for i=1:256
   for j=1:256
       for k=1:256
           if joint(i,j,k) ~= 0
               Hx1x2y = Hx1x2y + joint(i,j,k)*log2(joint(i,j,k)/y_pdf(k));
           end
       end
   end
end
Hx1x2y = -Hx1x2y;
z = Hx1x2y;
end