from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from db_config import DB_CONFIG

DB_URL = f"mysql+mysqlconnector://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}/{DB_CONFIG['database']}"

engine = create_engine(DB_URL)
Base = declarative_base()

class Committee(Base):
    __tablename__ = 'committee'

    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)
    address = Column(String(256), nullable=False)
    post_code = Column(String(6), nullable=False)
    city_id = Column(Integer, nullable=False)
    gmina_id = Column(Integer)
    powiat_id = Column(Integer)
    wojewodztwo_id = Column(Integer, nullable=False)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

with Session() as session:
    try:
        committees = session.query(Committee).all()

        for committee in committees:
            committee.address = committee.address.strip()

        session.commit()

    except Exception as e:
        print(f'Error: {e}')