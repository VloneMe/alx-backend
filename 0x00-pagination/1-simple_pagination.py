#!/usr/bin/env python3
"""Task 1: Simple Pagination

This module implements a simple pagination mechanism for a dataset of popular baby names.
"""

import csv
from typing import List, Tuple


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
    """Server class for paginating a database of popular baby names.
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
