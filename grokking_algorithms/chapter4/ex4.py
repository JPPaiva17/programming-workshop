# BinarySearch recursive

def binSearch(arr, n, start=0, end=None):
    if end is None:
        end = len(arr) - 1

    if start > end:
        return -1

    middle = (start + end) // 2
    if arr[middle] == n:
        return middle
    
    elif arr[middle] > n:
        return binSearch(arr, n, start, middle - 1)

    else:
        return binSearch(arr, n, middle + 1, end)

search = 777
array = [14, 320, 330, 470, 530, 670, 777, 890, 970, 1000]
print(binSearch(array, search))