from SortBase import SortBase


class MergeSort(SortBase):
    def merge_sort(self, pre_arr, arr, post_arr):
        if len(arr) > 1:
            # split array into left and right halves
            mid = len(arr) // 2
            left_array = arr[:mid]
            right_array = arr[mid:]

            # Recursively sort each half
            self.merge_sort(pre_arr, left_array, right_array + post_arr)
            self.merge_sort(pre_arr + left_array, right_array, post_arr)

            i = j = k = 0

            # Copy data from left and right sorted sub-arrays
            while i < len(left_array) and j < len(right_array):
                if left_array[i] < right_array[j]:
                    arr[k] = left_array[i]
                    i += 1
                else:
                    arr[k] = right_array[j]
                    j += 1
                k += 1

            # Copy any leftover elements from left array
            while i < len(left_array):
                arr[k] = left_array[i]
                i += 1
                k += 1

            # Copy any leftover elements from right array
            while j < len(right_array):
                arr[k] = right_array[j]
                j += 1
                k += 1

        # Only append unique arrays to generation list
        next_gen = pre_arr + arr.copy() + post_arr
        if any(a != b for a, b in zip(self.generations[-1], next_gen)):
            self.generations.append(next_gen)

    def sort(self, unsorted):
        super().pre_sort(unsorted)
        self.merge_sort([], unsorted, [])
        super().post_sort()
        self.name = "Merge Sort"
        return self.generations
