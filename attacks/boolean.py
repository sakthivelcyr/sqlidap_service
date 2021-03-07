from bitap_alg import bitap_algorithm

class boolean:
    
    def check_boolean_based_attack(self, input):
        
        inj_pattern = ["'", "'", "'", "'", "'", "#"]
        logical_operators = ["or", "||"]
        relational_operators = ["=", ">", ">=", "<", "<=", "<>", "!="]

        bitap = bitap_algorithm()
                
        for i in range(len(inj_pattern)):
                        
            if bitap.match_string(input.lower(), inj_pattern[i])>-1 :
                
                if i==0:                    
                    counter = 0
                    for j in range(len(logical_operators)):
                        if bitap.match_string(input.lower(), logical_operators[j])>-1 :
                            counter = counter + 1
                    
                    if counter==0:
                        result = False
                        break
                
                if i==2:                    
                    counter = 0
                    for k in range(len(relational_operators)):
                        if bitap.match_string(input.lower(), relational_operators[k])>-1 :
                            counter = counter + 1
                    
                    if counter==0:
                        result = False
                        break   
                
                if i+1 == len(inj_pattern):                                        
                    result = True                                

            else:                
                result = False
                break
        
        return result
