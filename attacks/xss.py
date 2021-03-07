from bitap_alg import bitap_algorithm

class xss:
    def check_xss_based_attack(self, input):
        
        inj_pattern = ["<script>", "'", ";","</script>"]              
        bitap = bitap_algorithm()      

        for i in range(len(inj_pattern)):                        
            if bitap.match_string(input.lower(), inj_pattern[i])>-1:                
                if i+1==len(inj_pattern):                    
                    result = True
            
            else:
                result = False
                break
            
        return result