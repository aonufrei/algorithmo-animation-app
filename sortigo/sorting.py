from abc import abstractmethod

class Sorting():
    @abstractmethod
    def set_array(self, array):
        raise NotImplementedError

    @abstractmethod
    def sort_iteration(self, iteration:int=0):
        raise NotImplementedError
    
    @abstractmethod
    def get_all_iterations(self):
        raise NotImplementedError

    @abstractmethod
    def clean_array(self):
        raise NotImplementedError


class BubbleSemiSort(Sorting):
    def __init__(self, array=[]):
        self.set_array(array)

    def set_array(self, array):
        self.array = array

    def sort_iteration(self, iteration:int=0):
        try:
            for x in range(len(self.array)-1):
                if self.array[x] > self.array[x+1]:
                    self.array[x], self.array[x+1] = self.array[x+1], self.array[x]
            return True
        except:
            return False

    def get_all_iterations(self):
        result_iterations = []
        it = 0
        for it in range(len(self.array)-1-it):
            self.sort_iteration(it)
            result_iterations.append(self.array)
        return result_iterations

    def clean_array(self):
        self.array = []
