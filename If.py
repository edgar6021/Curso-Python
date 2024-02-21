usuario= "Juan"
password = "12345678"
passwordIng=""
usuarioIng=""

usuarioIng= input("Ingresa tu usuario: ")
passwordIng=input("Ingresa tu password: ")

if usuarioIng == usuario and passwordIng == password:
    print ("Bienvenido",usuario)
else:
    print("Usuario o contraseña incorrectos")
    