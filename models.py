from app import db



#db = SQLAlchemy()

# define your models classes hereafter


class BaseModel(db.Model):
    """Base data model for all objects"""
    __abstract__ = True
    # define here __repr__ and json methods or any common method
    # that you need for all your models


class cboeibdresmap(BaseModel):
    # define your model

    __tablename__ = 'cboeibdresmap'

    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String, nullable=False)
    ibddatatables_indgrprankings = db.Column(db.String, nullable=False)
    ibdresearch_stockcheckupindgrp = db.Column(db.String, nullable=False)

    def __init__(self,ticker,ibddatatables, ibdresearch):
        self.ibddatatables_indgrprankings = ibddatatables
        self.ibdresearch_stockcheckupindgrp = ibdresearch
        self.ticker = ticker

    def __repr__(self):
        return'<TickerMap: {}, {}, {}'.format(self.ticker, self.ibddatatables_indgrprankings, self.ibdresearch_stockcheckupindgrp)


class ibdinternalmap(BaseModel):
    """model for one of your table"""
    __tablename__ = 'ibdinternalmap'
    # define your model


class industry2(BaseModel):
    """model for one of your table"""
    __tablename__ = 'industry2'
    # define your model


class Users(BaseModel):
    """model for one of your table"""
    __tablename__ = 'users'
    # define your model
    id = db.Column(db.Integer, primary_key=True                   )
    first_name = db.Column(db.String(80), unique=True)
    last_name =  db.Column(db.String(80), unique=True)
    email =   db.Column(db.String(255), unique=True)

    def __init__(self, first_name, last_name, email):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

    def __repr__(self):
        return '<User {} {} {}>'.format(self.first_name, self.last_name, self.email)

    def userstoJSON(self):
        json = {
            "ids":self.ids,
            "first_name":self.first_name,
            "last_name":self.last_name,
            "email":self.email,
        }

        return json