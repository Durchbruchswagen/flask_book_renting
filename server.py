import argparse
from sqlalchemy import create_engine, delete
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, validates, sessionmaker
from sqlalchemy import Table, Column, Integer, ForeignKey, String, Date
from sqlalchemy_utils import database_exists
from datetime import datetime
from dateutil import parser as parserd
import json
from flask import Flask, request, jsonify

app=Flask(__name__)

Base=declarative_base()

class Friends(Base):
    __tablename__='Friends'

    id=Column(Integer,primary_key=True)
    name=Column(String(20),nullable=False)
    surname=Column(String(20),nullable=False)
    age=Column(Integer,default=18)
    email=Column(String)
    borrowed=relationship('Borrowed')
    
    def __str__(self):
    	return (str(self.id)+' '+self.name+' '+self.surname+' '+str(self.age)+' '+self.email)

    @validates('email')
    def validate_email(self,key,value):
        if '@' not in value:
                return 'wrong email'
        return value

class Books(Base):
    __tablename__='Books'

    id=Column(Integer,primary_key=True)
    author=Column(String)
    year=Column(Integer,nullable=False)
    title=Column(String,nullable=False)
    borrowed=relationship('Borrowed')
    
    def __str__(self):
    	return (str(self.id)+' '+self.author+' '+str(self.year)+' '+self.title+' ')

    @validates('title')
    def validate_title(self,key,value):
        if value == '':
                return 'No title'
        return value
    @validates('year')
    def validate_year(self,key,value):
        if value == 0:
                return 1
        return value

class Borrowed(Base):
    __tablename__='Borrowed'

    id=Column(Integer,primary_key=True)
    person=Column(Integer,ForeignKey('Friends.id'),nullable=False)
    book=Column(Integer,ForeignKey('Books.id'),nullable=False)
    startdate=Column(Date)
    enddate=Column(Date)
    
    @validates('startdate','enddate')
    def validate_dates(self,key,value):
    	if key=='enddate':
    		if self.startdate>value:
                        return self.startdate
    	return value
    
    def __str__(self):
    	return (str(self.id)+' '+str(self.person)+' '+str(self.book)+' '+str(self.startdate)+' '+str(self.enddate))

engine=create_engine('sqlite:///baza.db')
if not database_exists(engine.url):
    print('Creating database')
    Base.metadata.create_all(engine)
else:
    print('Database already exists')

Session=sessionmaker(bind=engine)
session=Session()


@app.route("/")
def main():
        return "<p>serwer test</p>"
	
@app.route("/Friends",methods=['PUT'])
def add_friend():
        name=request.args.get('name',None)
        surname=request.args.get('surname',None)
        age=request.args.get('age',None)
        email=request.args.get('email',None)
        try:
                a1=Friends(name=name,surname=surname,age=int(age),email=email)
        except:
                err='Error when adding record'
                session.rollback()
                return jsonify({'msg':err})
        session.add(a1)
        session.commit()
        return jsonify({'name': name,'surname':surname,'age':age,'email':email})
        
@app.route("/Books",methods=['PUT'])
def add_Book():
        author=request.args.get('author',None)
        year=request.args.get('year',None)
        title=request.args.get('title',None)
        try:
                a1=Books(author=author,year=int(year),title=title)
        except:
                err='Error when adding record'
                session.rollback()
                return jsonify({'msg':err})
        session.add(a1)
        session.commit()
        return jsonify({'author': author,'year':year,'title':title})

@app.route("/Borrowed",methods=['PUT'])
def add_Borrowed():
        person=request.args.get('person',None)
        book=request.args.get('book',None)
        startdate=request.args.get('startdate',None)
        enddate=request.args.get('enddate',None)
        try:
                a1=Borrowed(person=int(person),book=int(book),startdate=parserd.parse(startdate),enddate=parserd.parse(enddate))
        except:
                err='Error when adding record'
                session.rollback()
                return jsonify({'msg':err})
        session.add(a1)
        session.commit()
        return jsonify({'person': person,'book':book,'startdate':str(a1.startdate),'enddate':str(a1.enddate)})

@app.route("/all/Friends",methods=['GET'])
def all_Friends():
        list_=[]
        x=session.query(Friends).all()
        for e in x:
                list_.append({'id':str(e.id),'name':e.name,'surname':e.surname,'age':str(e.age),'email':e.email})
        return json.dumps(list_,indent=2)
        
@app.route("/all/Books",methods=['GET'])
def all_Books():
        list_=[]
        x=session.query(Books).all()
        for e in x:
                list_.append({'id':str(e.id),'author':e.author,'year':str(e.year),'title':e.title})
        return json.dumps(list_,indent=2)

@app.route("/all/Borrowed",methods=['GET'])
def all_Borrowed():
        list_=[]
        x=session.query(Borrowed).all()
        for e in x:
                list_.append({'id':str(e.id),'person':str(e.person),'book':str(e.book),'startdate':str(e.startdate),'enddate':str(e.enddate)})
        return json.dumps(list_,indent=2)

@app.route("/Friends",methods=['GET'])
def get_Friend():
        list_=[]
        name=request.args.get('name',None)
        surname=request.args.get('surname',None)
        try:
                x=session.query(Friends).filter(Friends.name==name and Friends.surname==surname).all()
        except:
                list_.append({'msg':'Query error'})
                return json.dumps(list_,indent=2)
        for e in x:
                list_.append({'id':str(e.id),'name':e.name,'surname':e.surname,'age':str(e.age),'email':e.email})
        return json.dumps(list_,indent=2)
        
