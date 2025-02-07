import time

def cache(func):
    cache_value = {} #why it doesnt disapper
    def wrapper(*args):
        if args in cache_value:
            return cache_value[args]
        result = func(*args)
        cache_value[args] = result
        return result
    return wrapper

@cache
def long_running_function(a, b):
    time.sleep(4)
    return a+b


val1 = [1, 2, 3, 4, 5, 2, 3, 4, 5]

for val in val1:
    print(long_running_function(val, val))

 #   https://youtu.be/-AzSRHiV9Cc?si=sfFj4ZnPpKEn9csm

#  wsgi
# venv
