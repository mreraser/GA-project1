#-*- coding:utf8 -*-
import random

POPULATION_SIZE = 10
NUMBER_OF_ELITE_CHROMOSOME = 1
TOURNAMENT_SELECTION_SIZE = 4
MUTATION_RATE = 0.01
TARGET_CHROMOSOME = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

class Chromosome:
	def __init__(self):
		self.genes = []
		self.fitness = 0
		i = 0
		while i < TARGET_CHROMOSOME.__len__():
			if random.random() >= 0.5:
				self.genes.append(1)
			else:
				self.genes.append(0)
			i += 1

	def get_genes(self):
		return self.genes

	def get_fitness(self):
		self.fitness = 0
		for i in range(self.genes.__len__()):
			if self.genes[i] == TARGET_CHROMOSOME[i]:
				self.fitness += 1
		return self.fitness

	def __str__(self):
		return self.genes.__str__()

class Population:
	def __init__(self, size):
		self.chromosome = []
		i = 0
		while i < size:
			self.chromosome.append(Chromosome())
			i += 1

	def get_chromosome(self): return self.chromosome

class GeneticAlgorithm:
	@staticmethod
	def evovle(population):
		return GeneticAlgorithm.mutate_population(GeneticAlgorithm.crossover_population(population))

	@staticmethod
	def crossover_chromosomes(chromosome1, chromosome2):
		crossover_chrom = Chromosome()
		for i in range(TARGET_CHROMOSOME.__len__()):
			if random.random() >= 0.5:
				crossover_chrom.get_genes()[i] = chromosome1.get_genes()[i]
			else:
				crossover_chrom.get_genes()[i] = chromosome2.get_genes()[i]
		return crossover_chrom

	@staticmethod
	def crossover_population(population):
		crossover_pop = Population(0)
		for i in range(NUMBER_OF_ELITE_CHROMOSOME):
			crossover_pop.get_chromosome().append(population.get_chromosome()[i])
		i = NUMBER_OF_ELITE_CHROMOSOME
		while i < POPULATION_SIZE:
			chromosome1 = GeneticAlgorithm.select_tournament(population).get_chromosome()[0]
			chromosome2 = GeneticAlgorithm.select_tournament(population).get_chromosome()[0]
			crossover_pop.get_chromosome().append(GeneticAlgorithm.crossover_chromosomes(chromosome1, chromosome2))
			i += 1
		print("[*] 교차", str(chromosome1), " + ", str(chromosome2))
		return crossover_pop

	def mutate_chromosomes(chromosome):
		for i in range(TARGET_CHROMOSOME.__len__()):
			if random.random() < MUTATION_RATE:
				print("[*] 돌연변이 ", str(chromosome))
				if random.random() < 0.5:
					chromosome.get_genes()[i] = 1
				else:
					chromosome.get_genes()[i] = 0

	@staticmethod
	def mutate_population(population):
		for i in range(NUMBER_OF_ELITE_CHROMOSOME, POPULATION_SIZE):
			GeneticAlgorithm.mutate_chromosomes(population.get_chromosome()[i])

		return population

	@staticmethod
	def select_tournament(population):
		tournament_pop = Population(0)
		i = 0
		while i < TOURNAMENT_SELECTION_SIZE:
			tournament_pop.get_chromosome().append(population.get_chromosome()[random.randrange(0, POPULATION_SIZE)])
			i += 1
		tournament_pop.get_chromosome().sort(key=lambda x: x.get_fitness(), reverse=True)
		return tournament_pop

def print_population(population, generation):
	i = 0
	print("-----------------------------------------------------------")
	print("세대 #", generation, "+ 가장 높은 적합도 : ", population.get_chromosome()[0].get_fitness())
	print("Target 염색체 : ", TARGET_CHROMOSOME)
	print("-----------------------------------------------------------")
	for x in population.get_chromosome():
		print("염색체 #", i, " : ", x, " | 적합도 : ", x.get_fitness())
		i += 1
population = Population(POPULATION_SIZE)
population.get_chromosome().sort(key=lambda x: x.get_fitness(), reverse=True)
print_population(population, 0)

generation = 1
while population.get_chromosome()[0].get_fitness() < TARGET_CHROMOSOME.__len__():
	population = GeneticAlgorithm.evovle(population)
	population.get_chromosome().sort(key=lambda x: x.get_fitness(), reverse=True)
	print_population(population, generation)
	generation += 1
