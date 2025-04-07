from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from domain.models.base import Base

class Equipo(Base):
    __tablename__ = "equipo"

    equipo_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    nombre = Column(String(100), nullable=False)
    abreviatura = Column(String(10), nullable=False)

    # Relaciones con Partido
    partidos_local = relationship("Partido", back_populates="equipo_local", foreign_keys='Partido.equipo_local_id')
    partidos_visitante = relationship("Partido", back_populates="equipo_visitante", foreign_keys='Partido.equipo_visitante_id')
    
    def __repr__(self):
        return f"<Equipo(id={self.equipo_id}, nombre='{self.nombre}', abreviatura='{self.abreviatura}')>"
