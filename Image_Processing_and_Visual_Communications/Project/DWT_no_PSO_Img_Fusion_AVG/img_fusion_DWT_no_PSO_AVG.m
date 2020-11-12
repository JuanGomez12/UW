%Script for obtaining the fused images using DWT with the selected
%coefficients for the LL subband. Also calculates the IFPM and saves the
%obtained value + the fused image in the specified folder.

% Get the list of images and create the folder for the output images, if it
% doesn't exist
cd ECE613_Images
if ~exist('Fused' , 'dir')
    mkdir('Fused')
end
cd MRI
MRIFolder = pwd;
MRIFiles = dir('*.gif');
cd ..
cd PET
PETFolder = pwd;
PETFiles = dir('*.gif');
cd ..
cd ..

saveFolder = 'ECE613_Images/Fused/FusedDWT_No_PSO_AVG_';

ifpm = zeros(length(MRIFiles), 1); %Create the basic ifmp array

parfor k = 1:length(MRIFiles)
  baseFileNameMRI = MRIFiles(k).name; %Get the name of one of the MRI images on the list
  baseFileNamePET = PETFiles(k).name; %Get the name of one of the PET images on the list
  fullFileNameMRI = fullfile(MRIFolder, baseFileNameMRI); %Get the file path for the MRI image
  fullFileNamePET = fullfile(PETFolder, baseFileNamePET); %Get the file path for the PET image
  
  disp(strcat('Now reading: ', fullFileNameMRI));
  [A,map] = imread(fullFileNameMRI,1); %Load the MRI img
  A_RGB = ind2rgb(A,map);
  disp(strcat('Now reading: ', fullFileNamePET));
  [B,map] = imread(fullFileNamePET,1); %Load the PET img
  B_RGB = ind2rgb(B,map);

  %Fuse the image using the provided coeff for the LL subband, and get its
  %IFPM
  [ifpm_k, fused_img] = DWT_img_fusion_AVG(A_RGB, B_RGB, 0.5, 0.5); 
  ifpm(k,:) = ifpm_k; %Assign the coeff to the array
  
  name = baseFileNameMRI(1:end-4); % Get the name of the img
  fusedImgName = strcat(saveFolder, name,'.png'); %Create the fused image name
  disp(strcat('Saving fused image and .mat for: ', fusedImgName));
  imwrite(fused_img, fusedImgName) %Save the fused img
  parsave(strcat(saveFolder, name), ifpm_k); % Save the .mat with the coefficients and ifpm
end

disp('Saving the whole workspace, just in case');
save('image_fusion_workspace_DWT_No_PSO_AVG') % Save the whole workspace, just in case
