
import json
from countit.transport_list import dict_as_transport_list


data_dict = {'__default_label__': 1, 'test_1': 3, ('1.2.3.4', 'DE'): 10, ('172.18.0.1', 'FASEL'): 7}
data_dict = dict_as_transport_list(data_dict)
for label, value in data_dict:
    print(label, value)


print(json.loads(data_dict))