%% this script map the output pulley radius to the belt tension with 
% specified torque requirement

% r - pulley radius [mm]
% T - pulley torque [Mm]
% F - bele tenstion [N]

% An Mo
% update 2020-03-08
% create 2019-08-18

clc;clear;close all;

r = 10:70;
T = [5:5:20, 30:10:50];

for j = 1:length(T)
    for i = 1:length(r)
        F(i) = T(j)/r(i) * 1000;
    end
    plot(r*2, F, 'lineWidth', 2, 'DisplayName', ['Torque: ',num2str(T(j)), ' [Nm]']); hold on;
end
title('Belt tension estimation (5mm pitch)');
xlabel('Output pulley diameter [mm]'); ylabel('Timing belt tension [N]');
grid on; grid minor; legend show;

plot([r(1)*2 r(end)*2], [350 350], '--', 'lineWidth', 1, 'DisplayName', 'AT5 6mm: 350 [N]');
plot([r(1)*2 r(end)*2], [700 700], '--', 'lineWidth', 1, 'DisplayName', 'AT5 10mm: 700 [N]');
plot([r(1)*2 r(end)*2], [1260 1260 ], '--', 'lineWidth', 1, 'DisplayName', 'AT5 16mm: 1260 [N]');


print('-painters','-depsc', 'belt_tension');
print('-painters','-dpng', 'belt_tension');