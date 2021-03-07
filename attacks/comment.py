from bitap_alg import bitap_algorithm

class comment:
    def check_comment_based_attack(self, input):
        inj_pattern = ["'", "-"]        
        bitap = bitap_algorithm()

        for i in range(len(inj_pattern)):
                        
            if bitap.match_string(input, inj_pattern[i])>-1 :                
                
                if i+1 == len(inj_pattern):                    
                    result = True                
            
            else:
                result = False
                break
        
        return result 