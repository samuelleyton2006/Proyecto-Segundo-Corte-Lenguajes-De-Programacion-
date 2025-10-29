try:
    x = 1 / 0
except ZeroDivisionError:
    print("Error")
finally:
    print("Fin")