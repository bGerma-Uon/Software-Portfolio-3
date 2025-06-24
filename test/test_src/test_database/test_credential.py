"""
Tests the database credential gatherers
"""

# Builtin
pass

# External
pass

# Internal
from src.database.credential import get_credential


class TestGetCredential:
    """
    Tests the get credential function
    """

    def test_get_credential(self) -> None:
        """
        Tests the get credential function
        """
        assert get_credential()
