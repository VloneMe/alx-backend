#!/usr/bin/env python3
"""Task 2: Hypermedia Pagination

This module extends the simple pagination mechanism to provide hypermedia-style
pagination information for a dataset of popular baby names.
"""

import csv
import math
from typing import Dict, List, Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """Calculate the index range for a given page and page size.

    Args:
        page (int): The current page number.
        page_size (int): The number of items per page.

    Returns:
        Tuple[int, int]: A tuple representing the start and end indices of the requested page.
    """
    return ((page - 1) * page_size, ((page - 1) * page_size) + page_size)


class Server:
    """Server class for paginating a database of popular baby names with hypermedia support.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        """Initialize the Server instance.
        """
        self.__dataset = None

    def dataset(self) -> List[List[str]]:
        """Retrieve the cached dataset.

        Returns:
            List[List[str]]: The dataset containing popular baby names.
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List[str]]:
        """Retrieve a page of data from the dataset.

        Args:
            page (int, optional): The page number to retrieve (default is 1).
            page_size (int, optional): The number of items per page (default is 10).

        Returns:
            List[List[str]]: The data for the requested page.
        """
        assert isinstance(page, int) and isinstance(page_size, int)
        assert page > 0 and page_size > 0
        start, end = index_range(page, page_size)
        data = self.dataset()
        if start > len(data):
            return []
        return data[start:end]

    def get_hyper(self, page: int = 1, page_size: int = 10) -> Dict:
        """Retrieve hypermedia-style pagination information for a page.

        Args:
            page (int, optional): The page number to retrieve (default is 1).
            page_size (int, optional): The number of items per page (default is 10).

        Returns:
            Dict: A dictionary containing hypermedia-style pagination information.
        """
        data = self.get_page(page, page_size)
        start, end = index_range(page, page_size)
        total_pages = math.ceil(len(self.__dataset) / page_size)
        return {
            'page_size': len(data),
            'page': page,
            'data': data,
            'next_page': page + 1 if end < len(self.__dataset) else None,
            'prev_page': page - 1 if start > 0 else None,
            'total_pages': total_pages
        }
