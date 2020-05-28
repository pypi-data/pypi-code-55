from emailValidation import emailValidation
from pyspark.sql import SparkSession
email=input("Enter the input \n")
emailValidation.check(email)



