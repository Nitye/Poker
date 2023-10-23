# class dog():
#   def __init__(self, name, age):
#     self.name = name
#     self.age = age
  
#   def add_age(self, age):
#     dog.age+=age

# d1 = dog('Tim', 34)
# d2 = dog('Bill', 12)
# d1.add_age(10)
# print(d1.age)
# print(d2.age)
class A:
    instances = []
    def __init__(self):
        self.__class__.instances.append(self)
a1 = A()
a2 = A()
print(A.instances)
# dog = [1,22,3]
# dog2 = dog.copy()
# dog.remove(1)
# dog2.remove(1)
# print(dog2)