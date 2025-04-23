from sqlalchemy import Column, Integer, Date, ForeignKey, String
from sqlalchemy.orm import relationship
from domain.models.base import Base
from domain.models.equipo import Equipo
from domain.models.temporada import Temporada      
from domain.models.competicion import Competicion

class Partido(Base):
    __tablename__ = 'partido'

    partido_id = Column(String(20), primary_key=True, nullable=False)
    fecha = Column(Date, nullable=False)

    #equipo_local_id = Column(String(20), ForeignKey('equipo.equipo_id'), nullable=False)
    #equipo_visitante_id = Column(String(20), ForeignKey('equipo.equipo_id'), nullable=False)

    equipo_local_id = Column(String(20),  nullable=False)
    equipo_visitante_id = Column(String(20),  nullable=False)

    goles_local = Column(Integer, nullable=True)
    goles_visitante = Column(Integer, nullable=True)

    #temporada_id = Column(Integer, ForeignKey('temporada.temporada_id'), nullable=False)
    #competicion_id = Column(Integer, ForeignKey('competicion.competicion_id'), nullable=False)
    temporada_id = Column(Integer,nullable=False)
    competicion_id = Column(Integer, nullable=False)
    # Relaciones ORM
    #equipo_local = relationship("Equipo", foreign_keys=[equipo_local_id])
    #equipo_visitante = relationship("Equipo", foreign_keys=[equipo_visitante_id])
    #temporada = relationship("Temporada")
    #competicion = relationship("Competicion")
    #estadisticas = relationship("EstadisticasPartido", uselist=False, back_populates="partido")


    def __repr__(self):
        return (
            f"<Partido(id={self.partido_id}, fecha={self.fecha}, "
            f"local={self.equipo_local_id}, visitante={self.equipo_visitante_id}, "
            f"goles_local={self.goles_local}, goles_visitante={self.goles_visitante}, "
            f"temporada_id={self.temporada_id}, competicion_id={self.competicion_id})>"
        )
