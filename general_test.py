import cachetools
import cachetools.keys

@cachetools.cached(cache={}, key=lambda a: cachetools.keys.hashkey(a))
def fibonacci(a):
    if a == 0:
        return 0
    if a == 1:
        return 1
    if a == 2:
        return 2
    return fibonacci(a - 1) + fibonacci(a - 2)

print(fibonacci(100))