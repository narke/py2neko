# append()
l = []
l.append(1)
l.append(2)

print (l)

# list()
l = list()
print(l)

# __eq__()
print(([1,2,3] + [4,5,6,7]) ==  [1,2,3,4,5,6])

# __delitem__()
l = [6,7,8]
del l[0]
print(l)

# __getitem__()
print(l[1])

# __contains__()
l = [21, 54, 87]
if 87 in l:
    print(True)
else:
    print(False)

# __mul__()
print([1,2]*3)

# len()
print(len([1,2,3]))

# reversed()
a = reversed([1,2])
for i in a:
	print(i)
	
b = reversed([1,2])
b.__next__()

# reverse()
a = [1,2,3]
a.reverse()
print(a)

# count()
nb = a.count(1)
print(nb)

# index()
nb = a.index(1)
print(nb)

# insert()
a.insert(1,21)
print(a)

# pop()
a = [1,2,3]
value = a.pop()
print(value)


# remove
a.remove(2)
print(a)
