from sqlalchemy import Column, DateTime, ForeignKey, Integer, NVARCHAR, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime
import pytest

import sqlalchemy_explore

Base1 = sqlalchemy_explore.reflective(declarative_base())
Base2 = declarative_base(cls=sqlalchemy_explore.ReflectiveMixin)

class FooBar1(Base1):
    __tablename__ = 'foobars1'

    Name = Column(NVARCHAR(120))
    Id = Column(Integer, primary_key=True)
    Date = Column(DateTime, nullable=False)
    Price = Column(Numeric(10, 2), nullable=False)
    FriendId = Column(ForeignKey('foobars1.Id'), nullable=False, index=True)
    
    friend = relationship('FooBar1')

class FooBar2(Base2):
    __tablename__ = 'foobars2'

    Name = Column(NVARCHAR(120))
    Id = Column(Integer, primary_key=True)
    Date = Column(DateTime, nullable=False)
    Price = Column(Numeric(10, 2), nullable=False)
    FriendId = Column(ForeignKey('foobars2.Id'), nullable=False, index=True)
    
    friend = relationship('FooBar2')

@pytest.fixture
def foobar_name():
    return "my foobar"

@pytest.fixture(params=[FooBar1, FooBar2])
def empty_foobar(request):
    class_ = request.param
    return class_()

@pytest.fixture
def foobar_date():
    return datetime.datetime(year=2019, month=7, day=4)

@pytest.fixture
def foobar_price():
    return 0.99


def test_base_functions():
    assert Base1.sa_keys is not None
    assert Base1.sa_dict is not None
    assert Base1.__repr__ is not None

    assert Base2.sa_keys is not None
    assert Base2.sa_dict is not None
    assert Base2.__repr__ is not None


def test_foobar_keys(empty_foobar):
    assert 'Id' in empty_foobar.sa_keys()
    assert 'Name' in empty_foobar.sa_keys()
    assert 'Date' in empty_foobar.sa_keys()
    assert 'Price' in empty_foobar.sa_keys()
    assert 'FriendId' in empty_foobar.sa_keys()
    assert len(empty_foobar.sa_keys()) == 5

def test_foobar_dict_keys(empty_foobar):
    assert 'Id' in empty_foobar.sa_dict()
    assert 'Name' in empty_foobar.sa_dict()
    assert 'Date' in empty_foobar.sa_dict()
    assert 'Price' in empty_foobar.sa_dict()
    assert 'FriendId' in empty_foobar.sa_dict()
    assert len(empty_foobar.sa_dict()) == 5

def test_empty_foobar_dict_values(empty_foobar):
    assert empty_foobar.sa_dict()['Name'] is None
    assert empty_foobar.sa_dict()['Date'] is None
    assert empty_foobar.sa_dict()['Price'] is None


def test_foobar_dict_values(empty_foobar, foobar_name, foobar_date, foobar_price):
    empty_foobar.Name = foobar_name
    empty_foobar.Date = foobar_date
    empty_foobar.Price = foobar_price 
    print(empty_foobar)
    print(empty_foobar.sa_dict())
    assert empty_foobar.sa_dict()['Name'] == foobar_name
    assert empty_foobar.sa_dict()['Date'] == foobar_date
    assert empty_foobar.sa_dict()['Price'] == foobar_price


class Artist(Base2):
    __tablename__ = 'artists'

    ArtistId = Column(Integer, primary_key=True)
    Name = Column(NVARCHAR(120))


class Album(Base2):
    __tablename__ = 'albums'

    AlbumId = Column(Integer, primary_key=True)
    Title = Column(NVARCHAR(160), nullable=False)
    ArtistId = Column(ForeignKey('artists.ArtistId'), nullable=False, index=True)

    artist = relationship('Artist')

def test_artist():
    artist = Artist(ArtistId=1, Name='Norah Jones')
    output = repr(artist)
    assert output == "Artist(ArtistId=1, Name='Norah Jones')"

    album = Album(AlbumId=1, Title='Come Away with Me', ArtistId=artist.ArtistId)
    output = repr(album)
    assert output == "Album(AlbumId=1, Title='Come Away with Me', ArtistId=1)"

    output = repr(album.sa_dict())
    assert output == """{'AlbumId': 1, 'Title': 'Come Away with Me', 'ArtistId': 1}"""
