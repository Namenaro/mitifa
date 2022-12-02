import matplotlib.pyplot as plt
import numpy as np
import random


class Hist:
    def __init__(self, sample):
        self.sample = sample

    def get_probability_of_event(self, real_value, predicted_value):
        # Считаем все образцы, которые попадают в событие
        counter_of_fitted = 0
        left_val = min(real_value, predicted_value)
        right_val = max(real_value, predicted_value)
        for example in self.sample:
            if left_val <= example <= right_val:
                counter_of_fitted+=1
        prob_of_event = counter_of_fitted/len(self.sample)
        return prob_of_event

    def show_hist(self):
        plt.hist(self.sample, density=True, edgecolor="black")
        plt.show()


class BinaryHist:
    def __init__(self, sample):
        self.sample = sample

    def get_probability_of_event(self, binary_value):

        heights, bin_edges = np.histogram(self.sample, density=True)
        bin_width = bin_edges[1] - bin_edges[0]

        if binary_value == 0:
            return bin_width * heights[0]

        elif binary_value == 1:
            return bin_width * heights[-1]

        else:
            print("Non-binary value!")
            return None

    def show_hist(self):
        plt.hist(self.sample, density=True, edgecolor="black")
        plt.show()

if __name__ == '__main__':
    sample = []
    for i in range(1000):
        sample.append(random.randint(0, 25))

    my_hist = Hist(sample)
    print(f"Probability is: {my_hist.get_probability_of_event(0, 25)}")
    my_hist.show_hist()

    sample = []
    for i in range(1000):
        sample.append(random.randint(0, 1))

    my_hist = BinaryHist(sample)
    print(f"Probability of 0 is: {my_hist.get_probability_of_event(0)}")
    print(f"Probability of 1 is: {my_hist.get_probability_of_event(1)}")
    my_hist.show_hist()
