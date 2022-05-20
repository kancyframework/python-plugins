### 使用手册

**快速开始**

```python
import redisplus

# 获取原生的Redis对象
# redis = redisplus.getRedis(host="docker.kancy.top", password="root123")

# 获取SimpleRedis对象，不支持的的value会自动实现序列化
redis = redisplus.getSimpleRedis(host="docker.kancy.top", password="root123")

# 设置属性
redis.set("name", "kancy")

# 查询
redis.get("name")

# 删除
redis.delete("name")

# 设置过期时间
redis.setex("name", "kancy", 0.01)

# 设置，当key不存在时
redis.setnx("name", "kancy")
```