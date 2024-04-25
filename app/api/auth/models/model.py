from app.constant import constant
from config.database import Base
from sqlalchemy import Column, DateTime, Integer, String
from app.utils.helper import _get_datetime


class User(Base):
    """
    Table used for login for each user.
    """
    __tablename__ = "user"

    id = Column(Integer, primary_key=constant.STATUS_TRUE, nullable=constant.STATUS_FALSE)
    name = Column(String(100), doc='name of user', nullable=constant.STATUS_TRUE)
    email = Column(String(100),
                   doc='Email ID of the user', nullable=constant.STATUS_FALSE)
    password = Column(
        String(100), doc='Password of the user', nullable=constant.STATUS_FALSE)
    created_at = Column(DateTime, nullable=constant.STATUS_FALSE,
                        default=_get_datetime,
                        doc='its generate automatically when user create')
    updated_at = Column(DateTime, nullable=constant.STATUS_TRUE, default=_get_datetime,
                        onupdate=_get_datetime,
                        doc='its generate automatically when user update')
    deleted_at = Column(DateTime, nullable=constant.STATUS_TRUE,
                        doc='its generate automatically when user deleted')
    