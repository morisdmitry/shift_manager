# Shift_manager

# Features

- Used application factory pattern
- Used .env file for loading configuration

- if is shift between 2022-08-09 23.50.00 and 2022-08-10 00.10.00 will create two notes in data base
- check overlapping time per day per employee
- Not possible to register more than 24 hours per day per employee
- Unable to record shift if there is a newer date

For the application to work correctly, you need

- python not less pyhton3.8
- docker (or you able to start locally)

# How to start?

- make your .env file. Just copy .env.test and remove the .test at the end.
- Set values on your .env file

### mailgun

`MG_API = ""`
`MG_LINK = ""`
`MG_MAIL = ""`

### aws

`AWS_ACCESS_KEY_ID = ""`
`AWS_SECRET_ACCESS_KEY = ""`
`S3_BUCKET = ""`

- in root path make commands:
  `docker-compose build`
  `docker-compose up -d`
- update your database
  `docker-compose exec web flask db upgrade`

- go to `http://127.0.0.1:4000/api/`
- POST /api/timeshits/ for add shift
- GET /api/timeshits/monthly/{email} for make report and send to email and to store
- generated file will be in app/static/reports

## CLI interface

make this commands in root path(order is important)

- for post shift `python3 cli.py shifts add <employee_email> <start> <end>`
- for make report `python3 cli.py shifts report <employee_email>`

## local start

- switch DOCKER value to 1 to connect with database in docker container and 0 to connect with local database
- if you want to work locally you need:
- make virtual env in root path like: python3 -m venv venv
- activate like: source venv/bin/activate
- install requirements: pip install requirements.txt
