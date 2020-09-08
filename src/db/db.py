from typing import Union
from datetime import datetime
import numpy as np

from sqlalchemy import event
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from ._secrets import db_config
from . import models
from . import schemas


class DBClient:

    def __init__(self,
                 db_user: str = db_config['user'],
                 db_pwd: str = db_config['password'],
                 db_host: str = db_config['host'],
                 db_port: int = db_config['port'],
                 db_name: str = db_config['database']) -> None:
        """Create connection to database

        Args:
            db_user (str, optional): database user name. Defaults to db_config['user'].
            db_pwd (str, optional): database password. Defaults to db_config['password'].
            db_host (str, optional): database host. Defaults to db_config['host'].
            db_port (str, optional): database port. Defaults to db_config['port'].
            db_name (str, optional): database name. Defaults to db_config['database'].
        """

        connection_str = f'mysql+pymysql://{db_user}:{db_pwd}@{db_host}:{db_port}/{db_name}'
        self.engine = create_engine(connection_str, echo=True)

        # any class inheriting Base that does not have a table in the db will have one generated for them
        models.Base.metadata.create_all(self.engine)

        # creates session objects if more needed (used in tests mainly)
        self._Session = sessionmaker(bind=self.engine)
        # session object to communicate with db
        self.session = self._Session()

        # some values are mapped to numpy int so need to convert
        # https://github.com/worldveil/dejavu/issues/142
        event.listen(self.engine, "before_cursor_execute", DBClient.add_own_encoders)

    @staticmethod
    def add_own_encoders(conn, cursor, query, *args):
        cursor.connection.encoders[np.int64] = lambda value, encoders: int(value)


class CommandDB:
    '''
    Write side
    '''

    def __init__(self, session: Session) -> None:
        self.session = session

    def _add_instance(self, instance: models.Base) -> int:
        """Handles all single instance additions to the database

        Args:
            instance (models.Base): instance of db_table that inherits Base

        Returns:
            int: instance id in table
        """
        self.session.add(instance)
        self.session.commit()
        self.session.refresh(instance)
        # any object being added to a table must have an id col
        return instance.id

    def add_player(self, player: schemas.PlayerCreate) -> int:
        """Add player to database

        Args:
            player (schemas.PlayerCreate): instance of player to add

        Returns:
            int: player id of added player
        """
        player = models.Player(**player.dict())
        return self._add_instance(player)

    def add_tournament(self, tournament: schemas.TournamentCreate) -> int:
        """Add tournament to database

        Args:
            tournament (schemas.TournamentCreate): instance of tournament to add

        Returns:
            int: tournament id of added tournament
        """
        tournament = models.Tournament(**tournament.dict())
        return self._add_instance(tournament)

    # def add_game(self, game: schemas.GameCreate, tourney_id: int, w_performance_id: int, l_performance_id: int) -> None:
    #     """Add game to database

    #     Args:
    #         game (_Game): instance of game
    #     """
    #     if game.circuit == 'wta':
    #         game = models.WTA(**game.dict(), tournament_id=tourney_id,
    #                           w_performance_id=w_performance_id, l_performance_id=l_performance_id)
    #     else:
    #         game = models.ITF(**game.dict(), tournament_id=tourney_id,
    #                           w_performance_id=w_performance_id, l_performance_id=l_performance_id)
    #     self._add_instance(game)

    # def add_performance(self, performance: schemas.PerformanceCreate, player_id: int) -> int:
    #     performance = models.Performance(**performance.dict(), player_id=player_id)
    #     self._add_instance(performance)
    #     self.session.refresh(performance)
    #     return performance.id


# class QueryDB:
#     '''
#     Read side
#     '''

#     def __init__(self, session: Session) -> None:
#         self.session = session

#     def get_player(self, name: str, dob: datetime) -> models.Player:
#         """Get player from database

#         Args:
#             first_name (str): player's first name
#             last_name (str): player's last name
#             dob (datetime): player's date of birth

#         Raises:
#             Exception: If multiple results found

#         Returns:
#             Player: instance of queried player
#         """
#         try:
#             return self.session.query(models.Player).\
#                 filter(models.Player.name == name).\
#                 filter(models.Player.dob == dob).one_or_none()
#         except MultipleResultsFound:
#             raise Exception("Multiple instances of same player found.")

#     def get_tournament(self, name: str, start_date: datetime) -> models.Tournament:
#         """Get tournament from database

#         Args:
#             name (str): tournament name
#             start_date (datetime): tournament start date

#         Raises:
#             Exception: If multiple results found

#         Returns:
#             Tournament: instance of queried tournamnet
#         """
#         try:
#             return self.session.query(models.Tournament).\
#                 filter(models.Tournament.name == name).\
#                 filter(models.Tournament.start_date == start_date).one_or_none()
#         except MultipleResultsFound:
#             raise Exception("Multiple instances of same tournament found.")

#     def get_game(self, tournament: models.Tournament, w_player: models.Player, l_player: models.Player) -> models._Game:
#         """Get game from database

#         Args:
#             tournament (Tournament): tournament object
#             w_player (Player): winning player object
#             l_player (Player): loseing player object

#         Raises:
#             Exception: If multiple results found

#         Returns:
#             _Game: instance of queried game
#         """
#         try:
#             return self.session.query(models._Game).\
#                 filter(models._Game.tournament == tournament).\
#                 filter(models._Game.w_performance.has(models.Performance.player == w_player)).\
#                 filter(models._Game.l_performance.has(models.Performance.player == l_player)).one_or_none()
#         except MultipleResultsFound:
#             raise Exception("Multiple instances of same game found.")
