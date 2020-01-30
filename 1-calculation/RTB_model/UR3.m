clear;clf;

L(1) = Link('revolute', 'd', 0.15185,   'a', 0,     'alpha', pi/2);
L(2) = Link('revolute', 'd', 0,         'a', -0.24355,  'alpha', 0);
L(3) = Link('revolute', 'd', 0,         'a', -0.2132,   'alpha', 0);
L(4) = Link('revolute', 'd', 0.13105,   'a', 0,     'alpha', pi/2);
L(5) = Link('revolute', 'd', 0.08535,   'a', 0,     'alpha', -pi/2);
L(6) = Link('revolute', 'd', 0.08535,   'a', 0,     'alpha', 0);

sechs = SerialLink(L, 'name', 'UR3')


q0 = [0 0 0 0 0 0];
sechs.plot(q0, 'jvec');
sechs.teach();
