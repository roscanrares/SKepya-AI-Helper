import java.util.Collections;
import java.util.List;

public class BubbleSort {

    public static void bubbleSort(List<Pair<Integer, Integer>> arr) {
        boolean swapped;
        int size = arr.size();
        for (int i = 0; i < size - 1; i++) {
            swapped = false;
            for (int j = 0; j < size - i - 1; j++) {
                if (arr.get(j).getFirst() > arr.get(j + 1).getFirst()) {
                    Collections.swap(arr, j, j + 1);
                    swapped = true;
                }
            }
            if (!swapped)
                break;
        }
    }
}