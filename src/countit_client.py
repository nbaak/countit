import requests


class CountItClient():
    
    def __init__(self, server:str, port:int):
        self.server = server
        self.port = port
        
    def __get(self, endpoint):
        response = requests.get(f"{self.server}:{self.port}/{endpoint}")
        return response
    
    def __post(self, endpoint, data:dict=None):
        if not data: return None
        if not endpoint: return None
        response = requests.post(f"{self.server}:{self.port}/{endpoint}", json=data)
        return response
        
    def add_metric(self, metric_name) -> bool:
        response = self.__get(f"/new/{metric_name}")
        
        if response.status_code == 201:
            return response.json()["success"]
        
        return False
    
    def inc(self, metric_name:str, label, value=1) -> bool:
        """
        increases the metric label by value
        """
        if label and value:
            data = {'label': label, 'value': value}
            response = self.__post(f"/inc/{metric_name}", data)
            
            if response.status_code == 202:
                return response.json()["success"]
        
        return False
    
    def update(self, metric_name:str, label, value=1) -> bool:
        """
        updates the metric label by value
        same as inc
        """
        return self.inc(metric_name, label, value)
    
    
def test():
    cic = CountItClient("http://localhost", 5000)
    print(cic.add_metric('test_metric'))
    print(cic.inc('test_metric', 'test_1', 3))
    print(cic.inc('test_metric', (4, 2), 42))
    

if __name__ == "__main__":
    test()
        
