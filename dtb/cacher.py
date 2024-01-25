from django.core.cache import cache


class ActiveUserCache:
    """Cache for number of active users in the channel.group_name"""

    cache_backend = cache
    timeout = 60 * 60 * 24 * 7  # 1 week
    prefix = "active_user_"

    def __init__(self, group_name: str):
        self.group_name = group_name

    def get(self) -> int:
        """Get number of active users in the channel.group_name"""
        return self.cache_backend.get(self.prefix + self.group_name, 0)

    def set(self, value: int):
        """Set number of active users in the channel.group_name"""
        return self.cache_backend.set(
            self.prefix + self.group_name, value, self.timeout
        )

    def increment(self) -> int:
        """Safe increment number of active users in the channel.group_name
        if not exists, create with timeout"""
        try:
            return self.cache_backend.incr(self.prefix + self.group_name)
        except ValueError:
            self.set(1)
            return 1

    def decrement(self) -> int:
        """Decrement number of active users in the channel.group_name"""
        try:
            return self.cache_backend.decr(self.prefix + self.group_name)
        except ValueError:
            self.set(0)
            return 0
