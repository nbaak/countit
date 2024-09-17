import os
import pickle
from typing import Union
from countit_status_codes import StatusCodes


class Metric:
    
    def __init__(self, metric_name:str, data_location:str, labels:list=None):
        self.metric_name = metric_name
        
        self.data_location = data_location
        if not os.path.isdir(self.data_location):
            os.mkdir(self.data_location)
            
        self.data = {'__default_label__': 0}
        
        # experimental
        if labels:
            for label in labels:
                self.data[label] = 0
        
    def inc(self, label, value:Union[int, float]=1) -> Union[int, float]:
        if not label in self.data:
            self.data[label] = 0
        
        self.data[label] += value
        
        self.save()
        return self.data.get(label, None)
    
    def update(self, label, value:Union[int, float]=1) -> Union[int, float]:
        self.inc(label, value)
        
    def set(self, label:str, value:Union[int, float]=1) -> Union[int, float]:
        if not label in self.data:
            self.data[label] = value
        else:
            self.data[label] = value
        
        self.save()
        return self.data.get(label, None)
        
    def get(self, label):
        try:
            return self.data.get(label, None)
        except Exception as e:
            print(e)
            
    def remove(self, label):
        if label in self.data:
            drop = self.data.pop(label)
            if drop: return True
        
        return False
            
    def labels(self):
        return [label for label in self.data.keys()]
    
    def save(self):
        path = os.path.join(self.data_location, f"{self.metric_name}.dat") 
        with open(path, 'wb') as f:
            pickle.dump(self.data, f)
    
    def load(self):
        path = os.path.join(self.data_location, f"{self.metric_name}.dat")
        try:
            with open(path, 'rb') as f:
                self.data = pickle.load(f)
        except Exception as e:
            print(e)
            
    def __str__(self):
        return f"{self.metric_name}"
    
    def __repr__(self):
        return f"{self.metric_name}"


class Metrics:
    
    def __init__(self, data_location:str="./data_metrics"):
        self.metrics = {}
        self.data_path = data_location
        
    def add_metric(self, metric_name:str) -> Union[Metric, int]:
        status_code = None
        
        if metric_name not in self.metrics:
            self.metrics[metric_name] = Metric(metric_name, self.data_path)
            status_code = StatusCodes.NEW
        elif metric_name in self.metrics:
            status_code = StatusCodes.EXISTING
        else:
            status_code = StatusCodes.ERROR
            
        return self.metrics[metric_name], status_code
    
    def remove_metric(self, metric_name:str) -> bool:
        if metric_name in self.metrics:
            dropping = self.metrics.pop(metric_name)
            if dropping: return True
        
        return False
            
    def get_metric(self, metric_name:str) -> Metric:
        return self.metrics.get(metric_name, None)
        
    def show_metrics(self):
        return [str(metric) for metric in self.metrics.values()]
                
    def save(self):
        if not os.path.isdir(self.data_path):
            os.mkdir(self.data_path)
        
        for metric in self.metrics.values():
            metric.save()
    
    def load(self):
        try:
            files = os.listdir(self.data_path)
        except Exception as e:
            print(e)
            return
        
        for file in files:
            metric_name = file.split('.')[0]
            metric, _ = self.add_metric(metric_name)
            metric.load()
            


def test():
    metrics = Metrics(data_location='./data_metrics')
    metrics.load()
    counter = metrics.add_metric('Counter')
    
    counter.inc('up', 1)
    counter.inc('up', 1)
    counter.inc('up', 3)
    
    counter.set('dd', 7)
    
    print(f"Counter -up-  has value {counter.get('up')}")
    print(f"Counter -dd- has value {counter.get('dd')}")
    print(f"Counter -DDD- has value {counter.get('DDD')}")
    
    print(metrics.show_metrics())
    print(counter.labels())
    # counter.remove('up')
    print(counter.labels())
    
    # metrics.remove_metric('Counter')
    
    metrics.save()

        
if __name__ == "__main__":
    test()
