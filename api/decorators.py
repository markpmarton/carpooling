"""
Custom decorator to ensure the journeys is the waiting
list is checked if the global car capacity is changed.

The waiting list can be check before or after the
decorated funcion.
"""

from models.data import Journey


def run_waiting_list_after(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        Journey.run_waiting_list()
        return result

    return wrapper


def run_waiting_list_before(func):
    def wrapper(*args, **kwargs):
        Journey.run_waiting_list()
        result = func(*args, **kwargs)
        return result

    return wrapper
