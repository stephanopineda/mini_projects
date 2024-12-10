#   This python file is made to create solutions for the course 'Numerical Methods'
#   Created: May 15, 2021
#   Last Modified: June 3, 2021
#   This aims to provide a text output that can be copied to a word document
#   The solution uses Newton-Raphson method
#   Note: I forgot how I change the code to handle other type of functions 

import math

def function(equation, p, sub):
    equation = equation.replace("x", "(" + str(p) + ")")
    print("\tf({}) = {}".format("p_" + str(sub), equation).replace("math.", ""))
    equation = equation.replace("^", "**") \
        .replace("(", "(") \
        .replace(")", ")")
    print("\tf(p_" + str(sub) + ") = " + str(round(eval(equation), 5)).replace("math.", ""))
    return round(eval(equation), 5)

# Enter the equation in the func variable
# func = "1.25x^3 - 2.9375x^2 - 71.375x + 73.0625"
func = "3 * math.log10 x - math.e^-x"
# p_0 = 4.2
p_0 = 1
# p_1 = 5.5 # 5.5
p_1 = 5

print("Given: f(x)={}; [{},{}]; ε_a ≤ 0.02%".format(func, str(p_0), str(p_1)))
print("Required: Pn")
print("Solution: ")
print("f(x) = {}".format(func))

first = 0
second = 1
relErrorFormula = 100
while relErrorFormula > 1:
    print("@p_{} = {} & p_{} = {}".format(str(first), str(p_0), str(second), str(p_1)))
    value1 = function(func, p_0, first)
    value2 = function(func, p_1, second)

    third = second + 1
    secantMethFormula = "p_{} - [f(p_{})*(p_{} - p_{})] / [f(p_{}) - f(p_{})]"\
        .format(str(second), str(second), str(second), str(first), str(second), str(first))
    print("p_{} = {}".format(str(third), secantMethFormula))
    thirdFunc = secantMethFormula.replace("f(p_{})".format(first), str(value1))\
        .replace("f(p_{})".format(second), str(value2))\
        .replace("p_{}".format(first), str(p_0))\
        .replace("p_{}".format(second), str(p_1))
    print("\tp_{} = {}".format(str(third), thirdFunc))

    p_2 = round(eval(thirdFunc.replace("[", "(").replace("]", ")")), 5)
    print("\tp_{} = {}".format(str(third), p_2))

    relErrorFormula = round(100 * abs((p_2 - p_1)/p_2), 2)
    print("ε_a = |(p_current - p_prev)/p_current| 100%")
    print("ε_a = |({} - {})/{}| 100%".format(str(p_1), str(p_0), str(p_1)))
    print("ε_a = " + str(relErrorFormula) + "%\n")

    first = first + 1
    second = second + 1
    p_0 = p_1
    p_1 = p_2
