from flask import Flask, render_template, request
from flask_restful import Api, Resource
from web_app.auth import login_tenant, signup_tenant
from flask_mail import Mail, Message
from flask_restful.reqparse import RequestParser
import pymysql
from attacks.boolean import boolean
from attacks.comment import comment
from attacks.batch import batch
from attacks.like import like
from attacks.xss import xss
import time  
import socket
socket.getaddrinfo('localhost', 8080)  

app = Flask(__name__)
api = Api(app)
mail = Mail(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'dineshnandhagopal2802@gmail.com'
app.config['MAIL_PASSWORD'] = 'dinesh@98'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():    
    res = login_tenant(request.form)       
    if(res['status']==1):
        return render_template('index.html', data=res['msg'])
    else:             
        return render_template('dashboard.html', data=res['data'], count=res['count'], tenant=res['tenant'])

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    return render_template('signup.html')

@app.route('/tenants', methods=['POST'])
def add_tenant():
    res = signup_tenant(request.form)     
    if(res['status']==0):    
        return render_template('signup.html', data=res['msg'], token="Your Token is :  "+res['token'])    
    else:
        return render_template('signup.html', data=res['msg'])    

# DB Configuration
db = pymysql.connect(host='localhost',
                    user='root',
                    password='',
                    db='sqlidap',
                    charset='utf8mb4',
                    cursorclass=pymysql.cursors.DictCursor, autocommit= True)


# Temporary db work area
cursor = db.cursor()

# Asking necessary inputs for API
validate_request = RequestParser(bundle_errors=True)
validate_request.add_argument('user_input', type=str, required=True, help='User input is required')
validate_request.add_argument('token', type=str, required=True, help='Token is required')
validate_request.add_argument('mac_address', type=str, required=True, help='Mac Address is required')

class return_response:    
    def get_response(self, status_code, type_of_injection, injected_code=None):
        response = dict()
        response['status'] = status_code
        response['type_of_injection'] = type_of_injection
        response['injected_code'] = injected_code
        return response
        
class sqlidap(Resource):
    
    tenant_id = int
    tenant_email = str

    def check_valid_user(self,token):
        
        # Check user presence
        sql = "SELECT `id`, `email` FROM `tenants` WHERE `token`=%s"
        cursor.execute(sql, (token,))
        
        id = cursor.fetchone()        
        self.tenant_id = id['id'] 
        self.tenant_email = id['email']       

        if(len(id)>0):        
            return True
        
        else:
            return False

    def send_mail(self, receiver_mail_id, mac_address, time, type_of_attack, injected_code):        
        msg = Message('SQLIDAP - SQL Attack', sender = 'dineshnandhagopal2802@gmail.com', recipients = [receiver_mail_id])
        msg.body = f'''
        Hi, {receiver_mail_id}
        \n
        The below client trying to attack your web application.
        MAC ADDRESS : {mac_address}        
        TYPE OF ATTACK : {type_of_attack}
        INJECTED CODE : {injected_code}
        \n
        Thanks for using our service.
        \n
        SQLIDAP SERVICE
        '''
        mail.send(msg)
                    
    def store_attack(self, mac_address, type_of_attack, injected_code):
        
        date = time.strftime('%Y-%m-%d %H:%M:%S')
        sql = "SELECT `id` FROM attack_types WHERE attack_name = %s"
        cursor.execute(sql,(type_of_attack,))
        result = cursor.fetchone()
        type_of_attack_id = result['id']        

        # Store attack in corresponding tenant
        sql = "INSERT INTO attacks(tenant_id, date, type_of_attack, mac_address, injected_code) VALUES(%s, %s, %s, %s, %s)"        
        cursor.execute(sql, (self.tenant_id,date, type_of_attack_id, mac_address, injected_code))
                
        self.send_mail(self.tenant_email, mac_address, date, type_of_attack, injected_code)

    def post(self):
        args = validate_request.parse_args() 

        # Check valid user or not
        if(self.check_valid_user(args['token'])):
            
            boolean_attack = boolean()            
            comment_attack = comment()
            batch_attack = batch()
            like_attack = like()
            xss_attack = xss()
            
            if(boolean_attack.check_boolean_based_attack(args['user_input'])):    
                self.store_attack(args['mac_address'], "Boolean Based Attack", args['user_input'])            
                return return_response().get_response(True, "Boolean Based Attack", args['user_input'])                
                        
            elif(batch_attack.check_batch_based_attack(args['user_input'])):
                self.store_attack(args['mac_address'], "Batch Query Attack", args['user_input'])
                return return_response().get_response(True, "Batch Query Attack", args['user_input'])

            elif(like_attack.check_like_based_attack(args['user_input'])):
                self.store_attack(args['mac_address'], "Like Based Attack", args['user_input'])
                return return_response().get_response(True, "Like Based Attack", args['user_input'])

            elif(xss_attack.check_xss_based_attack(args['user_input'])):
                self.store_attack(args['mac_address'], "XSS Attack", args['user_input'])
                return return_response().get_response(True, "XSS Attack", args['user_input'])

            elif(comment_attack.check_comment_based_attack(args['user_input'])):
                self.store_attack(args['mac_address'], "Comment Based Attack", args['user_input'])
                return return_response().get_response(True, "Comment Based Attack", args['user_input'])  
            
            else:                
                return return_response().get_response(True, "No attack")

        else:
            return {"status":True, "msg": "You are not a valid user. Token not found"}

api.add_resource(sqlidap, '/sqlidap_service') 

if __name__ == '__main__':
    app.run(debug=True)