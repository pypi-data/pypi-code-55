import math

def calculate_bmi(weight, height):
    assert weight > 0
    assert height > 0
    precise_value = weight / (math.pow(height, 2))
    return math.ceil(precise_value)

def classify_bmi(weight, height):

    def isNormal(bmi):
        return bmi >= 18.5 and bmi <= 25

    def isUnderweight(bmi):
        return bmi < 18.5

    def isOverweight(bmi):
        return bmi > 25

    bmi = calculate_bmi(weight, height)
    
    if(isNormal(bmi)):
         return "normal"
    if(isUnderweight(bmi)):
         return "underweight"
    if(isOverweight(bmi)):
         return "overweight"