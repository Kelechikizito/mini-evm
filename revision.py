# Revision of the Python concepts


# Class
class Person:
    # The constructor method to initialize new objects of the class
    def __init__(self, name, age, height, weight, country):
        self.name = name
        self.age = age
        self.height = height
        self.weight = weight
        self.country = country

    def introduction(self):
        return f"My name is {self.name}, I am {self.age} years old, {self.height} feets tall, weigh {self.weight} kg, and I am from {self.country}."


kelechi_kizito_ugwu = Person("Billionaire", 23, 6, 79.5, "Nigeria")
print(kelechi_kizito_ugwu.introduction())
