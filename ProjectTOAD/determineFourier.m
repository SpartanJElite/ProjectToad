function [eq] = determineFourier(tspan,y,time)
%Purpose:Finding the fourier coefficients to describe the dataset and Noise
%Reduction
%
%Input:tspan = time span of the dataset
%      y = dataset of euler angles or quaterions
%      time = time span for predicting the dataset at a specific time range
%Output:eq = data set in the specific time range

%Author:Jason Le
%Last Modified:1/25/2022
%Project:CROACS
%Contributors:Steve Brunton

    %%%Function Setup%%%
    Nfourier = 1000; %Number of Fourier Coefficients wanted(More sometimes does mean more accurate and may lead to inaccuracy)
    dt = mean(diff(tspan))*2; %Scaled average time steps (Noise Reduction)
    dx = mean(diff(tspan))*(1/1); %Scaled average time steps (Fourier Coefficients)
    N = numel(tspan); %Number of data points
    average = mean(tspan); %Average time value
    L = average-min(tspan); %Half time span
    
    %%%Noise Reduction%%%
%     fhat = fft(y,N); %Fast Fourier Coefficients
%     PSD = fhat.*conj(fhat)/N; %Normalized magnitude of FFT (Power Magnitude)
%     freq = 1/(dt*N)*(0:N-1); %Frequency range to map power magnitude
% % 
% %     tol = 1000000;
% %       figure(10)
% %       plot(freq,PSD) %Figure used for debugging
% %       yline(tol)
% %       hold off
% % 
%     idx = PSD > mean(PSD); %Finding the index of wanted frequencies
%     PSDclean = PSD.*idx; %Power frequency with only index
%     fhat = idx.*fhat; %Index of only FFT that is wanted
%     ffilt = ifft(fhat); %Convert FFT to normal spec
    
%     figure()
%     plot(tspan,ffilt) %Figure used for debugging

%     y = ffilt; %Noise Reduced Signal

    %%%Fourier Coefficients Algoithem%%%
    A0 = sum(y.*ones(size(tspan)))*dx; %A0 term
    fFS = A0/2; %Total coefficient vector
%     figure()
%     hold on %used for debugging
    for k=1:Nfourier
        A(k) = sum(y.*cos(pi*k*tspan/L))*dx; % Inner product
        B(k) = sum(y .*sin(pi*k*tspan/L))*dx;
        fFS = fFS + A(k)*cos(k*pi*tspan/L) + B(k)*sin(k*pi*tspan/L);
        %plot(tspan,fFS,'-','LineWidth',1.2) %Used for debugging
    end
    fFS = fFS * (max(y)/max(fFS)); %Coefficient resizing
    %figure()
    %plot(tspan,fFS) %Used for debugging

    %%%Future Fourier Coefficients Algoithem%%%
    tspan = time; %Time where the coefficient apply
    fFS = A0/2; %A0 term
    for i = 1:Nfourier
        fFS = fFS + A(i)*cos(i*pi*tspan/L) + B(i)*sin(i*pi*tspan/L); %inner product
        %plot(tspan,fFS,'-','LineWidth',1.2) %Used for debugging
    end
    fFS = fFS * (max(y)/max(fFS))*1.0; %Coefficient resizing
    eq = fFS; %Output
end