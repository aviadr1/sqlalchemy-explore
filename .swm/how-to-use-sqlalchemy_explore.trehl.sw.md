---
id: trehl
name: "How to use sqlalchemy_explore "
file_version: 1.0.2
app_version: 0.7.3-0
file_blobs:
  tests/test_reflective.py: 1a7d0abef8fea67d5c9465cdd0d6f77fcdfa786a
  sqlalchemy_explore/reflective.py: b28b0073dfb1dffd206ef23d62731b66157c53a7
  README.md: c9b027d84aea1e279ccf8542c0b6a8089bc49210
---

The `Base` class from SQLAlchemy does not afford automatically iterating over items in the class. here comes `sqlalchemy_explore` to the rescue!

define your base this way:

```
import sqlalchemy_explore
Base = declarative_base(cls=sqlalchemy_explore.ReflectiveMixin)
```

Now your class has a new `.sa_dict()` method which gives you access to a dictionary containing the column names

<br/>

<!-- NOTE-swimm-snippet: the lines below link your snippet to Swimm -->
### 📄 tests/test_reflective.py
```python
⬜ 81         assert empty_foobar.sa_dict()['Price'] is None
⬜ 82     
⬜ 83     
🟩 84     def test_foobar_dict_values(empty_foobar, foobar_name, foobar_date, foobar_price):
🟩 85         empty_foobar.Name = foobar_name
🟩 86         empty_foobar.Date = foobar_date
🟩 87         empty_foobar.Price = foobar_price 
🟩 88         print(empty_foobar)
🟩 89         print(empty_foobar.sa_dict())
🟩 90         assert empty_foobar.sa_dict()['Name'] == foobar_name
🟩 91         assert empty_foobar.sa_dict()['Date'] == foobar_date
🟩 92         assert empty_foobar.sa_dict()['Price'] == foobar_price
🟩 93     
⬜ 94     
⬜ 95     class Artist(Base2):
⬜ 96         __tablename__ = 'artists'
```

<br/>

<!-- NOTE-swimm-snippet: the lines below link your snippet to Swimm -->
### 📄 sqlalchemy_explore/reflective.py
```python
⬜ 1      from typing import List, Dict
⬜ 2      
🟩 3      class ReflectiveMixin:
⬜ 4          @staticmethod
⬜ 5          def sa_key_from_column(column_name):
⬜ 6              return column_name[column_name.rfind('.') +1:]
```

<br/>

please refer to `📄 README.md`for more examples

here's a picture of fish and loaves

<br/>

<div align="center"><img src="https://firebasestorage.googleapis.com/v0/b/swimmio-content/o/repositories%2FZ2l0aHViJTNBJTNBc3FsYWxjaGVteS1leHBsb3JlJTNBJTNBYXZpYWRyMQ%3D%3D%2Fb431ef26-7c31-4a5d-bc4a-3b1952250410.jpg?alt=media&token=ad44f059-d531-4312-9f8f-2548b91fd9a9" style="width:'50%'"/></div>

<br/>

<!-- NOTE-swimm-snippet: the lines below link your snippet to Swimm -->
### 📄 README.md
```markdown
⬜ 76     output:
⬜ 77     > `buy Album(AlbumId=1, Title='Come Away with Me', ArtistId=1)`
⬜ 78     
🟩 79     also you can iterate over a dict of column names/values in your object
🟩 80     ```
🟩 81     print(album.sa_dict())
🟩 82     ```
🟩 83     output:
🟩 84     > `{'AlbumId': 1, 'Title': 'Come Away with Me', 'ArtistId': 1}`
🟩 85     
🟩 86     
⬜ 87     ## Database exploration tool
⬜ 88     
⬜ 89     when using sqlalchemy_explore as a tool, it can dump the schema of database tables to help you figure out what's in the DB
```

<br/>

This file was generated by Swimm. [Click here to view it in the app](https://app.swimm.io/repos/Z2l0aHViJTNBJTNBc3FsYWxjaGVteS1leHBsb3JlJTNBJTNBYXZpYWRyMQ==/docs/trehl).