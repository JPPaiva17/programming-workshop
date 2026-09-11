# recursive array size counter

def recursiveCounter(arr):
    if not arr:
        return 0
    else:
        return 1 + recursiveCounter(arr[1:])

array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print(recursiveCounter(array))
