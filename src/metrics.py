import pickle


class Metric:
    
    def __init__(self, metric_name:str):
        self.metric_name = metric_name
    
    def save(self, file:str):
        pass
    
    def load(self, file:str):
        pass
    
    def __repr__(self):
        return f"{self.metric_name}"

class Counter(Metric):
    
    def __init__(self, metric_name:str):
        super().__init__(metric_name)        
        self.value = 0
        
    def inc(self, value:int=1):
        self.value += value
        
    def get(self):
        return self.value
    
    def __str__(self):
        return f"{self.metric_name}({self.value})"
    
    
class Dictionary(Metric):
    
    def __init__(self, metric_name:str):
        super().__init(metric_name)
        self.table = {}
        
    def update(self, label, value=1):
        if label not in self.table:
            self.table[label] = 0
        self.table[label] += value
        
    def get(self, label:str):
        if label in self.table:
            return  self.table[label]
        return None
    
    def get_all(self):
        return [(k,v) for k,v in self.table.items()]
    
    def __str__(self):
        return f"{self.metric_name}"
    

# TODO: contiuous - table but label is timestamp
    
        

