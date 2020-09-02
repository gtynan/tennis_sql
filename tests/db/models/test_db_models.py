import pytest
import numpy as np
from sqlalchemy import inspect

from tests.conftest import TEST_DB
from src.db.models.player import Player
from src.db.models.game import _Game, WTA, ITF
from src.db.models.tournament import Tournament
from src.db.models.performance import Performance


# TODO dynamically pull all classes from db_models
# tables to check for in TestDBClient test_schema
TABLE_CLASSES = [Player(), _Game(), WTA(), ITF(), Tournament(), Performance()]


class TestDBModels:

    def test_schema(self, db_client):
        '''
        Ensure all tables in the src/db/tables module with Base parent are in the database
        '''
        db_inspector = inspect(db_client.engine)
        db_tables = db_inspector.get_table_names()

        # ensure expected tables present
        assert np.isin(
            [table.__tablename__ for table in TABLE_CLASSES],
            db_tables).all()

        # ensure table matches expected schema
        for table_class in TABLE_CLASSES:
            for db_column in db_inspector.get_columns(table_class.__tablename__):
                assert hasattr(table_class, db_column['name'])