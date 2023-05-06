# python decorators


def handle_0(func):

    def inner(a, b):
        if b == 0:
            return 'you cannot divide by zero'
        return func(a, b)

    return inner


@handle_0
def divide(a, b):
    return a / b


print(divide(2, 3))
print(divide(3, 0))
