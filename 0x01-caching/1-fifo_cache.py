#!/usr/bin/env python3
"""
FIFOCache Module

This module defines the FIFOCache class, which inherits from BaseCaching.
It implements a First-In-First-Out (FIFO) caching algorithm.

"""

from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """
    FIFOCache Class

    This caching system inherits from BaseCaching and
    implements a FIFO algorithm.

    Methods:
    - __init__(): Initializes the FIFOCache object.
    - _pop(): Removes the oldest element based on FIFO algorithm.
    - _push(key, item): Adds a new element to the cache
      based on FIFO algorithm.
    - put(key, item): Assigns the item to the cache using the FIFO algorithm.
    - get(key): Returns the value linked to the given key.

    """

    def __init__(self):
        """
        __init__()

        Initializes the FIFOCache object.

        Attributes:
        - data: Dictionary to store the order of keys based on FIFO.
        - next_in: Index for the next key to be added.
        - next_out: Index for the next key to be removed.

        """
        super().__init__()
        self.data = {}
        self.next_in, self.next_out = 0, 0

    def _pop(self):
        """
        _pop()

        FIFO algorithm - Removes the oldest element.

        """
        self.next_out += 1
        key = self.data[self.next_out]
        del self.data[self.next_out], self.cache_data[key]

    def _push(self, key, item):
        """
        _push(key, item)

        FIFO algorithm - Adds a new element to the cache.

        Parameters:
        - key: The key for the caching.
        - item: The item to be cached.

        """
        if len(self.cache_data) > BaseCaching.MAX_ITEMS - 1:
            print("DISCARD: {}".format(self.data[self.next_out + 1]))
            self._pop()
        self.cache_data[key] = item
        self.next_in += 1
        self.data[self.next_in] = key

    def put(self, key, item):
        """
        put(key, item)

        Assigns the item to the cache using the FIFO algorithm.

        Parameters:
        - key: The key for the caching.
        - item: The item to be cached.

        """
        if key and item:
            if key in self.cache_data:
                self.cache_data[key] = item
            else:
                self._push(key, item)

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
