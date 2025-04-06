```java
import java.util.ArrayList;
import java.util.Collections;

public class Main {

    // Migrating bubbleSort function from C++ to Java
    public static void bubbleSort(ArrayList<Pair<Integer, Integer>> arr) {
        boolean swapped;
        int size = arr.size();
        for (int i = 0; i < size - 1; i++) {
            swapped = false;
            for (int j = 0; j < size - i - 1; j++) {
                if (arr.get(j).getKey() > arr.get(j + 1).getKey()) {
                    // Using Collections.swap for swapping elements in Java
                    Collections.swap(arr, j, j + 1);
                    swapped = true;
                }
            }
            if (!swapped)
                break;
        }
    }

    public static void main(String[] args) {
        int[] raw_arr = {64, 34, 25, 12, 22, 11, 90};
        int size = raw_arr.length;

        ArrayList<Pair<Integer, Integer>> arr = new ArrayList<>();
        for (int i = 0; i < size; i++) {
            // Using Pair class to store elements and their original indices
            arr.add(new Pair<>(raw_arr[i], i));
        }

        System.out.print("Original array with indices: ");
        for (Pair<Integer, Integer> p : arr) {
            System.out.print("(" + p.getKey() + "," + p.getValue() + ") ");
        }

        bubbleSort(arr);

        System.out.print("\nSorted array with original indices: ");
        for (Pair<Integer, Integer> p : arr) {
            System.out.print("(" + p.getKey() + "," + p.getValue() + ") ");
        }
        System.out.println();
    }

    // Implementing a simple Pair class similar to std::pair in C++
    public static class Pair<K, V> {
        private K key;
        private V value;

        public Pair(K key, V value) {
            this.key = key;
            this.value = value;
        }

        public K getKey() {
            return key;
        }

        public V getValue() {
            return value;
        }
    }
}
```

This Java code is a direct migration from the provided C++ code, maintaining the original logic and structure. The `Pair` class is implemented to mimic the `std::pair` functionality from C++, and `Collections.swap` is used for swapping elements in the array list, similar to `std::swap` in C++.