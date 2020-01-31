from SortBase import SortBase


class InsertionSort(SortBase):
    def insertion_sort(self, arr):
        for i in range(1, len(arr)):

            key = arr[i]

            # Scan elements with index less than i (these will be sorted by definition).
            # For any which are larger than arr[i], increase index by 1, and insert arr[i] in the gap
            j = i - 1
            while j >= 0 and key < arr[j]:
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = key

            # Only append unique arrays to generation list
            if any(a != b for a, b in zip(self.generations[-1], arr)):
                self.generations.append(arr.copy())

    def sort(self, unsorted):
        super().pre_sort(unsorted)
        self.insertion_sort(unsorted)
        super().post_sort()
        self.name = "Insertion Sort"
        return self.generations
