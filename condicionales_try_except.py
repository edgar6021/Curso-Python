entrada ="hello"


try: 
    numero = int(entrada)
    print(f"El doble del numero es {numero * 2}")
except ValueError:
    print("La entrada no es un numero valido")