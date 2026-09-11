#   Ordenacao por selecao, e um algoritmo de ordenacao mas e ruim pois sua BigO notation e O(n²)
def findSmaller(arr):
    smaller = arr[0]
    smaller_index = 0
    for i in range(1, len(arr)):
        if arr[i] < smaller:
            smaller_index = i
    return smaller_index

def SelectionSort(arr):
    sorted_list = []
    for _ in range(len(arr)):
        smaller_index = findSmaller(arr)
        sorted_list.append(arr.pop(smaller_index))
    return sorted_list

print(SelectionSort([5, 3, 6, 2, 10]))