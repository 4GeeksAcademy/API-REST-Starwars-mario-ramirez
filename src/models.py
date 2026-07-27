from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class User(db.Model):

    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    full_name: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "full_name": self.full_name,
            "is_active": self.is_active
            # do not serialize the password, its a security breach
        }

class Planets(db.Model):

    __tablename__ = 'planets'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    climate: Mapped[str] = mapped_column(String(80), nullable=True)
    terrain: Mapped[str] = mapped_column(String(80), nullable=True)
    population: Mapped[int | None] = mapped_column(BigInteger, nullable=True)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "terrain": self.terrain,
            "population": self.population,
        }

class People(db.Model):

    __tablename__ = 'people'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    birth_date: Mapped[str] = mapped_column(String(50), nullable=True)
    gender: Mapped[str] = mapped_column(String(50), nullable=False)
    height: Mapped[int | None] = mapped_column(nullable=True)
    mass: Mapped[int | None] = mapped_column(nullable=True)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "birth_date": self.birth_date,
            "gender": self.gender,
            "height": self.height,
            "mass": self.mass,
        }

class Favorites(db.Model):

    __tablename__ = 'favorites'

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    planets_id: Mapped[int | None] = mapped_column(ForeignKey('planets.id'), nullable= True)
    people_id: Mapped[int | None] = mapped_column(ForeignKey('people.id'), nullable=True) 

    user: Mapped["User"] = relationship()
    planets: Mapped["Planets"] = relationship()
    people: Mapped["People"] = relationship()

    def serialize(self):

        favorite_data = {
                        "id": self.id,
                        "user_id": self.user_id
                    }

        if self.planets:
            favorite_data["planets"] = self.planets.serialize()
        else:
            favorite_data["planets"] = None

        if self.people:
            favorite_data["people"] = self.people.serialize()
        else:
            favorite_data["people"] = None

        return favorite_data