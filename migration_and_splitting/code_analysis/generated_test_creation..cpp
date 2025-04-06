```cpp
#include <iostream>
#include <utility>
#include <vector>
#include <cassert>

// Function declaration
void bubbleSort(std::vector<std::pair<int, int>>& arr);

// Test functions
void testBubbleSortEmptyVector() {
    std::vector<std::pair<int, int>> arr = {};
    bubbleSort(arr);
    assert(arr.empty());
    std::cout << "testBubbleSortEmptyVector passed." << std::endl;
}

void testBubbleSortSingleElement() {
    std::vector<std::pair<int, int>> arr = {{5, 0}};
    bubbleSort(arr);
    assert(arr.size() == 1 && arr[0].first == 5 && arr[0].second == 0);
    std::cout << "testBubbleSortSingleElement passed." << std::endl;
}

void testBubbleSortAlreadySorted() {
    std::vector<std::pair<int, int>> arr = {{1, 0}, {2, 1}, {3, 2}};
    bubbleSort(arr);
    for (int i = 0; i < arr.size() - 1; ++i) {
        assert(arr[i].first <= arr[i + 1].first);
    }
    std::cout << "testBubbleSortAlreadySorted passed." << std::endl;
}

void testBubbleSortGeneralCase() {
    std::vector<std::pair<int, int>> arr = {{64, 0}, {34, 1}, {25, 2}, {12, 3}, {22, 4}, {11, 5}, {90, 6}};
    bubbleSort(arr);
    int previous = arr[0].first;
    for (int i = 1; i < arr.size(); ++i) {
        assert(previous <= arr[i].first);
        previous = arr[i].first;
    }
    std::cout << "testBubbleSortGeneralCase passed." << std::endl;
}

// Main function to run the tests
int main() {
    testBubbleSortEmptyVector();
    testBubbleSortSingleElement();
    testBubbleSortAlreadySorted();
    testBubbleSortGeneralCase();

    std::cout << "All tests passed successfully." << std::endl;
    return 0;
}

// Function definition
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

This test file includes the original `bubbleSort` function and adds a series of test functions to validate its correctness. Each test function is designed to cover a specific scenario, including sorting an empty vector, a vector with a single element, an already sorted vector, and a general case. The `main` function calls these test functions, and successful execution of all tests confirms the reliability of the `bubbleSort` function.