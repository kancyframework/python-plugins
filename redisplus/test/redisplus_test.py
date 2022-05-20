import redisplus

# 获取SimpleRedis对象，不支持的的value会自动实现序列化
redis = redisplus.getSimpleRedis(host="docker.kancy.top", password="root123")

redis.set("m", (1,2,3))
s = redis.get("m")
