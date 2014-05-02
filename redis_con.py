"""
    Redis Configuration File
"""

import redis

r = redis.StrictRedis(host = "localhost", port = 6379, db = 0)

"""
    Check connectivity to Redis DB
"""
def ping_pong():
    try:
        a = r.ping()
        if a:
            return True
    except:
        pass
    return False


"""
    Save user data to Redis DB using pipeline
    Datastructures:
        online_users - Set of all online users
        users - Sorted set which contains all registered users sorted by their no of wins
        user:id - Hash of [username + userid]
        user:id:score - User's score
"""
def save_user_to_db(user_name, user_id):
    try:
        pipe = r.pipeline()
        pipe.zadd("users", 0, user_id)
        pipe.sadd("online_users", user_id)
        pipe.hmset("user:"+user_id, {"name" : user_name, "id" : user_id })
        pipe.set("user:"+user_id+":score", 0)
        pipe.execute()
        return True
    except:
        pass
    return False


"""
    This fn takes necessary steps when app is stopped.
    Steps:
        1. Remove user from online set
"""
def app_stopped(user_id):
    try:
        pipe = r.pipeline() 
        pipe.srem("online_users", str(user_id))
        pipe.execute()
        return True
    except:
        pass
    return False
