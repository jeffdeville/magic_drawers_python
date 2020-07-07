import pytest
from mycollections.deque import Deque


def test_deque_init():
    deque = Deque([], max_size=2)
    assert len(deque) == 0


def test_append():
    deque = Deque([], max_size=2)
    deque.append(1)
    deque.append(2)
    assert sum(deque) == 3

    deque.append(3)
    assert sum(deque) == 5

def test_indexing():
    deque = Deque([], max_size=2)
    deque.append(1)
    deque.append(2)
    assert deque[0] == 1
    assert deque[1] == 2
