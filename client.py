from flask import Flask, request, jsonify
import json
import requests
from datetime import datetime
from dateutil import parser as parserd
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--add',nargs='+', help='Add entry to database. Columns values are separated by space. First argument is name of table')
parser.add_argument('--dele',nargs='+', help='Delete Entry From Database By id. First argument is name of table')
parser.add_argument('--all', help='Print entire table',choices=['Friends','Books','Borrowed'])
parser.add_argument('--allB',help='Print all books borrowed and who borrows it',action='store_true')
parser.add_argument('--person', nargs=2,help='Print all data about person. Requires name and surname')
parser.add_argument('--book', help='Print all data about book. Requires book title')
parser.add_argument('--borrowed',nargs=2, help='Print all books borrowed by person. Requires name and surname')
parser.add_argument('--up_friend',nargs=3,help='Update age and/or email for Friend by id')
parser.add_argument('--up_date',nargs=2,help='Update enddate for Borrowed book by id')
args = parser.parse_args()

if args.add:
    if args.add[0]=='Friends':
        req=requests.put('http://127.0.0.1:5000/Friends?name='+args.add[1]+'&surname='+args.add[2]+\
        '&age='+args.add[3]+'&email='+args.add[4])
        added=req.json()
        if 'msg' in added.keys():
            print(added['msg'])
        else:
            print('ADDED FRIEND: '+added['name']+' '+added['surname']+' '+added['age']+' '+added['email'])
    elif args.add[0]=='Books':
        req=requests.put('http://127.0.0.1:5000/Books?author='+args.add[1]+'&year='+args.add[2]+\
        '&title='+args.add[3])
        added=req.json()
        if 'msg' in added.keys():
            print(added['msg'])
        else:
            print('ADDED BOOK: '+added['author']+' '+added['year']+' '+added['title'])
    elif args.add[0]=='Borrowed':
        req=requests.put('http://127.0.0.1:5000/Borrowed?person='+args.add[1]+'&book='+args.add[2]+\
        '&startdate='+args.add[3]+'&enddate='+args.add[4])
        added=req.json()
        if 'msg' in added.keys():
            print(added['msg'])
        else:
            print('BOOK BORROWED: '+added['person']+' '+added['book']+' '+added['startdate']+' '+added['enddate'])

elif args.all:
    if args.all=='Friends':
        req=requests.get('http://127.0.0.1:5000/all/Friends')
        resj=req.json()
        for x in resj:
            print(x['id']+' '+x['name']+' '+x['surname']+' '+x['age']+' '+x['email'])
    if args.all=='Books':
        req=requests.get('http://127.0.0.1:5000/all/Books')
        resj=req.json()
        for x in resj:
            print(x['id']+' '+x['author']+' '+x['year']+' '+x['title'])
    if args.all=='Borrowed':
        req=requests.get('http://127.0.0.1:5000/all/Borrowed')
        resj=req.json()
        for x in resj:
            print(x['id']+' '+x['person']+' '+x['book']+' '+x['startdate']+' '+x['enddate'])

elif args.allB:
    req=requests.get('http://127.0.0.1:5000/allB')
    resj=req.json()
    for x in resj:
        print(x['idF']+' '+x['name']+' '+x['surname']+' '+x['idB']+' '+x['title']+' '+x['startdate']+' '+x['enddate'])

elif args.person:
    req=requests.get('http://127.0.0.1:5000/Friends?name='+args.person[0]+'&surname='+args.person[1])
    resj=req.json()
    for x in resj:
        if 'msg' in x.keys():
            print(x['msg'])
            break
        print(x['id']+' '+x['name']+' '+x['surname']+' '+x['age']+' '+x['email'])
elif args.book:
    req=requests.get('http://127.0.0.1:5000/Books?title='+args.book)
    resj=req.json()
    for x in resj:
        if 'msg' in x.keys():
            print(x['msg'])
            break
        print(x['id']+' '+x['author']+' '+x['year']+' '+x['title'])
elif args.borrowed:
    req=requests.get('http://127.0.0.1:5000/Borrowed?name='+args.borrowed[0]+'&surname='+args.borrowed[1])
    resj=req.json()
    for x in resj:
        if 'msg' in x.keys():
            print(x['msg'])
            break
        print(x['idF']+' '+x['name']+' '+x['surname']+' '+x['idB']+' '+x['title']+' '+x['startdate']+' '+x['enddate'])

elif args.dele:
    if args.dele[0]=='Friends':
        req=requests.delete('http://127.0.0.1:5000/Friends/'+args.dele[1])
        resj=req.json()
        if 'msg' in resj.keys():
            print(resj['msg'])
        else:
            print('DELETED FRIEND: '+resj['id']+' '+resj['name']+' '+resj['surname']+' '+resj['age']+' '+resj['email'])
    if args.dele[0]=='Books':
        req=requests.delete('http://127.0.0.1:5000/Books/'+args.dele[1])
        resj=req.json()
        if 'msg' in resj.keys():
            print(resj['msg'])
        else:
            print('DELETED BOOK: '+resj['id']+' '+resj['author']+' '+resj['year']+' '+resj['title'])
    if args.dele[0]=='Borrowed':
        req=requests.delete('http://127.0.0.1:5000/Borrowed/'+args.dele[1])
        resj=req.json()
        if 'msg' in resj.keys():
            print(resj['msg'])
        else:
            print('DELETED BORROWED: '+resj['id']+' '+resj['person']+' '+resj['book']+' '+resj['startdate']+' '+resj['enddate'])

elif args.up_friend:
    req=requests.post('http://127.0.0.1:5000/Friends?id='+args.up_friend[0]+'&age='+args.up_friend[1]+'&email='+args.up_friend[2])
    resj=req.json()
    for k,v in resj.items():
        print(k+': '+v)

elif args.up_date:
    req=requests.post('http://127.0.0.1:5000/Borrowed?id='+args.up_date[0]+'&date='+args.up_date[1])
    resj=req.json()
    for k,v in resj.items():
        print(k+': '+v)
