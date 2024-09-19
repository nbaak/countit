import requests


def dict_builder(*args, **kwargs):
    new_dict = {}
    for label, value in kwargs.items():
        if value != None: new_dict[label] = value 
        
    return new_dict


class CountItClient():
    
    def __init__(self, server:str, port:int):
        self.server = server
        self.port = port
        
    def __get(self, endpoint):
        try:
            response = requests.get(f"{self.server}:{self.port}/{endpoint}")
            return response
        except Exception as e:
            print(e)
            return "Server not available"
    
    def __post(self, endpoint, data:dict=None):
        try:
            if data:
                response = requests.post(f"{self.server}:{self.port}/{endpoint}", json=data)
            else:
                response = requests.post(f"{self.server}:{self.port}/{endpoint}", json={})
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
    cic = CountItClient("http://localhost", 5000)
    print(cic.add_metric('test_metric'))
    
    print(cic.inc('test_metric', label='test_1', value=3))
    print(cic.inc('test_metric', label=(4, 2), value=2))
    print(cic.inc('test_metric', label=("1.2.3.4", 5001, 66), value=2))
    print(cic.inc('test_metric'))
    
    print("Labels:", cic.labels("test_metric"))
    print(cic.get('test_metric', label='test_1'))
    print(cic.get('test_metric'))
    
    print(cic.add_metric('test_metric_2'))
    print("Labels:", cic.labels("test_metric_2"))
    print(cic.get('test_metric_2'))
    

if __name__ == "__main__":
    test()
        
