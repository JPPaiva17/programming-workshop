# QuickSort

def quicksort(arr):
    if len(arr) < 2:
        return arr
    else:
        pivot = arr[0]
        smallerThanPivot = [n for n in arr[1:] if n <= pivot]
        biggerThanPivot = [n for n in arr[1:] if n > pivot]
        return quicksort(smallerThanPivot) + [pivot] + quicksort(biggerThanPivot)

array = [5, 7, 2, 4, 1, 3, 6]
print(quicksort(array))