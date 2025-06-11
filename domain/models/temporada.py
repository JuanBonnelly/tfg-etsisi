from sqlalchemy import Column, Integer, ForeignKey, String, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from domain.models.base import Base  
from domain.models.competicion import Competicion

class Temporada(Base):
    __tablename__ = 'temporada'

    temporada_id = Column(String(9), primary_key=True, nullable=False)
    año_inicio = Column(Integer, nullable=False)
    año_fin = Column(Integer, nullable=False)
    
    
    # pruebas sin foreing_keys
    #competicion_id = Column(Integer, nullable=False)
    
    
    # FK hacia Competición
    competicion_id = Column(Integer, ForeignKey('competicion.competicion_id'), nullable=False)

    # Relación inversa con Partido
    partidos = relationship("Partido", back_populates="temporada")

    # Relación directa con Competición
    competicion = relationship("Competicion", back_populates="temporadas")
    __table_args__ = (
        PrimaryKeyConstraint('temporada_id', 'competicion_id'),
    )
    
    def __repr__(self):
        return f"<Temporada(id={self.temporada_id}, {self.año_inicio}-{self.año_fin}, competicion_id={self.competicion_id})>"
