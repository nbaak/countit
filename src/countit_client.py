import os
import requests


def read_token(token_file):
    if os.path.exists(token_file):
        with open(token_file, 'r') as f:
            return f.read()
    return None


def dict_builder(in_dict=None, *args, **kwargs):
    parse_dict:dict = in_dict or kwargs
    new_dict = {}
    for label, value in parse_dict.items():
        if value != None: new_dict[label] = value 
        
    return new_dict


def build_headers(token:str):
    headers = {
        "Authorization": f"{token}",
        "Content-Type": "application/json"
    }
    return headers


class CountItClient():
    
    def __init__(self, server:str, port:int, token_file:str=None):
        self.server = server
        self.port = port
        self.token = read_token(token_file) 
        
    def __get(self, endpoint):
        try:
            headers = build_headers(self.token)
            response = requests.get(f"{self.server}:{self.port}/{endpoint}", headers=headers)
            return response
        except Exception as e:
            print(e)
            return "Server not available"
    
    def __post(self, endpoint, data:dict=None):
        try:
            headers = build_headers(self.token)
            response = requests.get(f"{self.server}:{self.port}/{endpoint}", headers=headers)
            if data:
                response = requests.post(f"{self.server}:{self.port}/{endpoint}", json=data, headers=headers)
            else:
                response = requests.post(f"{self.server}:{self.port}/{endpoint}", json={}, headers=headers)
            return response        
        except Exception as e:
            print(e)
            return "Server not available"
        
    def add_metric(self, metric_name, password="") -> bool:
        data = dict_builder(password=password)
        response = self.__post(f"/new/{metric_name}", data)
        
        if response.status_code == 201:
            return response.json()["success"]
        
        return False
    
    def inc(self, metric_name:str, *args, label=None, value=None, password=None) -> bool:
        """
        increases the metric label by value
        """
        data = dict_builder(label=label, value=value, password=password)
             
        response = self.__post(f"/inc/{metric_name}", data)
        
        if response.status_code == 202:
            return response.json()["success"]
        
        return False
    
    def update(self, metric_name:str, *args, label=None, value=None, password=None) -> bool:
        """
        updates the metric label by value
        same as inc
        """
        return self.inc(metric_name, label=label, value=value, password=password)
    
    def labels(self, metric_name:str):
        """
        get labels of metric
        """
        response = self.__get(f"/labels/{metric_name}")
        
        if response.status_code == 201:
            return response.json()["success"]
        
        return None
    
    def get(self, metric_name:str, *args, label=None):
        """
        get labels of metric
        """
        data = dict_builder(label=label)
            
        response = self.__post(f"/get/{metric_name}", data)
        
        if response.status_code == 201:
            return response.json()["success"]
        
        return None
    
    def metrics(self):
        """
        get metrics from service
        """
        response = self.__get(f"/countit_metrics")
        
        if response.status_code == 200:
            return response.json()["success"]
        
        return None
    
    def delete(self, metric_name, password=None):
        data = dict_builder(password=password)
        response = self.__post(f"/delete/{metric_name}", data)
        
        if response.status_code == 201:
            return response.json()["success"]
        
        return None
    
    def __str__(self):
        return f"CountIt: {self.server}:{self.port}"
    
    def __repr__(self):
        return self.__str__()
    
    
def test():
    # test dict builder
    d1 = dict_builder(a="a", B=1, c=None, d="123")
    print(d1)
    d2 = dict_builder(d1)
    print(d2)
    d3 = dict_builder({"a": None, "b": "C", (12, 32): (12, 34, 56)})
    print(d3)


if __name__ == "__main__":
    test()
        
