#include <iostream>
#include <vector>

using namespace std;

void backtrack(vector<int>& nums, vector<int>& current, int start, vector<vector<int>>& result) {
    result.push_back(current); // Add the current combination to the result

    for (int i = start; i < nums.size(); i++) {
        current.push_back(nums[i]); // Add current element to the combination
        backtrack(nums, current, i + 1, result); // Explore further with the next elements
        current.pop_back(); // Backtrack: Remove the last element to explore other combinations
    }
}

vector<vector<int>> combine(vector<int>& nums) {
    vector<vector<int>> result;
    vector<int> current;
    backtrack(nums, current, 0, result); // Start backtracking from index 0
    return result;
}

int main() {
    vector<int> nums = {1, 2, 3}; // Example input
    vector<vector<int>> combinations = combine(nums);

    // Print all combinations
    cout << "Combinations: \n";
    for (const auto& combo : combinations) {
        cout << "[ ";
        for (int num : combo) {
            cout << num << " ";
        }
        cout << "]\n";
    }

    return 0;
}
