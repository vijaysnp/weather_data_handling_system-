import re
import bleach
from app.constant import constant
from app.utils import helper


class ValidationMethods:

    def not_null_validator(self, v, field):
        if v is None or v == "":
            raise ValueError(f"{field} is required")
        return v


    def check_number_validator(self, v, field):
        if not isinstance(v, int):
            raise ValueError(f"{field} must be an integer")
        return v

    def check_float_validator(self, v, field):
        try:
            float_value = float(v)
        except ValueError:
            raise ValueError(f"{field} must be a float")
        return float_value

    def email_validator(self, v):
        if not re.match(r"^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$", v):
            raise ValueError("Please enter a valid email address")
        return v

    def password_validator(self, v):
        if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$", v):
            raise ValueError("Password should be at least eight characters long, "
                             "contain one capital letter, one number, and one special character")
        return v

    def sanitize_value(self, values):
        if values:
            return bleach.clean(values, tags=[], attributes=[], strip=constant.STATUS_TRUE)
        return values