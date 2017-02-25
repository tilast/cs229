import numpy as np
from numpy.linalg import inv, norm

from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

with open('../logistic_x.txt', 'r') as xs_file:
    xs = np.array([np.concatenate(([1], [float(xp.strip()) for xp in x.strip().split('  ')])) for x in xs_file.readlines()])

with open('../logistic_y.txt', 'r') as ys_file:
    ys = np.array([1 if int(float(y.strip())) == 1 else 0 for y in ys_file.readlines()])

m = len(xs)

def newton_minimize(f, g, h, x0, eps):
    x_prev = x0
    x = x0 - inv(h(x0)).dot(g(x0))

    iters = 1
    while norm(x - x_prev) > eps:

        if (iters >= 3):
            return x

        x_prev = x

        print(x)
        print(h(x))
        print("-----")

        x = x - inv(h(x)).dot(g(x))

        iters += 1

    return x

def lg(z):
    return 1 / (1 + np.e ** (-z))

def h_t(t, x):
    return lg(np.dot(t, x))

def L(t):
    prob = 1;
    for i in range(m):
        h_t_x_i = h_t(t, xs[i])
        cur_prob = (h_t_x_i ** ys[i]) * ((1 - h_t_x_i) ** (1 - ys[i]))
        prob *= cur_prob
    return prob

# log-likelihood
def l(t):
    total = 0
    for i in range(m):
        htxi = h_t(t, xs[i])
        yi = ys[i]

        if htxi < 0.0000001:
            htxi = 0.0000001
        elif htxi > 0.9999999:
            htxi = 0.9999999

        total += yi * np.log(htxi) + (1 - yi) * np.log(1 - htxi)
    return total

def l_gradient(t):
    t_len = len(t)
    grad = np.array([0.0 for i in range(t_len)])
    for i in range(m):
        xi = xs[i]
        yi = ys[i]
        htxi = h_t(t, xi)

        # if htxi < 0.0000001:
        #     htxi = 0.0000001
        # elif htxi > 0.9999999:
        #     htxi = 0.9999999

        for k in range(t_len):
            grad[k] += (yi - htxi) * xi[k]
    return grad

def l_hessian(t):
    t_len = len(t)
    hessian = np.array([[0.0 for s in range(t_len)] for k in range(t_len)])
    for i in range(m):
        xi = xs[i]
        htxi = h_t(t, xi)

        # if htxi < 0.0000001:
        #     htxi = 0.0000001
        # elif htxi > 0.9999999:
        #     htxi = 0.9999999

        for k in range(t_len):
            for s in range(t_len):
                hessian[k][s] += xi[k] * xi[s] * htxi * (1 - htxi)
    return hessian

print(ys)

# def gradient_descent()

# print(L(np.array([500, 500, 500])))
start_thetas = np.array([0.0, 0.0, 0.0])
print(l(start_thetas))
print(l_gradient(start_thetas))
print(l_hessian(start_thetas))

thetas = newton_minimize(l, l_gradient, l_hessian, start_thetas, 0.01)

# thetas = thetas / thetas[0]

print(thetas)

fig = plt.figure()
ax = fig.gca(projection='3d')
x1s = xs[:,1]
x2s = xs[:,2]

print(min(x1s))
print(max(x1s))
print(max(x1s) - min(x1s) / 100)

X = np.arange(min(x1s), max(x1s), (max(x1s) - min(x1s)) / 100)
print("X:")
print(X)
Y = np.arange(min(x2s), max(x2s), (max(x2s) - min(x2s)) / 100)
X, Y = np.meshgrid(X, Y)





transformation = thetas[0] + thetas[1] * X + thetas[2] * Y

logistic = 1 / (1 + np.exp(-transformation))

Z = logistic


surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)
ax.set_zlim(0, 1.5)

ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

fig.colorbar(surf, shrink=0.5, aspect=5)

plt.show()