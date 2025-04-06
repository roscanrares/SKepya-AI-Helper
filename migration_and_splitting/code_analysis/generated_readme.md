# Bubble Sort Algorithm for Sorting Integer Pairs

This document provides an overview of a simple C++ program that demonstrates the use of the bubble sort algorithm to sort an array of integer pairs. The sorting is based on the first element of each pair.

## Libraries Used

The program utilizes the following standard C++ libraries:
- `iostream` for input and output operations.
- `utility` for the `std::pair` container.
- `vector` for using dynamic array `std::vector`.

## Functions

### `bubbleSort`

#### Description
The `bubbleSort` function sorts a vector of integer pairs based on the first element of each pair using the bubble sort algorithm. The bubble sort is a simple sorting algorithm that repeatedly steps through the list, compares adjacent elements, and swaps them if they are in the wrong order. The pass through the list is repeated until the list is sorted.

#### Code
```cpp
void bubbleSort(std::vector<std::pair<int, int>>& arr) {
    bool swapped;
    int size = arr.size();
    for (int i = 0; i < size - 1; i++) {
        swapped = false;
        for (int j = 0; j < size - i - 1; j++) {
            if (arr[j].first > arr[j + 1].first) {
                std::swap(arr[j], arr[j + 1]);
                swapped = true;
            }
        }
        if (!swapped)
            break;
    }
}
```

This function is marked as an algorithm (`is_algorithm: True`) because it implements the bubble sort algorithm for sorting.

## Main Function

### Description
The `main` function demonstrates the sorting of an array of pairs where each pair consists of an integer from the original array and its index. This is done using the `bubbleSort` function defined above. The program first creates a vector of pairs from a hard-coded array of integers, where each pair is an integer and its index. It then prints the original array of pairs, sorts the pairs using `bubbleSort`, and finally prints the sorted array of pairs.

### Code
```cpp
int main() {
    int raw_arr[] = {64, 34, 25, 12, 22, 11, 90};
    int size = sizeof(raw_arr) / sizeof(raw_arr[0]);

    std::vector<std::pair<int, int>> arr;
    for(int i = 0; i < size; i++) {
        arr.push_back({raw_arr[i], i});
    }

    std::cout << "Original array with indices: ";
    for (const auto& p : arr) {
        std::cout << "(" << p.first << "," << p.second << ") ";
    }

    bubbleSort(arr);

    std::cout << "\nSorted array with original indices: ";
    for (const auto& p : arr) {
        std::cout << "(" << p.first << "," << p.second << ") ";
    }
    std::cout << std::endl;

    return 0;
}
```

This function is not marked as an algorithm (`is_algorithm: False`) because it primarily serves to demonstrate the use of the `bubbleSort` function rather than implementing a sorting algorithm itself.

## Conclusion

This program illustrates a basic application of the bubble sort algorithm to sort an array of integer pairs based on the first element. It demonstrates fundamental C++ programming concepts, including the use of vectors, pairs, and sorting algorithms.