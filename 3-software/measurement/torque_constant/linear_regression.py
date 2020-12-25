import numpy as np
from matplotlib import pyplot as plt

LINK_LENGTH = 0.2  # m
LINK_WEIGHT = 0.016  # kg
G = 9.8128  # m / s^2

def get_data():
    data = np.loadtxt("result_2820_np.txt").T
    x = data[0]
    y = data[1] * 0.001 * G * LINK_LENGTH - 0.5 * LINK_LENGTH * G * LINK_WEIGHT
    return x, y


def model(_x, _theta):
    return _x * _theta[0] + _theta[1]


def loss(_x, _y, _theta, _model):
    _loss = 0.0
    for i in range(len(_x)):
        _loss += (model(_x[i], _theta) - _y[i]) ** 2
    return _loss / len(_x)


def gradient(_x, _y, _theta, _model):
    g = np.array([0.0, 0.0])
    for i in range(len(_x)):
        g[0] += (model(_x[i], _theta) - _y[i]) * _x[i]
        g[1] += (model(_x[i], _theta) - _y[i])
    return g


def train(_x, _y, _theta, _model, lr=1e-4, steps=1000):
    for step in range(steps):
        _theta -= lr * gradient(_x, _y, _theta, _model)
        # print log
        if step % 100 == 0:
            print("step: %d, theta: %f %f, loss: %f" % (step, _theta[0], _theta[1], loss(_x, _y, _theta, _model)))
    return _theta


if __name__ == "__main__":
    x_train, y_train = get_data()
    theta = np.array([1.0, 0.0])
    # plot x, y data
    plt.scatter(x_train, y_train, color="red")
    # training
    theta_new = train(x_train, y_train, theta, model, steps=20000)
    print(theta_new)

    plt.title('result: k=0.01095249 b=0.00203316', color='black')
    plt.xlabel('Motor Current [A]', fontsize="12")
    plt.ylabel('Motor Torque (Nm)', fontsize="12")
    # plot line
    y_new = model(x_train, theta_new)
    plt.plot(x_train, y_new)
    plt.legend(['calculated torque', 'measured torque'], fontsize="12")
    plt.show()


