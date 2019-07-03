

def who_do_you_know():
    people_you_know = input("Enter people you know: ")
    people_you_know = people_you_know.split()
    return people_you_know 
    

def ask_user():
    name = input("Enter name: ")
    if name in who_do_you_know():
        print("You know {0}".format(name))
    else:
        print("You don't know {0}".format(name))


ask_user() 
