

def dict_builder(*args, **kwargs):
    new_dict = {}
    for label, value in kwargs.items():
        if value != None: new_dict[label] = value 
        
    return new_dict


def test():
    print(dict_builder(a="A", label="DIETER", t54=10, l2=None, l3=0))


if __name__ == "__main__":
    test()
