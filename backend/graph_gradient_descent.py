import matplotlib.pyplot as plt
import gradient_descent as gd


def f(x):
    return (x + 10) ** 2


seen_positions, seen_values = gd.perform_gradient_descent(f, 0, None, 5, 0, [0], [f(0)])

x = []
last = -20
while last < 5:
    last += 0.1
    x.append(last)

y = list(map(f, x))

plt.plot(x, y)
plt.scatter(seen_positions, seen_values, c="r")
plt.show()
