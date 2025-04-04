
num = 0
try:
    if num == "force" :
        print("Foo")
    elif num !="":
        float(num)
        print("Bar")
    else:
        print("Baz")
except ValueError:
    print("qux")