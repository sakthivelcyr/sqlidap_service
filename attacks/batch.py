from bitap_alg import bitap_algorithm

class batch:
    def check_batch_based_attack(self, input):
        
        inj_pattern = ["'", ";", ";", "#"]
        sql_functions = ["delete", "drop", "truncate", "update", "select", "alter"]        
        bitap = bitap_algorithm()      

        for i in range(len(inj_pattern)):
            if bitap.match_string(input.lower(), inj_pattern[i])>-1:

                if i==0:
                    counter = 0
                    for j in range(len(sql_functions)):

                        if  bitap.match_string(input.lower(), sql_functions[i])>-1:
                            counter += 1
                    
                    if counter ==0:
                        result = False
                        break
                
                if i+1==len(inj_pattern):
                    result = True
            
            else:
                result = False
                break
        return result