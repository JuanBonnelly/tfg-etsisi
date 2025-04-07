from sqlalchemy import Column, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship
from domain.models.base import Base
from domain.models.equipo import Equipo
#from domain.models.temporada import Temporada     No Estan creados aun 
#from domain.models.competicion import Competicion

class Partido(Base):
    __tablename__ = 'partido'

    partido_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    fecha = Column(Date, nullable=False)

    equipo_local_id = Column(Integer, ForeignKey('equipo.equipo_id'), nullable=False)
    equipo_visitante_id = Column(Integer, ForeignKey('equipo.equipo_id'), nullable=False)

    goles_local = Column(Integer, nullable=True)
    goles_visitante = Column(Integer, nullable=True)

    # temporada_id = Column(Integer, ForeignKey('temporada.temporada_id'), nullable=False)
    # competicion_id = Column(Integer, ForeignKey('competicion.competicion_id'), nullable=False)

    temporada_id = Column(Integer, nullable=False)     # Temporal hasta que se cree Temporada
    competicion_id = Column(Integer, nullable=False)   # Temporal hasta que se cree Competicion


    # Relaciones ORM
    equipo_local = relationship("Equipo", foreign_keys=[equipo_local_id])
    equipo_visitante = relationship("Equipo", foreign_keys=[equipo_visitante_id])
    #temporada = relationship("Temporada")
    #competicion = relationship("Competicion")

    def __repr__(self):
        return (
            f"<Partido(id={self.partido_id}, fecha={self.fecha}, "
            f"local={self.equipo_local_id}, visitante={self.equipo_visitante_id}, "
            f"goles_local={self.goles_local}, goles_visitante={self.goles_visitante}, "
            f"temporada_id={self.temporada_id}, competicion_id={self.competicion_id})>"
        )
