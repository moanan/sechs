%% this script map the output pulley radius to the belt tension with 
% specified torque requirement

% r - pulley radius [mm]
% T - pulley torque [Mm]
% F - bele tenstion [N]

% An Mo
% 2019-08-18

clc;clear;close all;

r = 10:70;
T = [5:5:20, 30:10:50];

for j = 1:length(T)
    for i = 1:length(r)
        F(i) = T(j)/r(i) * 1000;
    end
    plot(r, F, 'lineWidth', 2, 'DisplayName', ['Torque: ',num2str(T(j)), ' [Nm]']); hold on;
end
title('Belt tension estimation');
xlabel('Output pulley radius [mm]'); ylabel('Timing belt tension [N]');
grid on; grid minor; legend show;

plot([r(1) r(end)], [300 300], '--', 'lineWidth', 1, 'DisplayName', '6mm belt: 300 [N]');
plot([r(1) r(end)], [599 599], '--', 'lineWidth', 1, 'DisplayName', '10mm belt: 599 [N]');


print('-painters','-depsc', 'belt_tension');