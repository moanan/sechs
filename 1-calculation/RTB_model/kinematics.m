clear;clf;

L(1) = Link('revolute', 'd', 0.08, 'a', 0,     'alpha', pi/2);
L(2) = Link('revolute', 'd', 0.06,    'a', 0.2,   'alpha', 0);
L(3) = Link('revolute', 'd', 0, 'a', 0,   'alpha', pi/2);
L(4) = Link('revolute', 'd', 0.2,    'a', 0,   'alpha', -pi/2);
L(5) = Link('revolute', 'd', 0.1,    'a', 0,     'alpha', pi/2);
L(6) = Link('revolute', 'd', 0.08,    'a', 0,     'alpha', 0);

sechs = SerialLink(L, 'name', 'sechs')

q0 = [0 0 pi/2 pi 0 0];
sechs.plot(q0, 'jvec');
% sechs.teach();
