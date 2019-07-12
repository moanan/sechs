# sechs

直接在main.py中定义robot的dh参数，工具，负载，角加速度。

调用robot.frame得到各个轴的空间方位

调用robot.frame.origin得到各个轴的空间位置

调用robot.torque(tool, payload, acceleration)得到各个轴所需的转矩

调用robot.visualization(tool, payload, acceleration)可视化

torque的计算方法：

  第i个轴的torque为：abs(往后各轴以及末端负载对第i轴z_axis的力矩和) + 往后各轴以及末端负载的总惯性矩 * 预设的角加速度
