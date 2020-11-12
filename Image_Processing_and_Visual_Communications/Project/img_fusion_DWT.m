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

saveFolder = 'ECE613_Images/Fused/FusedDWT_';

ifpm = zeros(length(MRIFiles), 9); %Create the basic ifmp array

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

  [ifpm_k, fused_img] = DWT_PSO(A_RGB, B_RGB); %Run the PSO function and return the fused img + the coeff used
  ifpm(k,:) = ifpm_k; %Assign the coeff to the array
  
  name = baseFileNameMRI(1:end-4); % Get the name of the img
  fusedImgName = strcat(saveFolder, name,'.png'); %Create the fused image name
  disp(strcat('Saving fused image and .mat for: ', fusedImgName));
  imwrite(fused_img, fusedImgName) %Save the fused img
  parsave(strcat(saveFolder, name), ifpm_k); % Save the .mat with the coefficients and ifpm
end

disp('Saving the whole workspace, just in case');
save('image_fusion_workspace_DWT') % Save the whole workspace, just in case

function parsave(name, ifpm_array) %Auxiliary saving function
    save(strcat(name,'.mat'), 'ifpm_array');
end
