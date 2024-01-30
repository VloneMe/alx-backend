#!/usr/bin/env python3
"""
LFUCache Module

This module defines the LFUCache class, which inherits from BaseCaching.
It implements a Least Frequently Used (LFU) caching algorithm.

"""

from base_caching import BaseCaching
from collections import OrderedDict


class LFUCache(BaseCaching):
    """
    LFUCache Class

    This caching system inherits from BaseCaching and
    implements an LFU algorithm.

    Methods:
    - __init__(): Initializes the LFUCache object.
    - put(key, item): Assigns the item to the cache using the LFU algorithm.
    - get(key): Returns the value linked to the given key.

    """

    def __init__(self):
        """
        __init__()

        Initializes the LFUCache object.

        Attributes:
        - lru_cache: Ordered dictionary to store
          the items in the cache with LRU order.
        - lfu_cache: Dictionary to store
          the frequency of each key in the cache.

        """
        super().__init__()
        self.lru_cache = OrderedDict()
        self.lfu_cache = {}

    def put(self, key, item):
        """
        put(key, item)

        Assigns the item to the cache using the LFU algorithm.

        Parameters:
        - key: The key for the caching.
        - item: The item to be cached.

        """
        if key in self.lru_cache:
            del self.lru_cache[key]
        if len(self.lru_cache) > BaseCaching.MAX_ITEMS - 1:
            min_value = min(self.lfu_cache.values())
            lfu_keys = [k for k, v in self.lfu_cache.items() if v == min_value]
            if len(lfu_keys) == 1:
                print("DISCARD:", lfu_keys[0])
                self.lru_cache.pop(lfu_keys[0])
                del self.lfu_cache[lfu_keys[0]]
            else:
                for k, _ in list(self.lru_cache.items()):
                    if k in lfu_keys:
                        print("DISCARD:", k)
                        self.lru_cache.pop(k)
                        del self.lfu_cache[k]
                        break
        self.lru_cache[key] = item
        self.lru_cache.move_to_end(key)
        if key in self.lfu_cache:
            self.lfu_cache[key] += 1
        else:
            self.lfu_cache[key] = 1
        self.cache_data = dict(self.lru_cache)

    def get(self, key):
        """
        get(key)

        Returns the value linked to the given key.

        Parameters:
        - key: The key for retrieving the cached item.

        Returns:
        The cached item linked to the key, or None if not found.

        """
        if key in self.lru_cache:
            value = self.lru_cache[key]
            self.lru_cache.move_to_end(key)
            if key in self.lfu_cache:
                self.lfu_cache[key] += 1
            else:
                self.lfu_cache[key] = 1
            return value
