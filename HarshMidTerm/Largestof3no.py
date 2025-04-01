def find_largest(num1, num2, num3):
    if num1 >= num2 and num1 >= num3:
        return num1
    elif num2 >= num1 and num2 >= num3:
        return num2
    else:
        return num3

if __name__ == "__main__":
    a = 10
    b = 20
    c = 15
    largest = find_largest(a, b, c)
    print(f"The largest number is: {largest}")
