class bitap_algorithm:
    def match_string(self, text, pattern):                
        # Length of pattern
        m = len(pattern)

        # Initialize ~1
        A = ~1
        
        # If length is 0 or exceeds 63 then return "No match"
        if m==0:
            return -1        
        elif m>63:
            #print("Pattern is too long")
            return -1

        # Preparing bit masks
        p_mask = [~0 for i in range(300)]

        #Taking the pattern as index of PATTERN MASK then apply AND operator with complement of 1 by LEFT SHIFT by i times
        for i in range(m):        
            p_mask[ord(pattern[i])] &= ~(1<<i)            

        # Apply OR with pattern_mask
        for i in range(len(text)):
            A |= p_mask[ord(text[i])]
            A <<= 1
            if (A&(1<<m))==0:
                return i-m+1
        return -1