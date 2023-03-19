from jikanpy import Jikan
import diskcache
import time

jikan = Jikan()

cache = diskcache.Cache(f"/tmp/cache-{__name__}")


@cache.memoize()
def search(title):
    time.sleep(.5)
    result = jikan.search("anime", title)
    data = result["data"]
    if len(data) > 0:
        return data[0]
