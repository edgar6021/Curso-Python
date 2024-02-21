import re

texto = "python es genial, python es poderoso"
nuevo_texto = re.sub(r'\bpython\b', 'JavaScript', texto, flags=re.IGNORECASE)
print("Nuevo texto:", nuevo_texto)

new = re.findall(r'\bes\b', nuevo_texto, flags=re.IGNORECASE)
print(new)



