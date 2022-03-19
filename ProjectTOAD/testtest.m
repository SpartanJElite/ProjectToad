clc
clear
close all

dir = 'C:\Users\spong\Documents\ProjectTOAD\SampleFiles\';
file = subdir(dir);
for i = 1:numel(file)
    filename = file(i).name;
    data = readtable(filename);
end
