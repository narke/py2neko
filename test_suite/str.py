s = "hello world!"
print(s)

# add()
s = "hello" + " world!"
print(s)

# __contains__()
"abc".__contains__("ab")

# __eq__()
"abc".__eq__("abc")

# __getitem__()
"abc".__getitem__(1)

# __iter__()
for i in "abc":
	print(i)

# __ne__()
"abc".__ne__("cba")
