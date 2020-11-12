dir_gen = 'ECE613_Images/Fused/';

dir_DWT_AVG = strcat(dir_gen,'DWT_AVG/');
DWT_AVG = dir(strcat(dir_DWT_AVG, 'Fused*.png'));

dir_DWT_PSO = strcat(dir_gen,'DWT_PSO/');
DWT_PSO = dir(strcat(dir_DWT_PSO, 'Fused*.png'));

dir_DWT_WANG = strcat(dir_gen,'DWT_WANG/');
DWT_WANG = dir(strcat(dir_DWT_WANG, 'Fused*.png'));

dir_MWT_AVG = strcat(dir_gen,'MWT_AVG/');
MWT_AVG = dir(strcat(dir_MWT_AVG, 'Fused*.png'));

dir_MWT_PSO = strcat(dir_gen,'MWT_PSO/');
MWT_PSO = dir(strcat(dir_MWT_PSO, 'Fused*.png'));

dir_MWT_WANG = strcat(dir_gen,'MWT_WANG/');
MWT_WANG = dir(strcat(dir_MWT_WANG, 'Fused*.png'));

dir_MWT_PSO_Grp = strcat(dir_gen,'MWT_PSO_Grp/');
MWT_PSO_Grp = dir(strcat(dir_MWT_PSO_Grp, 'Fused*.png'));

piqeArray = zeros(length(DWT_AVG),6);
entropyArray = zeros(length(DWT_AVG),6);
for i=1:length(DWT_AVG)
    DWT_AVG_img = imread(strcat(dir_DWT_AVG, DWT_AVG(i).name));
    DWT_PSO_img = imread(strcat(dir_DWT_PSO, DWT_PSO(i).name));
    DWT_WANG_img = imread(strcat(dir_DWT_WANG, DWT_WANG(i).name));
    MWT_AVG_img = imread(strcat(dir_DWT_AVG, DWT_AVG(i).name));
    MWT_PSO_Grp_img = imread(strcat(dir_MWT_PSO_Grp, MWT_PSO_Grp(i).name));
    MWT_WANG_img = imread(strcat(dir_MWT_WANG, MWT_WANG(i).name));
    entropyArray(i,1) = entropy(DWT_AVG_img);
    
    entropyArray(i,2) = entropy(DWT_PSO_img);
    entropyArray(i,3) = entropy(DWT_WANG_img);
    entropyArray(i,4) = entropy(MWT_AVG_img);
    entropyArray(i,5) = entropy(MWT_PSO_Grp_img);
    entropyArray(i,6) = entropy(MWT_WANG_img);
    piqeArray(i,1) = piqe(DWT_AVG_img);
    piqeArray(i,2) = piqe(DWT_PSO_img);
    piqeArray(i,3) = piqe(DWT_WANG_img);
    piqeArray(i,4) = piqe(MWT_AVG_img);
    piqeArray(i,5) = piqe(MWT_PSO_Grp_img);
    piqeArray(i,6) = piqe(MWT_WANG_img);
end
meanEntropy = mean(entropyArray);
meanPiqe = mean(piqeArray);