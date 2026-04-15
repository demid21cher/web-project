# Task #1
def check_division_error(func):
    def wrapper(a, b):
        if b == 0:
            raise ValueError("Division by zero is not allowed.")
        return func(a, b)

    return wrapper


@check_division_error
def division(a, b):
    return a / b


# Example usage:
# print(division(10, 2))
# print(division(10, 0))
# print(division(0, 0))


# Task #2
def check_index_error(func):
    def wrapper(list, index):
        if index < 0 and index >= len(list):
            raise IndexError("Index out of range.")
        return func(list, index)

    return wrapper


@check_index_error
def get_element(list, index):
    return list[index]


# Example usage:
my_list = [1, 2, 3, 4, 5]
# print(get_element(my_list, 2))
# print(get_element(my_list, 5))
print(get_element(my_list, -1))
print(get_element(my_list, None))
