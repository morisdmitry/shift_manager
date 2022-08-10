from app.api import api
from config import Config
from flask import make_response, request
from flask_restx import Resource
from app.api.api_models import shift_model
from app.database.models import Shift
from app.src.common import ShiftHandler
from app.src.utils import response_bad, response_error

shift = api.namespace("shifts", description="shift")


@shift.route("/")
class ShiftApiPOST(Resource):
    @api.response(200, "OK")
    @api.doc(body=shift_model)
    def post(self):
        body = request.get_json()
        shift = ShiftHandler(body)
        is_correct = shift.check_dates()
        if not is_correct:
            return make_response(
                response_error("date start must be less than date end", 400)
            )

        try:
            shift.transform_dates()
            start_shift = shift.get_start_shift()

            periods, slots_error = shift.day_diff_check()
            if slots_error:
                return make_response(response_error(slots_error, 400))

            if start_shift:
                busy_time_error = shift.check_bisy_time(periods)
                if busy_time_error:
                    return make_response(response_error(busy_time_error, 400))

            created = Shift.create(*periods)
            if not isinstance(created, Shift):
                return make_response(
                    response_error("shift not created please try again", 500)
                )

            response = make_response("shift has writen")
        except Exception as e:
            response = make_response(response_bad(e, 500))

        return response


@shift.route("/<string:employee_email>")
class ShiftApiGet(Resource):
    @api.response(200, "OK")
    def get(self, employee_email):
        try:
            test = Shift.query.filter(Shift.email == employee_email).all()
            main = ShiftHandler(test)
            result = main.get_ui_table()
            response = make_response(result)
        except Exception as e:
            response = make_response(getattr(e, "message", str(e)))

        return response
