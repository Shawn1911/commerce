from itertools import product


rangi = ['oq', 'qora', 'kok']
xotira = ['8gb', '16gb', '32gb', '64gb']

for i in product(rangi, xotira):
    print(i)
