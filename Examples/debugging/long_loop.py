# Exceptions
def long_loop():
    for i in range(int(1e04)):
        i+1
        if i == 777:
            # can customize exception messages
            raise Exception("terrible bug")
    result = 1 + 1
    return result

print(long_loop())

s = "next statement"        
# Will this print? Why or why not?
print(s)
