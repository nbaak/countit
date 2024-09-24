

def dict_as_transport_list(data:dict) -> list:    
    sending = []
    
    for k, v in data.items():
        block = []
        
        # check for tuples..
        if isinstance(k, tuple):
            k = list(k)
            
        if isinstance(v, tuple):
            v = list(v)
        
        # append parts
        block.append(k)
        block.append(v)
        
        sending.append(block)
    
    return sending
