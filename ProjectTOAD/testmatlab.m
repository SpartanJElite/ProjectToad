clc
clear
close all

w = [0;0.5;1];
yaw = deg2rad(0);
pitch = deg2rad(0);
roll = deg2rad(0);
quat = angle2quat(yaw,pitch,roll);
tspan = [0:0.01:30];
y0 = quat;
[tSol,ySol] = ode45(@(t,y) g_func(y,w,t),tspan,y0);
ySol = ySol + 0.0*randn(size(ySol,1),4);
ySol = array_quat2eul(ySol);


figure()
% plot(tSol,ySol(:,2),'r')
% title('Collected Yaw vs Time')
% xlabel('Time [s]')
% ylabel('Yaw [deg]')

subplot(3,1,1)
title('Collected Euler Angles vs Time')
hold on
plot(tSol,ySol(:,1),'r')
xlabel('Time [s]')
ylabel('Yaw [deg]')
subplot(3,1,2)
plot(tSol,ySol(:,2),'r')
xlabel('Time [s]')
ylabel('Pitch [deg]')
subplot(3,1,3)
plot(tSol,ySol(:,3),'r')
xlabel('Time [s]')
ylabel('Roll [deg]')

futuretspan = [0:0.01:60];


% eq = determineFourier(tSol,ySol(:,2),futuretspan);
% figure(3)
% hold on
% scatter(tSol,ySol(:,2),'.r')
% plot(futuretspan,eq,'b')
% legend('Collected Yaw','Predicted Yaw')
% title('Collected and Predicted Yaw vs Time')
% xlabel('Time [s]')
% ylabel('Yaw [deg]')

hold on
subplot(3,1,1)
title('Collected and Predicted Euler Angles vs Time')
eq = determineFourier(tSol,ySol(:,1),futuretspan);
hold on
plot(tSol,ySol(:,1),'r')
plot(futuretspan,eq,'b')
xlabel('Time [s]')
ylabel('Yaw [deg]')
legend('Collected Yaw','Predicted Yaw')

subplot(3,1,2)
eq = determineFourier(tSol,ySol(:,2),futuretspan);
hold on
plot(tSol,ySol(:,2),'r')
plot(futuretspan,eq,'b')
xlabel('Time [s]')
ylabel('Pitch [deg]')

subplot(3,1,3)
eq = determineFourier(tSol,ySol(:,3),futuretspan);
hold on
plot(tSol,ySol(:,3),'r')
plot(futuretspan,eq,'b')
xlabel('Time [s]')
ylabel('Roll [deg]')

function [coeff] = coeffmaker(w)

    coeff = [0 -w(1) -w(2) -w(3);...
           w(1) 0     w(3) -w(2);...
           w(2) -w(3)  0    w(1);...
           w(3)  w(2)  -w(1)  0];

end

function [euler] = array_quat2eul(ySol)
    euler = zeros(size(ySol,1),3);
    for i = 1:size(ySol,1)
        [yaw,pitch,roll] = quat2angle(ySol(i,:));
        euler(i,:) = rad2deg([yaw,pitch,roll]);
    end

end

function [dY] = g_func(y,w,t)
    dY = (1/2)*coeffmaker(w)*y;
end


