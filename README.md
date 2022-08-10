# Shift_manager

# Features

- Used application factory pattern
- Used .env file for loading configuration

- if is shift between 2022-08-09 23.50.00 and 2022-08-10 00.10.00 will create two notes in data base
- check overlapping time per day per employee
- Not possible to register more than 24 hours per day per employee

# How to start?

- make your .env file. Just copy .env.file and remove the .file at the end. In .env is default values

- in root path make commands:
  `docker-compose build`
  `docker-compose up -d`
- update your database
  `docker-compose exec web flask db upgrade`

- go to `http://127.0.0.1:4000/api/`
