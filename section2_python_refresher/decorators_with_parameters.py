import functools

# Looking at decorators that will accept arguements

def decorator_with_arguments(number):
    def my_decorator(func):
        @functools.wraps(func)
        def function_that_runs(*args, **kwargs):
            print("In decorator.")
            if number == 56:
                print('Not running the function')
            else:
                func(*args, **kwargs)
            print("After decorator.")
        return function_that_runs
    return my_decorator


@decorator_with_arguments(57)
def my_function_too(x, y):
    print("Boo!!!")
    print(x+y)


my_function_too(46, 99)
