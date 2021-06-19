import numpy as np


class GeneticHelper:
    """This class encapsulates the Knapsack 0-1 Problem from RosettaCode.org
    """

    def __init__(self):

        # initialize instance variables:
        self.items = []
        self.maxCapacity = 0

    def __len__(self):
        """
        :return: the total number of items defined in the problem
        """
        return len(self.items)

    def initData(self, block_ids, block_wts, block_fee, maxCapacity):
        """initializes the RosettaCode.org knapsack 0-1 problem data
        """
        self.items = list(zip(block_ids, block_wts, block_fee))
        self.maxCapacity = maxCapacity

    def getValue(self, zeroOneList):
        """
        Calculates the value of the selected items in the list, while ignoring items that will cause the accumulating weight to exceed the maximum weight
        :param zeroOneList: a list of 0/1 values corresponding to the list of the problem's items. '1' means that item was selected.
        :return: the calculated value
        """
        totalWeight = totalValue = 0

        for i in range(len(zeroOneList)):
            item, weight, value = self.items[i]
            if totalWeight + weight <= self.maxCapacity:
                totalWeight += zeroOneList[i] * weight
                totalValue += zeroOneList[i] * value
        return totalValue

    def printItems(self, zeroOneList):
        """
        Prints the selected items in the list, while ignoring items that will cause the accumulating weight to exceed the maximum weight
        :param zeroOneList: a list of 0/1 values corresponding to the list of the problem's items. '1' means that item was selected.
        """
        totalWeight = totalValue = 0

        for i in range(len(zeroOneList)):
            item, weight, value = self.items[i]
            if totalWeight + weight <= self.maxCapacity:
                if zeroOneList[i] > 0:
                    totalWeight += weight
                    totalValue += value
                    print("- Adding {}: weight = {}, value = {}, accumulated weight = {}, accumulated value = {}".format(
                        item, weight, value, totalWeight, totalValue))
        print("- Total weight = {}, Total value = {}".format(totalWeight, totalValue))


# # testing the class:
# def main():
#     # create a problem instance:
#     knapsack = GeneticHelper()

#     # creaete a random solution and evaluate it:
#     randomSolution = np.random.randint(2, size=len(knapsack))
#     print("Random Solution = ")
#     print(randomSolution)

#     # knapsack.printItems(randomSolution)


# if __name__ == "__main__":
#     main()
