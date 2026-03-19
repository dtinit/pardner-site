import pytest


def pytest_collection_modifyitems(items):
    # Automatically adds django_db marker to all test functions
    for item in items:
        item.add_marker(pytest.mark.django_db)
