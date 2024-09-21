

def read_token(tokenfile) -> str:
    try:
        with open(tokenfile, 'r') as f:
            return f.read()
    except Exception as e:
        return ""
