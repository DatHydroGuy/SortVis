from SortBase import SortBase


class CountSort(SortBase):
    def count_sort(self, arr):
        # The output array that will contain the sorted array
        output = [0 for _ in range(max(arr) - min(arr) + 1)]

        # Count array to store count of individual elements
        count = [0 for _ in range(len(output))]

        # Store count of each element
        for i in range(len(arr)):
            count[arr[i] - min(arr)] += 1

        # Change count[i] so that count[i] now contains actual
        # position of this character in output array
        for i in range(1, len(count)):
            count[i] += count[i - 1]

        # Build the output character array
        for i in range(len(arr)):
            output[count[arr[i] - min(arr)] - 1] = arr[i]
            count[arr[i] - min(arr)] -= 1

        # Copy the output array to arr, so that arr now
        # contains sorted characters
        for i in range(len(arr)):
            arr[i] = output[i]

        # Only append unique arrays to generation list
        if any(a != b for a, b in zip(self.generations[-1], arr)):
            self.generations.append(arr.copy())

    def sort(self, unsorted):
        super().pre_sort(unsorted)
        self.count_sort(unsorted)
        super().post_sort()
        self.name = "Count Sort"
        return self.generations
