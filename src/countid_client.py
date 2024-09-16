import requests


class CountItClient():
    
    def __init__(self, server:str, port:int):
        self.server = server
        self.port = port
        
    def __get(self, endpoint):
        response = requests.get(f"{self.server}:{self.port}/{endpoint}")
        return response
    
    def __post(self, endpoint, data):
        pass
        
    def add_metric(self, metric_name) -> bool:
        response = self.__get(f"/new/{metric_name}")
        
        if response.status_code() == 200:
            return True
        return False
    
    
def test():
    cic = CountItClient("http://localhost", 5000)
    cic.add_metric('test_metric')
    

if __name__ == "__main__":
    test()
    
        
