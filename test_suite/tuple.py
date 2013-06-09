# __add__()
a = (1,2)
b = (3,4)
c = a + b

print(c)

# __contains__()
l = (21, 54, 87)
if 87 in l:
    print(True)
else:
    print(False)

# __eq__()
print((1,2) == (1,2))

# __getitem__(i)
a = (1,2,3)
print(a[1])

# len()
print(len([1,2,3]))

# __mul__()
print([1,2]*3)

# count()
nb = a.count(1)
print(nb)

# index()
nb = a.index(1)
print(nb)
