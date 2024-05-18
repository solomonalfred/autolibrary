# Определяем несколько функций
def add(x, y):
    return x + y

def multiply(x, y):
    return x * y

def greet(name):
    return f"Hello, {name}!"

# Создаем словарь с функциями
functions = {
    'add': add,
    'multiply': multiply,
    'greet': greet
}

# Вызываем функции из словаря с аргументами
result1 = functions['add'](3, 4)
result2 = functions['multiply'](2, 5)
result3 = functions['greet']('Alice')

print(result1)  # Вывод: 7
print(result2)  # Вывод: 10
print(result3)  # Вывод: Hello, Alice!
