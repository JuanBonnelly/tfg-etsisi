from sqlalchemy import Column, String, Float, Integer
from domain.models.base import Base

class EstadisticasPartidoCSV(Base):
    __tablename__ = 'estadisticas_partido_csv'


    partido_id = Column(String(20), primary_key=True)
    equipo_id = Column(String(20), primary_key=True)

    posesion = Column('posesion', Float)
    corners = Column('corners', Integer)
    amarillas = Column('amarillas', Integer)
    rojas = Column('rojas', Integer)
