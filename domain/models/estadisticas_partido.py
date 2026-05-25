from sqlalchemy import Column, Integer, ForeignKey, Float, String
from sqlalchemy.orm import relationship
from domain.models.base import Base


class EstadisticasPartido(Base):
    __tablename__ = 'estadisticas_partido'

    estadisticas_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    partido_id = Column(String(20), ForeignKey('partido.partido_id'), nullable=False, unique=True)
    
    posesion_local = Column(Float, nullable=True)
    posesion_visitante = Column(Float, nullable=True)
    
    
    tiros_local = Column(Integer, nullable=True)
    tiros_visitante = Column(Integer, nullable=True)

    tiros_puerta_local = Column(Integer, nullable=True)
    tiros_puerta_visitante = Column(Integer, nullable=True)

    corners_local = Column(Integer, nullable=True)
    corners_visitante = Column(Integer, nullable=True)

    tarjetas_amarillas_local = Column(Integer, nullable=True)
    tarjetas_amarillas_visitante = Column(Integer, nullable=True)

    tarjetas_rojas_local = Column(Integer, nullable=True)
    tarjetas_rojas_visitante = Column(Integer, nullable=True)

    
    partido = relationship("Partido", back_populates="estadisticas")

    def __repr__(self):
        return f"<EstadisticasPartido(id={self.estadisticas_id}, partido_id={self.partido_id})>"
