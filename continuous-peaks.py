# traveling salesman algorithm implementation in jython
# This also prints the index of the points of the shortest route.
# To make a plot of the route, write the points at these indexes
# to a file and plot them in your favorite tool.
# adapted from https://github.com/pushkar/ABAGAIL/blob/master/jython/travelingsalesman.py

import sys
import os
import time

# sys.path.append('C:\\Users\\Katharine\\Code\\ML\\Assignment2\\ABAGAIL\\ABAGAIL.jar')
sys.path.append(os.path.join(sys.path[0], 'ABAGAIL.jar'))
# print(sys.path)

import java.io.FileReader as FileReader
import java.io.File as File
import java.lang.String as String
import java.lang.StringBuffer as StringBuffer
import java.lang.Boolean as Boolean
import java.util.Random as Random

import dist.DiscreteDependencyTree as DiscreteDependencyTree
import dist.DiscreteUniformDistribution as DiscreteUniformDistribution
import dist.Distribution as Distribution
import dist.DiscretePermutationDistribution as DiscretePermutationDistribution
import opt.DiscreteChangeOneNeighbor as DiscreteChangeOneNeighbor
import opt.EvaluationFunction as EvaluationFunction
import opt.GenericHillClimbingProblem as GenericHillClimbingProblem
import opt.HillClimbingProblem as HillClimbingProblem
import opt.NeighborFunction as NeighborFunction
import opt.RandomizedHillClimbing as RandomizedHillClimbing
import opt.SimulatedAnnealing as SimulatedAnnealing
import opt.example.FourPeaksEvaluationFunction as FourPeaksEvaluationFunction
import opt.ga.CrossoverFunction as CrossoverFunction
import opt.ga.SingleCrossOver as SingleCrossOver
import opt.ga.DiscreteChangeOneMutation as DiscreteChangeOneMutation
import opt.ga.GenericGeneticAlgorithmProblem as GenericGeneticAlgorithmProblem
import opt.ga.GeneticAlgorithmProblem as GeneticAlgorithmProblem
import opt.ga.MutationFunction as MutationFunction
import opt.ga.StandardGeneticAlgorithm as StandardGeneticAlgorithm
import opt.ga.UniformCrossOver as UniformCrossOver
import opt.prob.GenericProbabilisticOptimizationProblem as GenericProbabilisticOptimizationProblem
import opt.prob.MIMIC as MIMIC
import opt.prob.ProbabilisticOptimizationProblem as ProbabilisticOptimizationProblem
import shared.FixedIterationTrainer as FixedIterationTrainer
import opt.example.TravelingSalesmanEvaluationFunction as TravelingSalesmanEvaluationFunction
import opt.example.TwoColorsEvaluationFunction as TwoColorsEvaluationFunction
import opt.SwapNeighbor as SwapNeighbor
import opt.ga.SwapMutation as SwapMutation
import opt.example.TravelingSalesmanCrossOver as TravelingSalesmanCrossOver
import opt.example.TravelingSalesmanSortEvaluationFunction as TravelingSalesmanSortEvaluationFunction
import shared.Instance as Instance
import util.ABAGAILArrays as ABAGAILArrays
import opt.example.ContinuousPeaksEvaluationFunction as ContinuousPeaksEvaluationFunction

from array import array

from time import clock
import csv




"""
Commandline parameter(s):
    none
"""

# set N value.  This is the number of points
N = 50
fill = [2] * N
random = Random()
ranges = array('i', fill)
T = 20

points = [[0 for x in xrange(2)] for x in xrange(N)]
for i in range(0, len(points)):
    points[i][0] = random.nextDouble()
    points[i][1] = random.nextDouble()

ef = ContinuousPeaksEvaluationFunction(T)
odd = DiscreteUniformDistribution(ranges)
nf = DiscreteChangeOneNeighbor(ranges)
mf = DiscreteChangeOneMutation(ranges)
cf = SingleCrossOver()
df = DiscreteDependencyTree(.1, ranges)
hcp = GenericHillClimbingProblem(ef, odd, nf)
gap = GenericGeneticAlgorithmProblem(ef, odd, mf, cf)

# repeat a few times to get an average?
trials = 10 # more?

hill_climbing = []
annealing = []
genetic = []
mimic_data = []


hill_climbing_output = "peaks_hill_climbing.csv"
annealing_output = "peaks_annealing.csv"
genetic_output = "peaks_genetic.csv"
mimic_output = "peaks_mimic.csv"

# HILL CLIMBING
for i in range(trials):
    rhc = RandomizedHillClimbing(hcp)
    fit = FixedIterationTrainer(rhc, 200000)

    start = clock()
    fit.train()
    end = clock()
    total_time = end - start
    max_fit = ef.value(rhc.getOptimal())
    time_optimum = [total_time, max_fit]
    hill_climbing.append(time_optimum)
    print "RHC Optimum: " + str(ef.value(rhc.getOptimal()))


#
# ANNEALING
for i in range(trials):
    sa = SimulatedAnnealing(1E12, .999, hcp)
    fit = FixedIterationTrainer(sa, 200000)
    start = clock()
    fit.train()
    end = clock()
    total_time = end - start
    max_fit = ef.value(sa.getOptimal())
    time_optimum = [total_time, max_fit]
    annealing.append(time_optimum)
    print("SA Optimum: " + str(ef.value(sa.getOptimal())))




# GENETIC ALGO
for i in range(trials):
    ga = StandardGeneticAlgorithm(2000, 1500, 250, gap)
    fit = FixedIterationTrainer(ga, 1000)
    start = clock()
    fit.train()
    end = clock()
    total_time = end - start
    max_fit = ef.value(ga.getOptimal())
    time_optimum = [total_time, max_fit]
    genetic.append(time_optimum)
    print("GA Optimum: " + str(ef.value(ga.getOptimal())))

# MIMIC
# for mimic we use a sort encoding
for i in range(trials):
    ef = ContinuousPeaksEvaluationFunction(T);
    fill = [N] * N
    ranges = array('i', fill)
    odd = DiscreteUniformDistribution(ranges);
    df = DiscreteDependencyTree(.1, ranges);
    pop = GenericProbabilisticOptimizationProblem(ef, odd, df);

    mimic = MIMIC(500, 100, pop)
    fit = FixedIterationTrainer(mimic, 1000)
    start = clock()
    fit.train()
    end = clock()
    total_time = end - start
    max_fit = ef.value(mimic.getOptimal())
    time_optimum = [total_time, max_fit]
    mimic_data.append(time_optimum)
    print "MIMIC Optimum: " + str(ef.value(mimic.getOptimal()))
#
csv_headers = ['Algorithm', 'Trial 1', 'Trial 2','Trial 3','Trial 4',
               'Trial 5','Trial 6','Trial 7','Trial 8','Trial 9', 'Trial 10']
# rows = [hill_climbing]

with open(hill_climbing_output, 'w') as hc_csv:
    # creating a csv writer object
    csvwriter = csv.writer(hc_csv)

    # writing the data rows
    csvwriter.writerows(hill_climbing)

with open(annealing_output, 'w') as sa_csv:
    # creating a csv writer object
    csvwriter = csv.writer(sa_csv)

    # writing the data rows
    csvwriter.writerows(annealing)

with open(genetic_output, 'w') as ga_csv:
    # creating a csv writer object
    csvwriter = csv.writer(ga_csv)

    # writing the data rows
    csvwriter.writerows(genetic)

with open(mimic_output, 'w') as mimic_csv:
    # creating a csv writer object
    csvwriter = csv.writer(mimic_csv)

    # writing the data rows
    csvwriter.writerows(mimic_data)

