#Bucle For Basico
for i in range(10):
    print(i)
    
#Bucle para iterar sobre una lista
frutas = ['Manzana','Banana','Cereza','Uva']
for fruta in frutas:
        print(fruta)

#Bucle For con indices
for indice, valor in enumerate(['a', 'b', 'c','h']):
    print(f'Indice: {indice}, Valor: {valor}')

#Bucle con else

for i in range(5):
    print(i)
else:
    print("El bucle ha terminado sin interrupciones.")

#Bucle con continue
for i in range(10):
    if i % 2 == 0:
        continue
    print(i)

#Bucle con Break
for i in range(10):
    if i == 9:
        break
    print(i)
#Bucle con ZIP
nombres = ['Juan', 'Ana', 'Pedro']
edades = [25, 30, 35]
for nombre, edad in zip(nombres, edades):
    print(f'{nombre} tiene {edad} year')

#Bucle con reversed
for i in reversed(range(5)):
    print(i)
    
#Bucle con sorted
for i in sorted([3,1,4,1,5,9,2]):
    print(i)
print("##################################################")
#Bucle con iterador personalizado:
class Contador:
    def __init__(self, inicio, fin):
        self.inicio=inicio
        self.fin=fin
        
    def __iter__(self):
        return self
    def __next__(self):
        if self.inicio < self.fin:
            self.inicio +=1
            return self.inicio - 1
        else:
            raise StopIteration
for i in Contador(3, 8):
    print(i)
    
print("######################################################")
#Bucle con funciones lambda
numeros=[1,2,3,4,5,6,7,8,9,10]

CUBO = map(lambda x: x**3, numeros)
for cubito in CUBO:
    print(cubito)
    

#Bucle con comprension de listas:
pares_al_cuadrado = [x**2 for x in range(10) if x % 2 == 0]
print(pares_al_cuadrado)

#Bucle con operador ternario:
pares = [x if x % 2 == 0 else "impar" for x in range(20)]
print(pares)


    