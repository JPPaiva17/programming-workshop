# Hash Table

def twoSum(arr, target):
    hashTable = {}
    for i in range(len(arr)):
        complement = target - arr[i]
        if complement in hashTable:
            return [hashTable[complement], i]

        hashTable[arr[i]] = i
    return []

num = [2, 7, 11, 15]
target = 9
print(twoSum(num, target))
