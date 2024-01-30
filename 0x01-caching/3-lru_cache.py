#!/usr/bin/env python3
"""
LRUCache Module

This module defines the LRUCache class, which inherits from BaseCaching.
It implements a Least Recently Used (LRU) caching algorithm.

"""

from base_caching import BaseCaching


class LRUCache(BaseCaching):
    """
    LRUCache Class

    This caching system inherits from BaseCaching and
    implements an LRU algorithm.

    Methods:
    - __init__(): Initializes the LRUCache object.
    - handle(head, tail): Handles the linked list structure for LRU.
    - _remove(key): Removes an element from the cache based on LRU.
    - _add(key, item): Adds a new element to the cache based on LRU.
    - put(key, item): Assigns the item to the cache using the LRU algorithm.
    - get(key): Returns the value linked to the given key.

    """

    def __init__(self):
        """
        __init__()

        Initializes the LRUCache object.

        Attributes:
        - head: Symbol representing the start of the linked list.
        - tail: Symbol representing the end of the linked list.
        - next: Dictionary to store the next element in the linked list.
        - prev: Dictionary to store the previous element in the linked list.

        """
        super().__init__()
        self.head, self.tail = '-', '='
        self.next, self.prev = {}, {}
        self.handle(self.head, self.tail)

    def handle(self, head, tail):
        """
        handle(head, tail)

        Handles the linked list structure for LRU.

        Parameters:
        - head: The symbol representing the start of the linked list.
        - tail: The symbol representing the end of the linked list.

        """
        self.next[head], self.prev[tail] = tail, head

    def _remove(self, key):
        """
        _remove(key)

        Removes an element from the cache based on LRU.

        Parameters:
        - key: The key of the element to be removed.

        """
        self.handle(self.prev[key], self.next[key])
        del self.prev[key], self.next[key], self.cache_data[key]

    def _add(self, key, item):
        """
        _add(key, item)

        Adds a new element to the cache based on LRU.

        Parameters:
        - key: The key for the caching.
        - item: The item to be cached.

        """
        self.cache_data[key] = item
        self.handle(self.prev[self.tail], key)
        self.handle(key, self.tail)
        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            print("DISCARD: {}".format(self.next[self.head]))
            self._remove(self.next[self.head])

    def put(self, key, item):
        """
        put(key, item)

        Assigns the item to the cache using the LRU algorithm.

        Parameters:
        - key: The key for the caching.
        - item: The item to be cached.

        """
        if key and item:
            if key in self.cache_data:
                self._remove(key)
            self._add(key, item)

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
            self._remove(key)
            self._add(key, value)
            return value
