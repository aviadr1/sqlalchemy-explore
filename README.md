# sqlalchemy_explore
tools for exploring databases using sqlalchemy

## installation

> ``` 
> pip install sqlalchemy_explore
> ```

## Features

1. Base class for relective usage of classes
2. Database exploration tool

## Base class for relective usage of classes

### Usage

Make the declarative base clsss provided by SQLAlchemy derive from `sqlalchemy_explore.ReflectiveMixin`

```python
import sqlalchemy_explore
Base = declarative_base(cls=cls=sqlalchemy_explore.ReflectiveMixin)
```

now all of your instances support the following functions:
* `sa_keys()` - returns the keys/column names that SQLAlchemy is mapping
* `sa_dict()` - return key/value pairs of all the columns in the object
* `__repr__()` - str represetation of the object that includes all the columns

### Example
Imagine you have a couple of classes represnting tables in SQLAlchemy 

```python
Base = declarative_base()

class Artist(Base):
    __tablename__ = 'artists'

    ArtistId = Column(Integer, primary_key=True)
    Name = Column(NVARCHAR(120))


class Album(Base):
    __tablename__ = 'albums'

    AlbumId = Column(Integer, primary_key=True)
    Title = Column(NVARCHAR(160), nullable=False)
    ArtistId = Column(ForeignKey('artists.ArtistId'), nullable=False, index=True)

    artist = relationship('Artist')
```

dynamiclly iterating through the column names and values of a mapped object requires a lot of boiler plate code.
but `sqlalchemy_explore` lets you do this very easily. to enable it on your classes 

```python
import sqlalchemy_explore
Base = declarative_base(cls=cls=sqlalchemy_explore.ReflectiveMixin)
```

and continue having your classes inherit from Base.

now formatted printing is avaiable to all your objects
```
artist = Artist(ArtistId=1, Name='Norah Jones')
print('hello', artist)
```
output:
> `hello Artist(ArtistId=1, Name='Norah Jones')`

```
album = Album(AlbumId=1, Title='Come Away with Me', ArtistId=artist.ArtistId)
print('buy', album)
```
output:
> `buy Album(AlbumId=1, Title='Come Away with Me', ArtistId=1)`

also you can iterate over a dict of column names/values in your object
```
print(album.sa_dict())
```
output:
> `{'AlbumId': 1, 'Title': 'Come Away with Me', 'ArtistId': 1}`


## Database exploration tool

when using sqlalchemy_explore as a tool, it can dump the schema of database tables to help you figure out what's in the DB

At the minimum, you have to give sqlalchemy_explore a database URL or a path to a local sqlite database. The URL is passed directly to SQLAlchemy’s create_engine() method so please refer to SQLAlchemy’s documentation for instructions on how to construct a proper URL.

Examples:

> ``` 
> python -m sqlalchemy_explore database.db
> python -m sqlalchemy_explore postgresql:///some_local_db
> python -m sqlalchemy_explore mysql+oursql://user:password@localhost/dbname
> python -m sqlalchemy_explore sqlite:///database.db
> ```