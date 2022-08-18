# Django News Reader

Advanced news reader website using django and celery.

#

# How to Run Project

## Download Codes

```
git clone https://github.com/dori-dev/news-reader.git
```

```
cd news-reader
```

## Build Virtual Environment

```
python -m venv env
```

```
source env/bin/activate
```

## Install Project Requirements

```
pip install -r requirements.txt
```

## Set Environ Variables

rename `.env.example` to `.env` and change values.<br>

```
mv .env.example .env
```

set your environment variables in `.env` file.

## Migrate Models

```
python manage.py makemigrations news taggit
```

```
python manage.py migrate
```

## Add Super User

```
python manage.py createsuperuser
```

## Run Project

run project using this command

```
python manage.py runserver
```

open _another terminal_ in **this path** then run `celery worker`

```
python -m celery -A config worker -l info
```

and open _another terminal_ in **this path** then run `celery beat`:

```
python -m celery -A config beat -l info

```

## Open On Browser

Home Page: [127.0.0.1:8000](http://127.0.0.1:8000/)<br>
Admin Page: [127.0.0.1:8000/admin](http://127.0.0.1:8000/admin/)

#

## Links

Download Source Code: [Click Here](https://github.com/dori-dev/news-reader/archive/refs/heads/master.zip)

My Github Account: [Click Here](https://github.com/dori-dev/)
