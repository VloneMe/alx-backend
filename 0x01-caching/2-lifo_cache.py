#!/usr/bin/env python3
"""
LIFOCache Module

This module defines the LIFOCache class, which inherits from BaseCaching.
It implements a Last-In-First-Out (LIFO) caching algorithm.

"""

from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """
    LIFOCache Class

    This caching system inherits from BaseCaching and
    implements a LIFO algorithm.

    Methods:
    - __init__(): Initializes the LIFOCache object.
    - put(key, item): Assigns the item to the cache using the LIFO algorithm.
    - get(key): Returns the value linked to the given key.

    """

    def __init__(self):
        """
        __init__()

        Initializes the LIFOCache object.

        Attributes:
        - last_key: Keeps track of the last key added.

        """
        super().__init__()
        self.last_key = ''

    def put(self, key, item):
        """
        put(key, item)

        Assigns the item to the cache using the LIFO algorithm.

        Parameters:
        - key: The key for the caching.
        - item: The item to be cached.

        """
        if key and item:
            self.cache_data[key] = item
            if len(self.cache_data) > BaseCaching.MAX_ITEMS:
                print("DISCARD: {}".format(self.last_key))
                self.cache_data.pop(self.last_key)
            self.last_key = key

    def get(self, key):
        """
        get(key)

        Returns the value linked to the given key.

        Parameters:
        - key: The key for retrieving the cached item.

        Returns:
        The cached item linked to the key, or None if not found.

        """
        if key is None or self.cache_data.get(key) is None:
            return None
        if key in self.cache_data:
            value = self.cache_data[key]
            return value
