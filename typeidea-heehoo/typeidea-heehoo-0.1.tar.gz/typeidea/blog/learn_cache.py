import functools
import time

CACHE = {}

def cache_it(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        key = repr(*args, **kwargs)
        print(key)
        try:
            result = CACHE[key]
        except KeyError:
            result = func(*args, **kwargs)
            CACHE[key] = result
        return result
    return inner

@cache_it
def qurey(sql):
    time.sleep(2)
    result = 'execute %s' % sql
    return result

if __name__ == '__main__':
    start = time.time()
    qurey('SELECT * FROM blog_post')
    print(time.time()-start)

    start = time.time()
    qurey('SELECT * FROM blog_post')
    print(time.time() - start)
