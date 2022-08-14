from app.api import api
from flask import make_response, request
from flask_restx import Resource
from app.api.api_models import timeshit_model
from app.database.models import Timeshits
from app.src.modules.timeshift_helper import TimeshitHandler
from app.src.modules.reports_helper import ReportsHelper
from app.src.validation import response_bad, response_error

timeshit = api.namespace("timeshits", description="timeshit")
reports = api.namespace("reports", description="reports")


@timeshit.route("/")
class TimeshitApi(Resource):
    @api.response(200, "OK")
    @api.doc(body=timeshit_model)
    def post(self):
        body = request.get_json()
        timeshit = TimeshitHandler(body)
        is_correct = timeshit.check_dates()
        if not is_correct:
            return make_response(
                response_error("date start must be less than date end", 400)
            )

        try:
            timeshit.transform_dates()
            start_timeshit = timeshit.get_start_shift()

            periods, slots_error = timeshit.day_diff_check()
            if slots_error:
                return make_response(response_error(slots_error, 400))

            if start_timeshit:
                busy_time_error = timeshit.check_bisy_time(periods)
                if busy_time_error:
                    return make_response(response_error(busy_time_error, 400))
            created = Timeshits.create(*periods)
            if not isinstance(created, Timeshits):
                return make_response(
                    response_error("timeshit not created please try again", 500)
                )

            response = make_response("timeshit has writen")
        except Exception as e:
            response = make_response(response_bad(e, 500))

        return response


@timeshit.route("/monthly/<string:employee_email>")
class TimeshitApiGet(Resource):
    @api.response(200, "OK")
    def get(self, employee_email):
        try:
            report = ReportsHelper()
            data = report.set_data(employee_email)
            if not data:
                return make_response(
                    response_error("no timeshit for current month", 400)
                )

            file_message = report.create(data)
            mail_message = report.to_email()
            store_message = report.to_store()

            response = {
                "file": file_message,
                "ssend to mail": mail_message,
                "send to store": store_message,
            }
            response = make_response(response)
        except Exception as e:
            response = make_response(getattr(e, "message", str(e)))

        return response
