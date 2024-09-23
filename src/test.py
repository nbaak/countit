

label = (1, 2, 3, 4)
label2 = (11, 22, 33, 44)

my_dict = {}
if label not in my_dict:
    my_dict[label] = 1

if not label2 in my_dict:
    my_dict[label2] = 666
    
print(my_dict)
