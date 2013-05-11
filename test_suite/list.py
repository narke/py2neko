# append
l = []
l.append(1)
l.append(2)

print (l)

# list
l = list()
print(l)

# __eq__
print(([1,2,3] + [4,5,6,7]) ==  [1,2,3,4,5,6])

# __delitem__
l = [6,7,8]
del l[0]
print(l)

# __getitem__
print(l[1])

# __contains__
l = [21, 54, 87]
if 87 in l:
    print(True)
else:
    print(False)
