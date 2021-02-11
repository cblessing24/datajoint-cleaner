"""Contains the PyMySQL gateway."""
from typing import Any, Dict, Set
from uuid import UUID

from ..use_cases.interfaces import AbstractDatabaseGateway
from .interfaces import PyMySQLFacade


class PyMySQLGateway(AbstractDatabaseGateway):
    """Gateway between the PyMySQL facade and the use cases."""

    def __init__(self, facade: PyMySQLFacade, config: Dict[str, str]) -> None:
        """Initialize PyMySQLGateway."""
        self.facade = facade
        self.config = config

    def configure(self, config: Any) -> None:
        """Configure the gateway."""
        self.facade.configure(config)

    def get_ids(self) -> Set[UUID]:
        """Get the IDs of entities stored in the external table."""
        external_table_name = "~external_" + self.config["store_name"]
        sql = f"SELECT `hash` from `{external_table_name}`"
        hashes = self.facade.execute(self.config["schema_name"], sql)
        object_ids = {UUID(bytes=h["hash"]) for h in hashes}
        return object_ids

    def __repr__(self) -> str:
        """Return a string representation of the object."""
        return f"{self.__class__.__name__}(facade={self.facade}, config={self.config})"
