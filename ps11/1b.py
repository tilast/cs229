import numpy

# xs = fopen('./logistic_x.txt', 'r')
# ys = fopen('./logistic_y.txt', 'r')

with open('./logistic_x.txt', 'r') as xs_file:
    xs = [[float(xp.strip()) for xp in x.strip().split('  ')] for x in xs_file.readlines()]

with open('./logistic_y.txt', 'r') as ys_file:
    ys = [float(y.strip()) for y in ys_file.readlines()]

print(xs)
print(ys)
