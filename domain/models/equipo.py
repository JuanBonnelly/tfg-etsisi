from sqlalchemy import Column, Integer, String
from domain.models.base import Base

class Equipo(Base):
    __tablename__ = "equipo"

    equipo_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    nombre = Column(String(100), nullable=False)
    abreviatura = Column(String(10), nullable=False)

    def __repr__(self):
        return f"<Equipo(id={self.equipo_id}, nombre='{self.nombre}', abreviatura='{self.abreviatura}')>"
