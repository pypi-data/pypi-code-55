'''
    用于计算公司员工的薪资
'''

def yearSalary(monthSalary):
    """根据传入的月薪的值，计算出年薪：monthsalary*12"""
    return monthSalary*12

def daySalary(monthsalary):
    """根据传入的月薪值，计算出一天的薪资。一个月按照22.5天计算（国家规定的工作日）"""
    return monthsalary/22.5



