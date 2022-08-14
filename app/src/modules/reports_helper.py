import json
import requests
import calendar
import boto3
import zipfile
import io
from datetime import datetime, timedelta
from pathlib import Path
from flask import current_app
from app.database.models import Timeshits

# from app.store import s3
from sqlalchemy import and_


class ReportsHelper:

    folder_reports = Path().absolute() / "app/static/reports/"
    file_format = ".txt"
    zip_format = ".zip"
    current_date = datetime.now()
    first_day = 1
    last_day = calendar.monthrange(current_date.year, current_date.month)[1]

    def __init__(self):
        self.employee_email: str
        self.total_hours: float
        self.path: Path
        self.filename: str
        self.zip_name: str
        self.filename_format: Path

    def set_data(self, employee_email: str) -> list:
        timeshits = Timeshits.query.filter(
            and_(
                Timeshits.email == employee_email,
                Timeshits.start
                >= datetime(
                    year=self.current_date.year,
                    month=self.current_date.month,
                    day=1,
                ),
                Timeshits.end
                <= datetime(
                    year=self.current_date.year,
                    month=self.current_date.month,
                    day=self.last_day,
                    hour=23,
                    minute=59,
                    second=59,
                ),
            )
        ).all()

        self.employee_email = employee_email
        return timeshits

    def create(self, data: list) -> None:
        try:
            self.form_filename()
            self.create_empty_file()
            error = self.write_file_content(data)
            if error:
                return error
            return f"file {self.filename_format} created succesfuly"
        except Exception as e:
            return getattr(e, "message", str(e))

    def form_filename(self) -> None:
        format = "%y-%m"
        current_month = self.current_date.strftime(format)

        self.filename = f"{self.employee_email}_{current_month}"
        self.zip_name = f"{self.employee_email}_{current_month}{self.zip_format}"
        self.filename_format = Path(f"{self.filename}{self.file_format}")

    def create_empty_file(self) -> None:
        self.path = self.folder_reports / self.filename_format
        self.path.touch()

    def write_file_content(self, data: list):
        try:
            existing_dates = self.format_shifts(data)
            month_table = self.month_table(existing_dates)
            result_table = self.format_table(month_table)

            with open(self.path, "w") as file:
                file.write(f"Employee: {self.employee_email}" + "\n")
                for day, hours in result_table.items():
                    file.write(f"{day} {hours}" + "\n")
                file.write("—-----------" + "\n")
                file.write(f"Total: {self.total_hours} hours")

            if not self.path.is_file():
                return "file not created"

            return False
        except Exception as e:
            return getattr(e, "message", str(e))

    def format_shifts(self, data: list) -> dict:
        result = {}
        hour_count = timedelta()
        current_day = 0
        for i in data:
            if current_day == i.start.day or current_day == 0:
                hour_count += i.end - i.start
                current_day = i.start.day

            elif i.start.day == current_day + 1:
                hour_count = i.end - i.start
                current_day = i.start.day
            result[i.start.day] = self.get_table_format(hour_count)
        self.total_hours = round(sum(result.values()), 1)
        return result

    def month_table(self, data: dict) -> dict:
        template = {day: 0.0 for day in range(1, self.last_day + 1)}
        for day, hours in data.items():
            template[day] = hours
        return template

    def format_table(self, month_table: dict) -> dict:
        return {f"D {day:02}": f"H {hours}" for day, hours in month_table.items()}

    @staticmethod
    def get_table_format(td: datetime) -> float:
        hours = td.seconds // 3600
        minutes = (td.seconds // 60) % 60
        if minutes != 0:
            minutes = int(10 / (60 / minutes))
        return float(f"{hours}.{minutes}")

    def to_email(self) -> requests:
        try:
            response = requests.post(
                current_app.config.get("MG_LINK"),
                auth=("api", current_app.config.get("MG_API")),
                files=[
                    (
                        "attachment",
                        (
                            str(self.filename_format),
                            open(str(self.path), "rb").read(),
                        ),
                    )
                ],
                data={
                    "from": current_app.config.get("MG_MAIL"),
                    "to": [f"{self.employee_email}"],
                    "subject": f"Report. month: {self.current_date.month}",
                    "text": "Your report is attached",
                },
            )
            return json.loads(response.text)["message"]
        except Exception as e:
            return getattr(e, "message", str(e))

    def to_store(self):
        try:
            zip_bytes = self.zip_create()
            s3_resource = boto3.resource("s3")
            bucket = s3_resource.Bucket(current_app.config.get("S3_BUCKET"))
            data = bucket.Object(self.zip_name).put(
                Body=io.BytesIO(zip_bytes.getvalue())
            )
            if not data:
                raise Exception("bad connection, repeat again")

            return "zip file uploaded succesfuly"
        except Exception as e:
            return getattr(e, "message", str(e))

    def zip_create(self) -> bytes:
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(
            zip_buffer, mode="w", compression=zipfile.ZIP_DEFLATED
        ) as zip:
            zip.write(self.path, arcname=self.filename_format)
        return zip_buffer
