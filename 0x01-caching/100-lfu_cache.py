#!/usr/bin/env python3

'''
LFU Caching
'''
from collections import deque
from base_caching import BaseCaching


class LFUCache(BaseCaching):
    """
    LFUCache: Implements a Least Frequently Used (LFU) caching algorithm.

    Inherits from BaseCaching and serves as
    a caching system with LFU eviction policy.
    """

    def __init__(self):
        """
        Initialize the LFUCache.
        """
        self.frequency_of_item = {}
        self.lfu_order = []
        super().__init__()

    def put(self, key, item):
        """
        Put a key/item pair into the cache, implementing LFU eviction policy.

        Args:
            key: The key for caching.
            item: The item to be cached.
        """
        if key is not None and item is not None:
            if key in self.cache_data:
                self.cache_data[key] = item
                self.frequency_of_item[key] += 1
                self.lfu_order.remove(key)
            else:
                if len(self.cache_data) >= self.MAX_ITEMS:
                    min_value = min(self.frequency_of_item.values())
                    min_keys = [keys for keys in self.frequency_of_item
                                if self.frequency_of_item[keys] == min_value]
                    for index in range(len(self.lfu_order)):
                        if self.lfu_order[index] in min_keys:
                            break
                    discarded_key = self.lfu_order.pop(index)
                    del self.cache_data[discarded_key]
                    del self.frequency_of_item[discarded_key]
                    print("DISCARD:", discarded_key)
                self.cache_data[key] = item
                self.frequency_of_item[key] = 1
            self.lfu_order.append(key)

    def get(self, key):
        """
        Get the value associated with the key from the cache.

        Args:
            key: The key for retrieving the cached item.

        Returns:
            The cached item linked to the key, or None if not found.
        """
        if key in self.cache_data:
            self.lfu_order.remove(key)
            self.lfu_order.append(key)
            self.frequency_of_item[key] += 1
            return self.cache_data[key]
        else:
            return None
