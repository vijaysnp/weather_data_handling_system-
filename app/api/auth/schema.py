from app.constant import constant
from app.api.core import validation
from pydantic import EmailStr, BaseModel, ConfigDict, field_validator



class SigupClient(BaseModel):
    name: str
    email: EmailStr
    password: str
    
    model_config = ConfigDict(from_attributes=constant.STATUS_TRUE, json_schema_extra={
        "example": {
            "name": "johnsmith",
            "email": "johnsmith@gmail.com",
            "password": "Test@123"
        }
    })
    
    @field_validator('name')
    @classmethod
    def sanitize_value(cls, values):
        return validation.ValidationMethods().sanitize_value(values)
    
    @field_validator('name')
    @classmethod
    def name_must_be_required(cls, v):
        return validation.ValidationMethods().not_null_validator(v, 'name')

    @field_validator('email')
    @classmethod
    def email_must_be_required(cls, v):
        return validation.ValidationMethods().not_null_validator(v, 'email')

    @field_validator('password')
    @classmethod
    def password_validation(cls, v):
        return validation.ValidationMethods().password_validator(v)
    

class LoginUser(BaseModel):
    email: EmailStr
    password: str
    model_config = ConfigDict(from_attributes=constant.STATUS_TRUE, extra="allow", json_schema_extra={
        "example": {
            "email": "johnsmith@gmail.com",
            "password": "Test@123"
        }
    })
    
    @field_validator('email')
    @classmethod
    def email_must_be_required(cls, v):
        return validation.ValidationMethods().not_null_validator(v, 'email')

    @field_validator('password')
    @classmethod
    def email_must_be_required(cls, v):
        return validation.ValidationMethods().not_null_validator(v, 'password')
