import functools #needed for decorators

def my_decorator(func):
    @functools.wraps(func)
    def function_that_runs_func():
        print("In the decorator!")
        func()  # without this 'I'm the function' would not print
        print("After the decorator!")
    return function_that_runs_func

@my_decorator
def my_function():
    print("I'm the function")


my_function()
