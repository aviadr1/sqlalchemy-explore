from sqlalchemy import create_engine, MetaData, Column, Integer, DateTime, Numeric, NVARCHAR, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import pytest

import sqlalchemy_explore

metadata=MetaData()
Base = declarative_base(metadata=metadata)

class Bar(Base):
    __tablename__ = 'bars'

    Name = Column(NVARCHAR(120))
    Id = Column(Integer, primary_key=True)
    Date = Column(DateTime, nullable=False)
    Price = Column(Numeric(10, 2), nullable=False)

class Foo(Base):
    __tablename__ = 'foos'

    Name = Column(NVARCHAR(120))
    Id = Column(Integer, primary_key=True)
    Date = Column(DateTime, nullable=False)
    Price = Column(Numeric(10, 2), nullable=False)
    FriendId = Column(ForeignKey('bars.Id'), nullable=False, index=True)
    
    friend = relationship('Bar')


@pytest.fixture
def db_url():
    return 'sqlite:///test_dump.db'


@pytest.fixture
def engine(db_url):
    myengine = create_engine(db_url, echo=False)
    metadata.create_all(myengine)
    from sqlalchemy.orm import sessionmaker
    Session = sessionmaker(bind=myengine)
    session = Session()
    session.commit()
    return myengine

def test_dump(engine, db_url):
    output = sqlalchemy_explore.reflect_db(db_url)
    print(1, output)
    assert 'foos' in output
    assert 'bars' in output
    assert 'Name' in output
    assert 'Price' in output
    assert 'FriendId' in output

def test_dump_bitexact(engine, db_url):

    def trim_lines(s):
        return '\n'.join([line.strip() for line in s.splitlines() if len(line.strip()) > 0])
    expected = trim_lines("""
        CREATE TABLE bars (
            "Name" NVARCHAR(120),
            "Id" INTEGER NOT NULL,
            "Date" DATETIME NOT NULL,
            "Price" NUMERIC(10, 2) NOT NULL,
            PRIMARY KEY ("Id")
        )

        CREATE TABLE foos (
                "Name" NVARCHAR(120),
                "Id" INTEGER NOT NULL,
                "Date" DATETIME NOT NULL,
                "Price" NUMERIC(10, 2) NOT NULL,
                "FriendId" INTEGER NOT NULL,
                PRIMARY KEY ("Id"),
                FOREIGN KEY("FriendId") REFERENCES bars ("Id")
        )

        CREATE INDEX "ix_foos_FriendId" ON foos ("FriendId")
        """)
    output = trim_lines(sqlalchemy_explore.reflect_db(db_url))
    print(output)
    assert 'CREATE TABLE' in output
    assert output == expected
