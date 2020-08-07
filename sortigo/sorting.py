class Sorting():
    
    @staticmethod
    def sort_iteration(array:list):
        raise NotImplementedError
    @staticmethod
    def get_all_iterations(array:list):
        raise NotImplementedError



class BubbleSemiSort():
    
    @staticmethod
    def sort_iteration(array:list):
        buffer = array
        for x in range(len(buffer)-1):
            if buffer[x] > buffer[x+1]:
                buffer[x], buffer[x+1] = buffer[x+1], buffer[x]
        
        return buffer

    @staticmethod
    def get_all_iterations(array:list):
        result_iterations = []
        buffer = array[:]
        result_iterations.append(buffer[:])
        it = 0
        for it in range(len(buffer)-1-it):
            iteration = BubbleSemiSort.sort_iteration(buffer)
            result_iterations.append(iteration[:])

        return result_iterations