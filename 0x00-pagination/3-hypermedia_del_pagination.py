#!/usr/bin/env python3
"""
Deletion-Resilient Hypermedia Pagination
"""

import csv
from typing import Dict, List


class Server:
    """Server class to paginate a database of
    popular baby names with deletion resilience.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        """Initialize the Server instance.
        """
        self.__dataset = None
        self.__indexed_dataset = None

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

    def indexed_dataset(self) -> Dict[int, List[str]]:
        """Create a dataset indexed by sorting position, starting at 0.

        Returns:
            Dict[int, List[str]]: The indexed dataset.
        """
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            truncated_dataset = dataset[:1000]
            self.__indexed_dataset = {
                    i: row for i, row in enumerate(truncated_dataset)
                    }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = None, page_size: int = 10) -> Dict:
        """Retrieve hypermedia-style pagination information from a given index.

        The goal is to ensure that if certain rows are removed from the dataset
        between two queries, the user does not miss items when changing pages.

        Args:
            index (int, optional): The start
            index of the current page (default is None).
            page_size (int, optional): The size of items required
            in the current page (default is 10).

        Returns:
            Dict[int, List[str], int, int]: A dictionary containing
            hypermedia-style pagination information.
        """
        focus = []
        dataset = self.indexed_dataset()
        index = 0 if index is None else index
        keys = sorted(dataset.keys())
        assert 0 <= index <= keys[-1]

        [focus.append(i) for i in keys if i >= index and
         len(focus) <= page_size]
        data = [dataset[v] for v in focus[:-1]]
        next_index = focus[-1] if len(focus) - page_size == 1 else None

        return {'index': index, 'data': data, 'page_size': len(data),
                'next_index': next_index}
