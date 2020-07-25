### Bookshelf
---
##### I'don't read much but i have an obsession with being over organized.
---
#### if you want to use it for yourself, do this steps:
```
git clone https://github.com/mohammadekhosravi/Bookshelf.git && cd Bookshelf
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt

export FLASK_APP=app.py # set app to FLASK_APP config variable.
flask shell # enter flask shell

from app import db
db.create_all() # create Data Base.

exit() # exit the flask shell

flask run # run the application. now go to site and make your own list.
```

<p> P.S: i'm aware that we already have goodreads for this purpose but i just want my own simple version.</p>
<p> Another P.S: single file application are evil but <strong>If the shoe fits, then wear it.</strong></p>
