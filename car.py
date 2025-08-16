class Car:

    def __init__(self,brand,model,year):
        self.brand = brand
        self.model = model
        self.year = year

    def brand1 (self):
        print(self.brand,self.model,self.year)


Car1 = Car("Toyota","CC",356)
Car2 = Car("BMW","BB",124)
Car3 = Car("Merc","AA",1345)

Car1.brand1()
Car2.brand1()
Car3.brand1()