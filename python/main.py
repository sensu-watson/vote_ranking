#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

from bottle import route, get, post, run, HTTPResponse, request
import simplejson as json
import MySQLdb

class useMySQL:
    def __init__(self,
                 host='localhost', user='root', password='kenken3922',
                 db='kyozaihack', charset='utf8'):
        self.connection = MySQLdb.connect(
            host=host, user=user, passwd=password, db=db, charset=charset)

    def get_ranking(self):
        cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
        sql = 'select id, name, vote from foods order by vote desc'
        cursor.execute(sql)
        return cursor.fetchall()

    def vote2food(self, food_id):
        cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
        sql = 'update foods set vote = vote + 1 where id = ' + food_id
        cursor.execute(sql)
        self.connection.commit()

    def newfood(self, food_name):
        cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
        sql = 'insert into foods(name, vote) value ("'+food_name+'", 1)'
        cursor.execute(sql)
        self.connection.commit()

@route('/')
def index():
    return ""

@post('/api/new')
def new():
    newfood = request.forms.newfood
    usemysql = useMySQL()
    usemysql.newfood(newfood)
    body = json.dumps({
        'message' : 'OK',
        'newfood' : newfood
    })
    r = HTTPResponse(status=200, body=body)
    r.set_header('Content-Type', 'application/json')
    r.set_header('Access-Control-Allow-Origin', '*')
    return r
    

@post('/api/vote/<food_id>')
def vote(food_id):
    usemysql = useMySQL()
    usemysql.vote2food(food_id)
    body = json.dumps({
        'message' : 'OK',
        'food_id' : food_id
    })
    r = HTTPResponse(status=200, body=body)
    r.set_header('Content-Type', 'application/json')
    r.set_header('Access-Control-Allow-Origin', '*')
    return r

@get('/api/ranking')
def ranking():
    usemysql = useMySQL()
    ranking = usemysql.get_ranking()
    body = json.dumps({
            'message' : 'OK',
            'ranking' : ranking
        })
    r = HTTPResponse(status=200, body=body)
    r.set_header('Content-Type', 'application/json')
    r.set_header('Access-Control-Allow-Origin', '*')
    return r

run(host='localhost', port=8080, debug=True)
