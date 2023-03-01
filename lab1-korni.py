a,b,c = map(float, input('Введите коэффициенты через пробел:').split())
D = b**2-4*a*c
x1,x2=(-b-D**0.5)/(2*a),(-b+D**0.5)/(2*a)
print(f'x1 = {x1}; x2 = {x2}') if D>=0 else print('Нет корней')