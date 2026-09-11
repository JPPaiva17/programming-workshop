# Recusrsive biggest value in an array

def recursiveBiggestValue(arr):
    if len(arr) == 1:
        return arr[0]
    
    if not arr:
        return 0 
        
    sub_max = recursiveBiggestValue(arr[1:])
    return arr[0] if arr[0] > sub_max else sub_max

#array = [14, 32, 33, 47, 53, 67, 777, 89, 97, 10]
array = [-14, -32, -33, -47, -53, -67, -777, -89, -97]
print(recursiveBiggestValue(array))
