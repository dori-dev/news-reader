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

## Install Redis

Install redis from [here](https://redis.io/docs/getting-started/installation/)
After installing redis run redis server

```
redis-server --daemonize yes
```

Then test redis

```
$ redis-cli ping
PONG
```

## Run Project

Run project using this command

```
python manage.py runserver
```

Open _another terminal_ in **this path** then run `celery worker`

```
source env/bin/activate
```

```
python -m celery -A config worker -l info
```

And open _another terminal_ in **this path** then run `celery beat`:

```
source env/bin/activate
```

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
