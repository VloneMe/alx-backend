#!/usr/bin/env python3
"""
BasicCache Module

This module defines the BasicCache class, which inherits from BaseCaching.
It is a caching system without a limit.

"""

from base_caching import BaseCaching


class BasicCache(BaseCaching):
    """
    BasicCache Class

    This caching system inherits from BaseCaching and doesn't have a limit.

    Methods:
    - put(key, item): Assigns the item to the dictionary.
    - get(key): Returns the value linked to the given key.

    """

    def put(self, key, item):
        """
        put(key, item)

        Assigns the item to the dictionary.

        Parameters:
        - key: The key for the caching.
        - item: The item to be cached.

        """

        if key and item:
            self.cache_data[key] = item

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
        return self.cache_data.get(key)
