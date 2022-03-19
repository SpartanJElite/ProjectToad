clc
clear
close all

counterTime = 0;
counterFirst = 0;
counterSecond = 0;
counterThird = 0;
previousData = 0;
currentData = 0;
maxTime = 15;

while(counterFirst == 0)
    dir = 'C:\Users\spong\Documents\ProjectTOAD\SampleFiles\';
    file = subdir(dir);
    fileNames = {file.name};
    currentFiles = fileNames;
    if(~isempty(fileNames))
        counterFirst = 1;
        data = readtable(fileNames{end});
        previousData = numel(fileNames);
    end
end

while(counterThird == 0)
    while(counterSecond == 0)
        file = subdir(dir);
        fileNames = {file.name};
        newFiles = setdiff(fileNames,currentFiles);
        if ~isempty(newFiles)
            currentFiles = fileNames;
            currentData = numel(fileNames);
            for i = (previousData+1):currentData
                data = [data;readtable(fileNames{i})];
            end
            previousData = currentData;
            counterTime = 0;
            counterSecond = 1;
        end
        counterTime = counterTime + 1;
        if (counterTime >= maxTime)
            counterThird = 1;
            counterSecond = 1;
        end
        pause(0.5);
    end
    counterSecond = 0;   
end
data = table2array(data);

subplot(3,1,1)
plot(data(:,1),data(:,2))

subplot(3,1,2)
plot(data(:,1),data(:,3))

subplot(3,1,3)
plot(data(:,1),data(:,4))