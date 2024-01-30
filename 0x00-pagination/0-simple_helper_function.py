#!/usr/bin/env python3
"""Pagination helper function.

This module provides a function to calculate the index range for a given page
and page size in a paginated data set.

Author: Your Name
"""

from typing import Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """Retrieves the index range for a given page and page size.

    Args:
        page (int): The current page number.
        page_size (int): The number of items per page.

    Returns:
        Tuple[int, int]: A tuple representing the start and end indices
        of the requested page.
    """
    return ((page - 1) * page_size, ((page - 1) * page_size) + page_size)
