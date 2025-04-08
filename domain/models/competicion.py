from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from domain.models.base import Base

class Competicion(Base):
    __tablename__ = 'competicion'

    competicion_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    nombre = Column(String(100), nullable=False)
    abreviatura = Column(String(10), nullable=False)

    # Relación con Temporada
    temporadas = relationship("Temporada", back_populates="competicion")

    def __repr__(self):
        return f"<Competicion(id={self.competicion_id}, nombre={self.nombre} , abreviatura={self.abreviatura})>"
