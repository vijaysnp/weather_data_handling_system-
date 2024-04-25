from app.constant import constant
from fastapi import Depends
from app.constant import constant
# from app.utils.message import ErrorMessage, InfoMessage
from config import database
from sqlalchemy.orm import Session
# from app.api.core import db_attribute
# from app.api.auth.models.model import Clients, Roles, ClientHasRoles
# from app.utils.standard_response import StandardResponse
# from app.utils.message import InfoMessage, ErrorMessage
# from fastapi import status
# from fastapi.encoders import jsonable_encoder

getdb = database.get_db


class BaseMethod():

    """This class is provide the basic methods
    """

    def __init__(self, model):
        self.model = model

    
    def save(self, validate_data, db: Session = Depends(getdb)):
        """This function creates new object

        Arguments:
            self(db): database session
            validate_data (dict): validate data

        Returns:
            Returns the creates object
        """
        try:
            db.add(validate_data)
            db.commit()
            db.refresh(validate_data)
            return constant.STATUS_TRUE
        except Exception as err:
            print(err)
            db.rollback()
            db.close()
            return constant.STATUS_FALSE

    def save_all(self, validate_data: list, db: Session = Depends(getdb)):
        """ Saves bulk data in the database. """
        try:
            db.add_all(validate_data)
            db.commit()
            return constant.STATUS_TRUE
        except Exception as err:
            print(err)
            db.rollback()
            db.close()
            return constant.STATUS_FALSE
        
    def bulk_insert_mapping(self, data: dict, db: Session = Depends(getdb)):
        """ Saves bulk data in the database with its mapping"""
        try:
            db.bulk_insert_mappings(self.model, data)
            db.commit()
            return constant.STATUS_TRUE
        except Exception as err:
            print(err)
            db.rollback()
            db.close()
            return constant.STATUS_FALSE  


    def find_by_id(self, uuid, db: Session):
        """This function is used to find users by its uuid"""
        return db.query(self.model).filter(self.model.uuid == uuid, self.model.deleted_at == constant.STATUS_NULL).first()

    def find_by_email(self, db: Session, email: str):
        """This function is used to find users by its uuid"""
        return db.query(self.model).filter(self.model.email == email, self.model.deleted_at == constant.STATUS_NULL).first()

    def find_by_ticket_price_id(self, uuid, db: Session):
        """This function is used to find booking if by its uuid"""
        return db.query(self.model).filter(self.model.uuid == uuid).first()