import re
import bleach
from app.constant import constant
from app.utils import helper


class ValidationMethods:
    def not_null_validator(self, v, field):
        if v == "":
            raise ValueError(f"{field} must be required")
        return v

    def check_number_validator(self, v, field):
        if v == str(v):
            raise ValueError(f"{field} must be an integer")
        return v

    def check_float_validator(self, v, field):
        try:
            float_value = float(v)
        except ValueError:
            raise ValueError(f"{field} must be a float")
        return float_value


    def email_validator(self, v):
        reg = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"

        # compiling regex
        pat = re.compile(reg)

        if not (mat := re.search(pat, v)):
            raise ValueError("Please, enter a valid email address")
        return v

    def password_validator(self, v):
        reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"

        # compiling regex
        pat = re.compile(reg)

        if not (mat := re.search(pat, v)):
            sentence = "Password should be at least eight characters long, should contain one capital letter, \
                        one number and one special character"
            raise ValueError(sentence)
        return v

    def validate_schema_date(self, v):
        if v < helper._get_date():
            raise ValueError("The provided date must be in the future.")
        return v

    def sanitize_value(self, values):
        if values:
            return bleach.clean(
                values, tags={}, attributes=[], strip=constant.STATUS_TRUE
            )
