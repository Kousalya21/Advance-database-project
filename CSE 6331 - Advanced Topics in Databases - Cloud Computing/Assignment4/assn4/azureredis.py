"""
Yash Bardapurkar
1001731650
CSE-6331-004
"""

import redis

myHostname = "1650-assignment-3.redis.cache.windows.net"
myPassword = "GeOZuPhlpLf1j4PQ4tTyfTeIuybImUytAUxKX32wIDk="

r = redis.StrictRedis(host=myHostname, port=6380,password=myPassword,ssl=True)
