from deap import base
from deap import creator
from deap import tools
from deap import algorithms

import random
import numpy

import matplotlib.pyplot as plt
import seaborn as sns

import GeneticHelper


class Genetic:
    def __init__(self):
        # problem constants:

        # Genetic Algorithm constants:
        self.POPULATION_SIZE = 50
        self.P_CROSSOVER = 0.9  # probability for crossover
        self.P_MUTATION = 0.1   # probability for mutating an individual
        self.MAX_GENERATIONS = 50
        self.HALL_OF_FAME_SIZE = 1

    # Genetic Algorithm flow:

    def fit(self, block_ids, block_wts, block_fee, maxCapacity, plot=False):
        # create the knapsack problem instance to be used:
        knapsack = GeneticHelper.GeneticHelper()
        knapsack.initData(block_ids, block_wts, block_fee, maxCapacity)
        # set the random seed:
        RANDOM_SEED = 42
        random.seed(RANDOM_SEED)

        toolbox = base.Toolbox()

        # create an operator that randomly returns 0 or 1:
        toolbox.register("zeroOrOne", random.randint, 0, 1)

        # define a single objective, maximizing fitness strategy:
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))

        # create the Individual class based on list:
        creator.create("Individual", list, fitness=creator.FitnessMax)

        # create the individual operator to fill up an Individual instance:
        toolbox.register("individualCreator", tools.initRepeat,
                         creator.Individual, toolbox.zeroOrOne, len(knapsack))

        # create the population operator to generate a list of individuals:
        toolbox.register("populationCreator", tools.initRepeat,
                         list, toolbox.individualCreator)

        # fitness calculation

        def knapsackValue(individual):
            return knapsack.getValue(individual),  # return a tuple

        toolbox.register("evaluate", knapsackValue)

        # genetic operators:mutFlipBit

        # Tournament selection with tournament size of 3:
        toolbox.register("select", tools.selTournament, tournsize=3)

        # Single-point crossover:
        toolbox.register("mate", tools.cxTwoPoint)

        # Flip-bit mutation:
        # indpb: Independent probability for each attribute to be flipped
        toolbox.register("mutate", tools.mutFlipBit, indpb=1.0/len(knapsack))

        # create initial population (generation 0):
        population = toolbox.populationCreator(n=self.POPULATION_SIZE)

        # prepare the statistics object:
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("max", numpy.max)
        stats.register("avg", numpy.mean)

        # define the hall-of-fame object:
        hof = tools.HallOfFame(self.HALL_OF_FAME_SIZE)

        # perform the Genetic Algorithm flow with hof feature added:
        population, logbook = algorithms.eaSimple(population, toolbox, cxpb=self.P_CROSSOVER, mutpb=self.P_MUTATION,
                                                  ngen=self.MAX_GENERATIONS, stats=stats, halloffame=hof, verbose=True)

        # print best solution found:
        best = hof.items[0]
        # print("-- Best Ever Individual = ", best)
        print("-- Best Ever Fitness = ", best.fitness.values[0])

        # print("-- Knapsack Items = ")
        # self.knapsack.printItems(best)

        # plot statistics:
        if plot == True:
            # extract statistics:
            maxFitnessValues, meanFitnessValues = logbook.select("max", "avg")
            sns.set_style("whitegrid")
            plt.plot(maxFitnessValues, color='red')
            plt.plot(meanFitnessValues, color='green')
            plt.xlabel('Generation')
            plt.ylabel('Max / Average Fitness')
            plt.title('Max and Average fitness over Generations')
            plt.show()

        return best
