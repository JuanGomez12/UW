function [best_config, F] = DWT_PSO(x1_RGB, x2_RGB)
% Perform Single-Level 2D Multiwavelet decomposition on RGB channels of MRI image %  
x1_Red = (x1_RGB(:,:,1));
x1_Green = (x1_RGB(:,:,2));
x1_Blue = (x1_RGB(:,:,3));

% Perform Single-Level 2D Multiwavelet decomposition on RGB channels of SPECT image % 
x2_Red = (x2_RGB(:,:,1));
x2_Green = (x2_RGB(:,:,2));
x2_Blue = (x2_RGB(:,:,3));

% Concatenate RGB channels
img1 = cat(3, x1_Red, x1_Green, x1_Blue);
img2 = cat(3, x2_Red, x2_Green, x2_Blue);

% Extract LL (Approximations, A), LH(Horizontal,H), HL (Vertical, V), and HH(Diagonal, D) frequency sub-bands %
[img1_A_R, img1_H_R, img1_V_R, img1_D_R] = dwt2(x1_Red, 'db2');
[img1_A_G, img1_H_G, img1_V_G, img1_D_G] = dwt2(x1_Green, 'db2');
[img1_A_B, img1_H_B, img1_V_B, img1_D_B] = dwt2(x1_Blue, 'db2');

[img2_A_R, img2_H_R, img2_V_R, img2_D_R] = dwt2(x2_Red, 'db2');
[img2_A_G, img2_H_G, img2_V_G, img2_D_G] = dwt2(x2_Green, 'db2');
[img2_A_B, img2_H_B, img2_V_B, img2_D_B] = dwt2(x2_Blue, 'db2');

LL_x1 = cat(3,img1_A_R, img1_A_G, img1_A_B);
LH_x1 = cat(3,img1_H_R, img1_H_G, img1_H_B);
HL_x1 = cat(3,img1_V_R, img1_V_G, img1_V_B);
HH_x1 = cat(3,img1_D_R, img1_D_G, img1_D_B);

LL_x2 = cat(3,img2_A_R, img2_A_G, img2_A_B);
LH_x2 = cat(3,img2_H_R, img2_H_G, img2_H_B);
HL_x2 = cat(3,img2_V_R, img2_V_G, img2_V_B);
HH_x2 = cat(3,img2_D_R, img2_D_G, img2_D_B);


n_particles = 25; % number of particles to use in PSO
w = zeros(n_particles,8); % weights/particle positions
p = zeros(n_particles,9); % particles' best known positions + corresponding IFPMs
g = zeros(8); % swarm's best known position
ifpm_g = 0; % swarm's best IFPM value
v = zeros(n_particles,8); % particles' velocities

n_weights = 8;
for i=1:n_particles
    % Generate a candidate solution (particle position) drawn from a uniform distribution %
    w(i,:) = rand(n_weights,1); 
    
    % Initialize particle's best known position as this position %
    p(i,1:n_weights) = w(i,:);
    
    % Fusion of sub-bands based on weights (from particle i) %
    LL_F = p(i,1)*LL_x1 + p(i,2)*LL_x2;
    LH_F = p(i,3)*LH_x1 + p(i,4)*LH_x2;
    HL_F = p(i,5)*HL_x1 + p(i,6)*HL_x2;
    HH_F = p(i,7)*HH_x1 + p(i,8)*HH_x2;
    
    % Perform Inverse Discrete Wavelet Transform on RGB channels %
    F_Red = idwt2(LL_F(:,:,1), LH_F(:,:,1), HL_F(:,:,1), HH_F(:,:,1),'db2');
    F_Green = idwt2(LL_F(:,:,2), LH_F(:,:,2), HL_F(:,:,2), HH_F(:,:,2),'db2');
    F_Blue = idwt2(LL_F(:,:,3), LH_F(:,:,3), HL_F(:,:,3), HH_F(:,:,3),'db2');
    
    % Concatenate RGB channels %
    F = cat(3,F_Red,F_Green,F_Blue);
    
    % Compute IFPM of candidate solution %
    ifpm_p = IFPM(im2uint8(x1_RGB), im2uint8(x2_RGB), im2uint8(F));
    p(i,9) = ifpm_p;
    
    % Update the swarm's best known position %
    if(ifpm_p > ifpm_g)
        ifpm_g = ifpm_p;
        g = p(i,1:8);
    end
    
    % Generate a particle velocity drawn from a uniform distribution %
    v(i,:) = -1 + (1+1)*rand(1,8);
end

