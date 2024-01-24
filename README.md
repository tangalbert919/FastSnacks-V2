# FastSnacks-V2

This is a reconstruction of a university project I did with a few others, but with Django instead of ExpressJS.
The original version can be found [here](https://github.com/ethangbeltran/SE3354-Group-Project).

## How to setup

You must have Python 3 installed on your machine. Setting up a virtual environment is recommended.

Open a command shell in this directory and run:

```
python -m pip install -r requirements.txt
```

To start the server, `cd` into the FastSnacks directory, start the migrations (this will setup the database), and then run the server:

```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

You should be able to view the website at `http://127.0.0.1:8000`.
