
class Student:
    def __init__(self, name, school):
        self.name = name
        self.school = school
        self.marks = []

    def average(self):
        return sum(self.marks)/len(self.marks)

    @classmethod
    def friend(cls, origin, friend_name, *args, **kwargs):
        return cls(friend_name, origin.school, *args, **kwargs)


anna = Student("Anna", "Oxford")

#friend = anna.friend("Greg")


class WorkingStudent(Student):
    def __init__(self, name, school, salary, job_title):
        # calling students init method
        super().__init__(name, school)
        self.salary = salary
        self.job_title = job_title


anna = WorkingStudent("Anna", "Oxford", 20.00, job_title="Student")
print(anna.salary)

friend = WorkingStudent.friend(
    anna, "Greg", salary=10.00, job_title="Software Developer"
)
print(friend.name)
print(friend.school)
print(friend.salary)

