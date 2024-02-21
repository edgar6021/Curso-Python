numeros = [2,4,6,8,10]

if all(num % 2 == 0 for num in numeros):
    print(all(numeros))
if any(num % 3 == 0 for num in numeros):
    print(any(numeros))