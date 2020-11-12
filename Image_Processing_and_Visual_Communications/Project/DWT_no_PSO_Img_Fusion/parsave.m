function parsave(name, ifpm_array) %Auxiliary saving function
    save(strcat(name,'.mat'), 'ifpm_array');
end