import redis

myHostname = "redis-1650-cse-6331.wlr5hy.ng.0001.use2.cache.amazonaws.com"

# r = redis.StrictRedis(host=myHostname, port=6380,password=myPassword,ssl=True)
r = redis.StrictRedis(host=myHostname, port=6379, db=0, socket_timeout=1)

# result = r.ping()
# print("Ping returned : " + str(result))

# result = r.set("Message", "Hello!, The cache is working with Python!")
# print("SET Message returned : " + str(result))

# result = r.get("Message")
# print("GET Message returned : " + result.decode("utf-8"))

# result = r.get("foo")
# print("GET Message returned : " + result.decode("utf-8"))

# result = r.client_list()
# print("CLIENT LIST returned : ") 
# for c in result:
# 	print("id : " + c['id'] + ", addr : " + c['addr'])
