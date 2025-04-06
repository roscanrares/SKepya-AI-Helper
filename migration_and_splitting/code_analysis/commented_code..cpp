```cpp
// Including necessary libraries for the program
#include <iostream> // For input and output operations
#include <utility>  // For std::pair to store pairs of integers
#include <vector>   // For std::vector to store a dynamic array of elements

// Function declaration and definition
void bubbleSort(std::vector<std::pair<int, int>>& arr) {
    // Initialize a boolean variable to keep track of swapping
    bool swapped;
    // Determine the size of the vector
    int size = arr.size();
    // Outer loop to control the number of passes
    for (int i = 0; i < size - 1; i++) {
        // Reset swapped to false on each pass
        swapped = false;
        // Inner loop to compare adjacent elements
        for (int j = 0; j < size - i - 1; j++) {
            // If the first element of the pair is greater than the next, swap them
            if (arr[j].first > arr[j + 1].first) {
                std::swap(arr[j], arr[j + 1]);
                // Mark swapped as true if a swap has occurred
                swapped = true;
            }
        }
        // If no elements were swapped, the array is sorted, and we can break out of the loop
        if (!swapped)
            break;
    }
}

// Main function to demonstrate the sorting of an array of pairs
int main() {
    // Initialize an array of integers
    int raw_arr[] = {64, 34, 25, 12, 22, 11, 90};
    // Calculate the size of the array
    int size = sizeof(raw_arr) / sizeof(raw_arr[0]);

    // Create a vector to store pairs of integers
    std::vector<std::pair<int, int>> arr;
    // Populate the vector with elements from raw_arr and their original indices
    for(int i = 0; i < size; i++) {
        arr.push_back({raw_arr[i], i});
    }

    // Print the original array with indices
    std::cout << "Original array with indices: ";
    for (const auto& p : arr) {
        std::cout << "(" << p.first << "," << p.second << ") ";
    }

    // Call the bubbleSort function to sort the array based on the first element of the pairs
    bubbleSort(arr);

    // Print the sorted array while maintaining the original indices
    std::cout << "\nSorted array with original indices: ";
    for (const auto& p : arr) {
        std::cout << "(" << p.first << "," << p.second << ") ";
    }
    std::cout << std::endl;

    // Return 0 to indicate successful completion
    return 0;
}
```

This code demonstrates the use of the bubble sort algorithm to sort a vector of integer pairs based on the first element of each pair. It includes a `main` function that initializes an array of integers, pairs each element with its original index, and then sorts these pairs using the `bubbleSort` function. The sorting is based solely on the first element of each pair, allowing the original indices to be preserved. This is particularly useful in scenarios where the original position of each element needs to be tracked after sorting.