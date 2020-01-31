from SortBase import SortBase


class HeapSort(SortBase):
    def heapify(self, arr, n, i):
        largest = i         # Root
        left = 2 * i + 1    # Left child
        right = 2 * i + 2   # Right child

        # If left child exists and is greater than root, make it the new root
        if left < n and arr[i] < arr[left]:
            largest = left

        # If right child exists and is greater than root, make it the new root
        if right < n and arr[largest] < arr[right]:
            largest = right

        # Change root if necessary
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]

            # Heapify the new root
            self.heapify(arr, n, largest)

    def heap_sort(self, arr):
        n = len(arr)

        # Build a maxheap
        for i in range(n, -1, -1):
            self.heapify(arr, n, i)

        # Extract elements from unordered sub-heap
        for i in range(n - 1, 0, -1):
            arr[i], arr[0] = arr[0], arr[i]
            self.heapify(arr, i, 0)

            # Only append unique arrays to generation list
            if any(a != b for a, b in zip(self.generations[-1], arr)):
                self.generations.append(arr.copy())

    def sort(self, unsorted):
        super().pre_sort(unsorted)
        self.heap_sort(unsorted)
        super().post_sort()
        self.name = "Heap Sort"
        return self.generations
