from src.SACache import SACache
from src.Cache import Cache

l1d = SACache(64, 2, 16)
l1i = SACache(64, 2, 16)
l2 = SACache(128, 4, 32)
l3 = SACache(1024, 4, 64)

cache1 = Cache(l1d, l1i, l2, l3)

cache2 = cache1.duplicate()

print(cache2)