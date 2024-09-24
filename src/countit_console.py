from countit_client import CountItClient


countit = CountItClient("http://localhost", 5050, token_file="auth.token")


def purge_metrics(countit):
    pass
    
    
def main():
    metrics = countit.metrics()
    # purge_metrics(countit)t25
    
    print("CONSOLE")
    for metric in metrics:
        # if metric == "test_counter": continue
        print(f"{metric}")
        data = countit.data(metric)
        
        # print sorted by value
        for label, value in sorted(data, key=lambda x: x[1], reverse=True):
            #if label == "__default_label__": continue
            print(value, label)
        
        print()

    
if __name__ == "__main__":
    main()
