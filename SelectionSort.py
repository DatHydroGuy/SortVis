from SortBase import SortBase


class SelectionSort(SortBase):
    def selection_sort(self, arr):
        # Traverse through all array elements
        for i in range(len(arr)):

            # Find the minimum element in remaining unsorted array
            min_idx = i
            for j in range(i + 1, len(arr)):
                if arr[min_idx] > arr[j]:
                    min_idx = j

            # Swap the found minimum element with the first element
            arr[i], arr[min_idx] = arr[min_idx], arr[i]

            # Only append unique arrays to generation list
            if any(a != b for a, b in zip(self.generations[-1], arr)):
                self.generations.append(arr.copy())

    def sort(self, unsorted):
        super().pre_sort(unsorted)
        self.selection_sort(unsorted)
        super().post_sort()
        self.name = "Selection Sort"
        return self.generations
