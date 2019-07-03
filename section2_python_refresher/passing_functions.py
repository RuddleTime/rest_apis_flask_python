
def methodception(another):
    return another()

def add_two_numbers():
    return 35 +77


print(methodception(add_two_numbers))

print(methodception(lambda: 35 + 77))



my_list = [13, 56, 77, 484]
new_list = [item for item in my_list if item%2==0]
print(new_list)


print(list(filter(lambda x: x%2==0, my_list)))


def multiply_3(num):
    return num*3

print(multiply_3(5))
print((lambda x: x*3)(5))
