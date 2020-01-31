from SortBase import SortBase


class BubbleSort(SortBase):
    def bubble_sort(self, unsorted):
        for _ in unsorted:
            swap = False
            for e1 in range(len(unsorted) - 1):
                if unsorted[e1] > unsorted[e1 + 1]:
                    unsorted[e1], unsorted[e1 + 1] = unsorted[e1 + 1], unsorted[e1]
                    self.generations.append(unsorted.copy())
                    swap = True
            if swap is False:
                break

    def sort(self, unsorted):
        super().pre_sort(unsorted)
        self.bubble_sort(unsorted)
        super().post_sort()
        self.name = "Bubble Sort"
        return self.generations
