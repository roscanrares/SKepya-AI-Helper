#include <iostream>
#include <utility>
#include <vector>

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