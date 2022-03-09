from typing import List

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config.config import settings
from rentomatic.domain.room import Room
from rentomatic.repository.constants import FiltersEnum
from rentomatic.repository.postgres.postgres_objects import Base, RoomPostgres


class PostgresRepo:
    def __init__(self) -> None:
        self.engine = create_engine(settings.POSTGRES_URI)
        Base.metadata.create_all(self.engine)
        Base.metadata.bind = self.engine

    def _create_room_objects(
        self, *, results: List[RoomPostgres]
    ) -> List[Room]:
        room_objects = [
            Room(
                code=result.code,
                size=result.size,
                price=result.price,
                latitude=result.latitude,
                longitude=result.longitude,
            )
            for result in results
        ]
        return room_objects

    def list(self, *, filters=None) -> List[Room]:
        DBSession = sessionmaker(bind=self.engine)
        session = DBSession()
        query = session.query(RoomPostgres)

        if filters is None:
            return self._create_room_objects(results=query.all())

        if FiltersEnum.CODE__EQ in filters:
            query = query.filter(
                RoomPostgres.code == filters[FiltersEnum.CODE__EQ]
            )

        if FiltersEnum.PRICE__EQ in filters:
            query = query.filter(
                RoomPostgres.price == filters[FiltersEnum.PRICE__EQ]
            )

        if FiltersEnum.PRICE__LT in filters:
            query = query.filter(
                RoomPostgres.price < int(filters[FiltersEnum.PRICE__LT])
            )

        if FiltersEnum.PRICE__GT in filters:
            query = query.filter(
                RoomPostgres.price > int(filters[FiltersEnum.PRICE__GT])
            )

        return self._create_room_objects(results=query.all())