%omegas = [-0.6 -0.5 -0.4 -0.3 -0.2 -0.1 0.1 0.2 0.3 0.4 0.5 0.6];
omegas = [-0.6 -0.4 -0.2 0.1 0.3 0.5];
phi_ps = [-1 -0.6 -0.15 0.5 2.1 2.5];
phi_gs = [0.6 1.33 2.2 2.6 3.4 4 4.9];
best_config = zeros(1,9);
max_iter = 10; % termination criterion

ifpm_g_last = 0;
count = 0;
term = 0;

for omega_i=1:size(omegas,2)
    for phi_p_i=1:size(phi_ps,2)
        for phi_g_i=1:size(phi_gs,2)
            
            for iter=1:max_iter
                for i=1:n_particles
                    for d=1:8
                        rp = rand(1);
                        rg = rand(1);
            
                        % Update particle's velocity %
                        v(i,d) = omegas(omega_i)*v(i,d) + phi_ps(phi_p_i)*rp*(p(i,d) - w(i,d)) + phi_gs(phi_g_i)*rg*(g(d) - w(i,d));
                    end
        
                    % Update particle's position %
                    w(i,:) = w(i,:) + v(i,:);
        
                    % Fusion of sub-bands based on new weights %
                    LL_F = w(i,1)*LL_x1 + w(i,2)*LL_x2;
                    LH_F = w(i,3)*LH_x1 + w(i,4)*LH_x2;
                    HL_F = w(i,5)*HL_x1 + w(i,6)*HL_x2;
                    HH_F = w(i,7)*HH_x1 + w(i,8)*HH_x2;
    
                    % Perform Inverse Discrete Wavelet Transform on RGB channels %
                    F_Red = idwt2(LL_F(:,:,1), LH_F(:,:,1), HL_F(:,:,1), HH_F(:,:,1),'db2');
                    F_Green = idwt2(LL_F(:,:,2), LH_F(:,:,2), HL_F(:,:,2), HH_F(:,:,2),'db2');
                    F_Blue = idwt2(LL_F(:,:,3), LH_F(:,:,3), HL_F(:,:,3), HH_F(:,:,3),'db2');
    
                    % Concatenate RGB channels %
                    F = cat(3,F_Red,F_Green,F_Blue);
    
                    % Compute IFPM of new solution %
                    ifpm_w = IFPM(im2uint8(x1_RGB), im2uint8(x2_RGB), im2uint8(F));
        
                    % Update the particle's best known position %
                    if(ifpm_w > p(i,9))
                        p(i,1:8) = w(i,:);
                        p(i,9) = ifpm_w;
                        % Update the swarm's best known position %
                        if(p(i,9) > ifpm_g)
                            ifpm_g = p(i,9);
                            g = p(i,1:8);
                        end
                    end
                end
                verbose = sprintf('Iteration: %d',iter);
                disp(verbose);
            end
            
            if(ifpm_g > best_config(9))
                best_config(9) = ifpm_g;
                best_config(1:8) = g;
            end
            
            if(ifpm_g - ifpm_g_last < 0.000001)
                count = count + 1;
            end
            ifpm_g_last = ifpm_g;
            
            verbose = sprintf('Configuration: %d %d %d ====> IFPM = %f',omega_i, phi_p_i, phi_g_i, best_config(9));
            disp(verbose);
            
            if(count == 5)
                term = 1;
                break
            end
        end
        if(term == 1)
            break
        end
    end
    if(term == 1)
        break
    end
end

% Fusion of sub-bands based on optimal weights %
LL_F = best_config(1)*LL_x1 + best_config(2)*LL_x2;
LH_F = best_config(3)*LH_x1 + best_config(4)*LH_x2;
HL_F = best_config(5)*HL_x1 + best_config(6)*HL_x2;
HH_F = best_config(7)*HH_x1 + best_config(8)*HH_x2;

% Perform Inverse Discrete Wavelet Transform on RGB channels %
F_Red = idwt2(LL_F(:,:,1), LH_F(:,:,1), HL_F(:,:,1), HH_F(:,:,1),'db2');
F_Green = idwt2(LL_F(:,:,2), LH_F(:,:,2), HL_F(:,:,2), HH_F(:,:,2),'db2');
F_Blue = idwt2(LL_F(:,:,3), LH_F(:,:,3), HL_F(:,:,3), HH_F(:,:,3),'db2');

% Concatenate RGB channels %
F = cat(3,F_Red,F_Green,F_Blue);
    
% Compute IFPM of optimal solution %
ifpm_o = best_config(9);

%%save('best_config.mat', 'best_config');
