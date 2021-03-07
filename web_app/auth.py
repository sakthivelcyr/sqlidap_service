import pymysql
import uuid

db = pymysql.connect(host='localhost',
                    user='root',
                    password='',
                    db='sqlidap',
                    charset='utf8mb4',
                    cursorclass=pymysql.cursors.DictCursor, autocommit= True)

cursor = db.cursor()

def signup_tenant(data):    
    try:
        # Store tenant
        sql = "SELECT * FROM `tenants` WHERE `email`=%s"
        cursor.execute(sql, (data['email']))  
        res = cursor.fetchall()
        
        if(len(res)==0):
            # make a UUID based on the host ID and current time
            token = uuid.uuid1()
               
            # Create a new tenant                
            sql = "INSERT INTO `tenants` (`name`, `org_name`, `email`, `token`) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (data['name'], data['org_name'], data['email'], str(token)))
            
            # Commit all the changes
            db.commit()       
            return {"status":0,"msg":"Tenant registered successfully.","token":str(token)}

        else:
            return {"status":1, "msg":"Email already found"}     

    except:
        return {"status":1, "msg":"Server has some issues. Try again later."} 

def login_tenant(data):                
    try:
        # Check tenant exist or not
        sql = "SELECT * FROM `tenants` WHERE `email`=%s AND `token`=%s"
        cursor.execute(sql, (data['email'],data['token']))        
        res = cursor.fetchall()        
        tenant_id = res[0]['id']
        tenant = res[0]        
        
        if(len(res)==1):
            sql = "SELECT a.date, a_t.attack_name, a.mac_address, a.injected_code FROM `attacks` a, `attack_types` a_t WHERE a.`tenant_id` = %s AND a_t.id = a.type_of_attack ORDER BY a.`date` ASC"            
            cursor.execute(sql, (tenant_id,))        
            data = cursor.fetchall()            
            print(len(data))
            count_sql = "SELECT COUNT(*) as count FROM `attacks` a, `attack_types` a_t WHERE a.`tenant_id` = %s AND a_t.id = a.type_of_attack ORDER BY a.`date` ASC"
            cursor.execute(count_sql, (tenant_id,))        
            res = cursor.fetchone()
            count = res['count']
            print(count)
            return {"status":0, "msg":"Login Successful", "data" : data, "count" : count, "tenant":tenant}
        
        else:
            return {"status":1, "msg":"Invalid Email or Token"}
    
    except:
        return {"status":1, "msg":"Server has some issues. Try again later."}