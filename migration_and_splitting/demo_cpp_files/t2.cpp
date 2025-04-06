#include <iostream>
#include <vector>
#include <cmath>
#include <algorithm>

using namespace std;

int binarySearch(const vector<int>& list, int target) {
    int left = 0, right = list.size() - 1;
    while (left <= right) {
        int mid = left + (right - left) / 2;
        if (list[mid] == target) {
            return mid;
        }
        if (list[mid] < target) {
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }
    return -1;
}

vector<int> mergeSort(const vector<int>& list) {
    if (list.size() <= 1) return list;
    int mid = list.size() / 2;
    vector<int> left(list.begin(), list.begin() + mid);
    vector<int> right(list.begin() + mid, list.end());
    
    left = mergeSort(left);
    right = mergeSort(right);
    
    vector<int> result;
    int i = 0, j = 0;
    while (i < left.size() && j < right.size()) {
        if (left[i] <= right[j]) {
            result.push_back(left[i]);
            i++;
        } else {
            result.push_back(right[j]);
            j++;
        }
    }
    result.insert(result.end(), left.begin() + i, left.end());
    result.insert(result.end(), right.begin() + j, right.end());
    return result;
}

vector<int> bubbleSort(const vector<int>& list) {
    vector<int> arr = list;
    for (size_t i = 0; i < arr.size(); i++) {
        for (size_t j = 0; j < arr.size() - i - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                swap(arr[j], arr[j + 1]);
            }
        }
    }
    return arr;
}

double toDecimal(int binary) {
    double decimal = 0;
    int base = 1;
    while (binary > 0) {
        int lastDigit = binary % 10;
        decimal += lastDigit * base;
        base *= 2;
        binary /= 10;
    }
    return decimal;
}

int toBinary(double decimal) {
    int binary = 0;
    int remainder, i = 1;
    while (decimal != 0) {
        remainder = static_cast<int>(decimal) % 2;
        binary += remainder * i;
        decimal /= 2;
        i *= 10;
    }
    return binary;
}

long long factorial(int n) {
    return (n == 0) ? 1 : n * factorial(n - 1);
}

void performOperations() {
    int num1 = 10, num2 = 5;

    vector<int> sortedList1 = mergeSort({num1, num2});
    vector<int> sortedList2 = bubbleSort({num1, num2});

    double decimal1 = toDecimal(num1);
    double decimal2 = toDecimal(num2);

    int binary1 = toBinary(decimal1);
    int binary2 = toBinary(decimal2);

    int sum = binary1 + binary2;

    long long factorialResult = factorial(binary1) + factorial(binary2);

    cout << "Binary Search Result (find 5 in sorted list): " << binarySearch(sortedList1, 5) << endl;
    cout << "Sorted List (Merge Sort): ";
    for (int n : sortedList1) cout << n << " ";
    cout << endl;

    cout << "Sorted List (Bubble Sort): ";
    for (int n : sortedList2) cout << n << " ";
    cout << endl;

    cout << "Decimal of " << num1 << ": " << decimal1 << endl;
    cout << "Decimal of " << num2 << ": " << decimal2 << endl;
    cout << "Binary of " << num1 << ": " << binary1 << endl;
    cout << "Binary of " << num2 << ": " << binary2 << endl;
    cout << "Sum of binary numbers: " << sum << endl;
    cout << "Factorial of binary 1: " << factorial(binary1) << endl;
    cout << "Factorial of binary 2: " << factorial(binary2) << endl;
    cout << "Sum of factorials: " << factorialResult << endl;
}

int main() {
    performOperations();
    return 0;
}
