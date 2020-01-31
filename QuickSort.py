from SortBase import SortBase


class QuickSort(SortBase):
    def partition_array(self, arr, low, high):
        i = low - 1  # Element with left-most index
        pivot = arr[high]  # Pivot element chosen at right-most end of array

        for j in range(low, high):
            # If current element is smaller than pivot element
            if arr[j] < pivot:
                # Increment index of smaller element & swap with current element
                i = i + 1
                arr[i], arr[j] = arr[j], arr[i]

                # Only append unique arrays to generation list
                if any(a != b for a, b in zip(self.generations[-1], arr)):
                    self.generations.append(arr.copy())

        # Final element swap & return index of pivot element (now at it's correct position)
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1

    def quick_sort(self, arr, low_index=None, high_index=None):
        if low_index < high_index:
            partition_index = self.partition_array(arr, low_index, high_index)

            # Recursively sort elements before and after partition index
            self.quick_sort(arr, low_index, partition_index - 1)
            self.quick_sort(arr, partition_index + 1, high_index)

        # Only append unique arrays to generation list
        if any(a != b for a, b in zip(self.generations[-1], arr)):
            self.generations.append(arr.copy())

    def sort(self, unsorted):
        super().pre_sort(unsorted)
        self.quick_sort(unsorted, 0, len(unsorted) - 1)
        super().post_sort()
        self.name = "Quick Sort"
        return self.generations
