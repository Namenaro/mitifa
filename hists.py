import matplotlib.pyplot as plt
import numpy as np
import random


class Hist:
    def __init__(self, sample):
        self.sample = sample

    @staticmethod
    def get_bin(bin_edges, val):
        if val == bin_edges[-1]:
            return len(bin_edges) - 2
        else:
            for i in range(len(bin_edges) - 1):
                if bin_edges[i] <= val < bin_edges[i + 1]:
                    return i
        return -1

    def get_probability_of_event(self, real_value, predicted_value):

        if real_value < predicted_value:
            min = real_value
            max = predicted_value

        elif real_value > predicted_value:
            min = predicted_value
            max = real_value

        elif real_value == predicted_value:
            return 0

        heights, bin_edges = np.histogram(self.sample, density=True)

        bin_width = bin_edges[1] - bin_edges[0]
        left_bin = self.get_bin(bin_edges, min)
        right_bin = self.get_bin(bin_edges, max)

        if left_bin == -1 or right_bin == -1:
            return None

        if left_bin == right_bin:
            prob = (max - min) * heights[left_bin]
            return prob

        else:
            left_border = bin_edges[left_bin + 1] - min
            right_border = max - bin_edges[right_bin]

            border_sum = left_border * heights[left_bin] + right_border * heights[right_bin]
            prob = bin_width * sum(heights[left_bin + 1:right_bin]) + border_sum

        return prob

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
