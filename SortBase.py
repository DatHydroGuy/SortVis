class SortBase:
    def __init__(self):
        self.generations = []
        self.name = ''

    def pre_sort(self, unsorted):
        self.generations = [unsorted.copy()] + [unsorted.copy()]

    def post_sort(self):
        self.generations.append(self.generations[-1].copy())
