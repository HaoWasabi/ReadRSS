
def a(a, b: str, c):
    print(a,b,c)
    
d = a.__code__.co_varnames
print(type(a))