# -*- coding: utf-8 -*-
## Sistema de Atendimento Automatizado via Telegram

## Copyright (c) 2015, 2016, 2017, 2018, 2019 - Todos os direitos reservados
##
##              SAT Tecnologia Ltda.
##              Rua Alecrim Lote 9 Ed. Espaco Veredas Apt. 1003
##              Brasilia(DF) +5561 95213232
## Autor:
##              Josemar Tadeu Migowski josemarmigowski@gmail.com
##              Data: março de 2016
##              Ultima Atualizacao: 02/11/2015
##              Versao: 0.1

## Web Serice

from flask import Flask
from flask import g
from flask import Response
from flask import request
from flask import render_template
import json
import MySQLdb

app = Flask(__name__)

@app.before_request
def db_connect():
    g.conn = MySQLdb.connect(host='127.0.0.1',
                             user='root',
                             passwd='migbsb98',
                             db='ZapBurguer61')
    g.cursor = g.conn.cursor()

@app.after_request
def db_disconnect(response):
    g.cursor.close()
    g.conn.close()
    return response

def query_db(query, args=(), one=False):
    g.cursor.execute(query, args)
    rv = [dict((g.cursor.description[idx][0], value)
               for idx, value in enumerate(row)) for row in g.cursor.fetchall()]
    return (rv[0] if rv else None) if one else rv

@app.route('/')
def hello():
    return render_template('index.html')

#
# Função para listagem de todos os clientes da base
#
@app.route('/clientes', methods=['GET'])
def clientes():
    result = query_db("SELECT id_cliente,nr_telefone,nr_telegram,nm_nome,\
        ds_endereco,nm_bairro,nm_cidade,uf_uf,rf_referencia,ed_email FROM ZapBurguer61.tb_cliente")
    data = json.dumps(result,ensure_ascii=False)
    resp = Response(data, status=200, mimetype='application/json')
    return resp

#
# Função para consulta de um cliente específico
#
@app.route('/cliente/<telefone>', methods=['GET'])
def cliente(telefone):
    result = query_db("SELECT id_cliente,nr_telefone,nr_telegram,nm_nome,\
        ds_endereco,nm_bairro,nm_cidade,uf_uf,rf_referencia,\
        ed_email FROM ZapBurguer61.tb_cliente WHERE nr_telefone = %s" % telefone )
    data = json.dumps(result,ensure_ascii=False)
    resp = Response(data, status=200, mimetype='application/json')
    return resp

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=2016,debug=True)

