from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from domain.models.base import Base  
from domain.models.competicion import Competicion

class Temporada(Base):
    __tablename__ = 'temporada'

    temporada_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    año_inicio = Column(Integer, nullable=False)
    año_fin = Column(Integer, nullable=False)

    # FK hacia Competición
    competicion_id = Column(Integer, ForeignKey('competicion.competicion_id'), nullable=False)

    # Relación inversa con Partido
    partidos = relationship("Partido", back_populates="temporada")

    # Relación directa con Competición
    competicion = relationship("Competicion", back_populates="temporadas")

    def __repr__(self):
        return f"<Temporada(id={self.temporada_id}, {self.año_inicio}-{self.año_fin}, competicion_id={self.competicion_id})>"
