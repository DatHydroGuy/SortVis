from SortBase import SortBase


class ShellSort(SortBase):
    def shell_sort(self, arr):
        # Initial sub-array size covers half of the array
        n = len(arr)
        sub_array_size = n // 2

        # Do insertion sort for the sub-array size
        # Repeat for smaller sub-array sizes
        # Once sub-array size < 1, array is fully sorted
        while sub_array_size > 0:

            for i in range(sub_array_size, n):
                temp = arr[i]

                # Left-shift elements which are < a[i] until the correct location for a[i] is found
                j = i
                while j >= sub_array_size and arr[j - sub_array_size] > temp:
                    arr[j] = arr[j - sub_array_size]
                    j -= sub_array_size

                # Put a[i] in correct location
                arr[j] = temp

                # Only append unique arrays to generation list
                if any(a != b for a, b in zip(self.generations[-1], arr)):
                    self.generations.append(arr.copy())

            # Reduce the sub-array size
            sub_array_size //= 2

    def sort(self, unsorted):
        super().pre_sort(unsorted)
        self.shell_sort(unsorted)
        super().post_sort()
        self.name = "Shell Sort"
        return self.generations
