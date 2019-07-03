class LotteryPlayer:
    def __init__(self, name):
        self.name = name
        self.numbers = (1, 2, 3, 4, 5, 6)

    def total(self):
        return sum(self.numbers)


player_one = LotteryPlayer('Danny')
player_two = LotteryPlayer('Christina')

#print(player_one.name)
#print(player_one.numbers)
#print(player_one.total())



###################################

class Student:
    def __init__(self, name, school, marks):
        self.name = name
        self.school = school
        self.marks = []
    
    def average(self):
        return sum(self.marks)/len(self.marks)

    @classmethod
    def go_to_school(cls):
        print("I go to school")
        print("I'm a {}".format(cls))

    @staticmethod
    def go_to_school_again():
        print("I go to school")

anna = Student(name="Anna", school="MIT", marks=[])

anna.marks.append(56)

print(anna.name)
print(anna.average())
Student.go_to_school()
Student.go_to_school_again()
