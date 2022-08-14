from datetime import datetime, time, timedelta
from typing import Union

from sqlalchemy import and_

from app.database.models import Timeshits


class TimeshitHandler:
    max_hour_shift = 24

    def __init__(self, data):
        self.data = data
        self.start_shift = None
        self.periods = None

    def check_dates(self) -> bool:
        """Check correct dates order"""
        return self.data["start"] < self.data["end"]

    def transform_dates(self):
        """Transform dates"""
        for key, value in self.data.items():
            if key in ["start", "end"]:
                self.data[key] = self.converter_datetime(value)
            else:
                self.data[key] = value

    def converter_datetime(self, date_time: int) -> datetime:
        """Get Datetime from Unix format"""
        dt = self.get_date(
            datetime.utcfromtimestamp(date_time).strftime("%Y-%m-%d %H:%M:%S")
        )
        return dt

    @staticmethod
    def get_date(date: str) -> datetime:
        return datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

    def is_day_slots(
        self, *periods: tuple[dict, dict]
    ) -> Union[tuple[dict, dict], None]:
        for period in periods:
            current_start, current_end = period["start"], period["end"]
            if current_start.time() != time(0, 0, 0) and self.start_shift:
                current_start = self.start_shift.start
            common_spending_time = current_end - current_start
            end_day = timedelta(seconds=self.max_hour_shift * 60 * 60)
            res = end_day.total_seconds() - common_spending_time.total_seconds()
            if res < 0:
                return (
                    None,
                    f"no more shift slots between: {current_start} and {current_end}",
                )
        return periods, None

    def separate_data(self) -> tuple[dict, dict]:
        yesterday_data = {
            "email": self.data["email"],
            "start": self.data["start"],
            "end": datetime.combine(self.data["start"].date(), time(23, 59, 59)),
        }
        today_data = {
            "email": self.data["email"],
            "start": datetime.combine(self.data["end"].date(), time(0, 0, 0)),
            "end": self.data["end"],
        }
        return yesterday_data, today_data

    def get_start_shift(self):
        """Check is there note for this day"""
        start_shift = (
            Timeshits.query.filter(
                and_(
                    Timeshits.email == self.data["email"],
                    Timeshits.start >= self.data["start"].date(),
                )
            )
            .order_by(Timeshits.start.asc())
            .first()
        )
        self.start_shift = start_shift
        return start_shift

    @staticmethod
    def check_bisy_time(periods):
        """Check overlapping"""
        for period in periods:
            res = Timeshits.query.filter(
                and_(
                    Timeshits.email == period["email"], Timeshits.end > period["start"]
                )
            ).first()
            if res:
                return f"this time is already taken: {res.start} and {res.end}"

    def day_diff_check(self):
        """Next day check"""
        if self.data["start"].day < self.data["end"].day:
            double_data = self.separate_data()
            periods, slots_error = self.is_day_slots(*double_data)
        else:
            periods, slots_error = self.is_day_slots((self.data))
        self.periods = periods
        return periods, slots_error
