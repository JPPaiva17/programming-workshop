# Divide to conquer, recursive sum

def recursiveSum(arr):
    if not arr:
        return 0
    if arr:
        return arr[0] + recursiveSum(arr[1:])

array = [2, 4, 6]
print(recursiveSum(array))