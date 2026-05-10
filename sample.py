# sample.py

def greet(name):
    return f"Hello, {name}!"

def add(a, b):
    return a + b

if __name__ == "__main__":
    user_name = input("Enter your name: ")
    print(greet(user_name))

    x = int(input("Enter first number: "))
    y = int(input("Enter second number: "))

    print("Sum =", add(x, y))