@app.route("/Books",methods=['GET'])
def get_Books():
        list_=[]
        title=request.args.get('title',None)
        try:
                x=session.query(Books).filter(Books.title==title).all()
        except:
                list_.append({'msg':'Query error'})
                return json.dumps(list_,indent=2)
        for e in x:
                list_.append({'id':str(e.id),'author':e.author,'year':str(e.year),'title':e.title})
        return json.dumps(list_,indent=2)

@app.route("/Borrowed",methods=['GET'])
def get_Borrowed():
        list_=[]
        name=request.args.get('name',None)
        surname=request.args.get('surname',None)
        try:
                x=session.query(Borrowed).join(Friends).join(Books).filter(Friends.name==name and Friends.surname==surname).with_entities(Friends.id,Friends.name,Friends.surname,Books.id,Books.title,Borrowed.startdate,Borrowed.enddate).all()
        except:
                list_.append({'msg':'Query error'})
                return json.dumps(list_,indent=2)
        for e in x:
                list_.append({'idF':str(e[0]),'name':e[1],'surname':e[2],'idB':str(e[3]),'title':e[4],'startdate':str(e[5]),'enddate':str(e[6])})
        return json.dumps(list_,indent=2)

@app.route("/allB",methods=['GET'])
def allB():
        list_=[]
        x=session.query(Borrowed).join(Friends).join(Books).with_entities(Friends.id,Friends.name,Friends.surname,Books.id,Books.title,Borrowed.startdate,Borrowed.enddate).all()
        for e in x:
                list_.append({'idF':str(e[0]),'name':e[1],'surname':e[2],'idB':str(e[3]),'title':e[4],'startdate':str(e[5]),'enddate':str(e[6])})
        return json.dumps(list_,indent=2)

@app.route("/Friends/<id>",methods=['DELETE'])
def delete_Friends(id):
        dltrec=session.query(Friends).filter(Friends.id==int(id)).one()
        x=session.query(Friends).filter(Friends.id==int(id)).one()
        try:
                session.delete(x)
        except:
                session.rollback()
                return jsonify({'msg':'error when deleting record'})
        try:
                session.commit()
        except:
                session.rollback()
                return jsonify({'msg':'error when deleting record'})
        return jsonify({'id':str(dltrec.id),'name':dltrec.name,'surname':dltrec.surname,'age':str(dltrec.age),'email':dltrec.email})

@app.route("/Books/<id>",methods=['DELETE'])
def delete_Books(id):
        dltrec=session.query(Books).filter(Books.id==int(id)).one()
        x=session.query(Books).filter(Books.id==int(id)).one()
        try:
                session.delete(x)
        except:
                session.rollback()
                return jsonify({'msg':'error when deleting record'})
        try:
                session.commit()
        except:
                session.rollback()
                return jsonify({'msg':'error when deleting record'})
        return jsonify({'id': str(dltrec.id), 'author': dltrec.author,'year':str(dltrec.year),'title':dltrec.title})

@app.route("/Borrowed/<id>",methods=['DELETE'])
def delete_Borrowed(id):
        dltrec=session.query(Borrowed).filter(Borrowed.id==int(id)).one()
        x=session.query(Borrowed).filter(Borrowed.id==int(id)).one()
        try:
                session.delete(x)
        except:
                return jsonify({'msg':'error when deleting record'})
        try:
                session.commit()
        except:
                return jsonify({'msg':'error when deleting record'})
        return jsonify({'id': str(dltrec.id),'person': str(dltrec.person),'book':str(dltrec.book),'startdate':str(dltrec.startdate),'enddate':str(dltrec.enddate)})

@app.route("/Friends",methods=['POST'])
def updt_Friends():
        id=request.args.get('id','basba')
        newage=request.args.get('age',None)
        newemail=request.args.get('email',None)
        try:
                idnum=int(id)
        except:
                return jsonify({'msg':'Update error'}) 
        if newage==None or newemail==None:
                return jsonify({'msg':'Update error'}) 
        if newage=='NULL' and newemail!='NULL':
                session.query(Friends).filter(Friends.id==int(id)).update({'email':newemail})
                session.commit()
                return jsonify({'newemail':newemail})
        elif newage!='NULL' and newemail=='NULL':
                session.query(Friends).filter(Friends.id==int(id)).update({'age':int(newage)})
                session.commit()
                return jsonify({'newage':newage})
        elif newage!='NULL' and newemail!='NULL':
                session.query(Friends).filter(Friends.id==int(id)).update({'email':newemail,'age':int(newage)})
                session.commit()
                return jsonify({'newemail':newemail,'newage':newage})
        else:
                return jsonify({'msg':'no updates'})

@app.route("/Borrowed",methods=['POST'])
def updt_Borrowed():
        id=request.args.get('id','Wrong number')
        newdate=request.args.get('date',None)
        try:
                idnum=int(id)
        except:
                return jsonify({'msg':'Update error'}) 
        if newdate==None:
                return jsonify({'msg':'Update error'})
        if newdate=='NULL':
                return jsonify({'msg':'no updates'})
        else:
                try:
                        dateparsed=parserd.parse(newdate)
                except:
                        return jsonify({'msg':'no updates'})
                record=session.query(Borrowed).filter(Borrowed.id==int(id)).one()
                if dateparsed.date()<record.enddate:
                        return jsonify({'msg':'wrong date'})
                else:
                     session.query(Borrowed).filter(Borrowed.id==int(id)).update({'enddate':dateparsed})
                     session.commit()
                     return jsonify({'newdate':str(dateparsed.date())})

