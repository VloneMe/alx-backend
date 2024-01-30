#!/usr/bin/env python3
"""Task 3: Deletion-Resilient Hypermedia Pagination

This module extends the hypermedia pagination mechanism to support retrieval of
information from a specific index in a dataset of popular baby names.
"""

import csv
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
    """Server class for paginating a database of popular baby names with deletion resilience.
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

    def get_hyper_index(self, index: int = None, page_size: int = 10) -> Dict:
        """Retrieve information about a page from a given index with a specified size.

        Args:
            index (int, optional): The starting index (default is None).
            page_size (int, optional): The number of items per page (default is 10).

        Returns:
            Dict: A dictionary containing hypermedia-style pagination information.
        """
        data = self.indexed_dataset()
        assert index is not None and 0 <= index <= max(data.keys())
        page_data = []
        data_count = 0
        next_index = None
        start = index if index else 0
        for i, item in data.items():
            if i >= start and data_count < page_size:
                page_data.append(item)
                data_count += 1
                continue
            if data_count == page_size:
                next_index = i
                break
        page_info = {
            'index': index,
            'next_index': next_index,
            'page_size': len(page_data),
            'data': page_data,
        }
        return page_info
