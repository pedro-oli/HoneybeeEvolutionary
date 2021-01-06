import copy
import math
from random import choice, randint, random, shuffle
from sys import stdin
from queue import PriorityQueue
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import RegularPolygon

# Algorithm's Individuals
population = []

#arquivo = open("plots.txt", "w")

# Hive model:
#               __
#            __/  \__
#         __/  \__/  \__
#      __/  \__/  \__/  \__
#   __/  \__/  \__/  \__/  \__
#  /  \__/  \__/  \__/  \__/  \
#  \__/  \__/  \__/  \__/  \__/
#  /  \__/  \__/  \__/  \__/  \
#  \__/  \__/  \__/  \__/  \__/
#  /  \__/  \__/  \__/  \__/  \
#  \__/  \__/  \__/  \__/  \__/
#  /  \__/  \__/  \__/  \__/  \
#  \__/  \__/  \__/  \__/  \__/
#  /  \__/  \__/  \__/  \__/  \
#  \__/  \__/  \__/  \__/  \__/
#     \__/  \__/  \__/  \__/
#        \__/  \__/  \__/
#           \__/  \__/
#              \__/
#
# Observation: see README for more details
class Hive(object):
    def __init__(self, bees = None):
        if bees is None:
            bees = []
        self.bees = bees
        self.possibleCells = [(-4,4,0), (-3,4,-1), (-2,4,-2), (-1,4,-3), (0,4,-4), (4,-4,0), (3,-4,1), (2,-4,2), (1,-4,3), (0,-4,4),
            (1,3,-4), (0,3,-3), (-1,3,-2), (-2,3,-1), (-3,3,0), (-4,3,1), (-1,-3,4), (0,-3,3), (1,-3,2), (2,-3,1), (3,-3,0), (4,-3,-1), (-4,2,2),
            (-3,2,1), (-2,2,0), (-1,2,-1), (0,2,-2), (1,2,-3), (2,2,-4), (4,-2,-2), (3,-2,-1), (2,-2,0), (1,-2,1), (0,-2,2), (-1,-2,3), (-2,-2,4),
            (4,-1,-3), (3,-1,-2), (2,-1,-1), (1,-1,0), (0,-1,1), (-1,-1,2), (-2,-1,3), (-3,-1,4), (-4,1,3), (-3,1,2), (-2,1,1), (-1,1,0),
            (0,1,-1), (1,1,-2), (2,1,-3), (3,1,-4), (-4,0,4), (-3,0,3), (-2,0,2), (-1,0,1), (0,0,0), (1,0,-1), (2,0,-2), (3,0,-3), (4,0,-4)]
        self.finalbees = []

    def __str__(self):
        string = "[ "
        for bee in self.bees:
            string += str(bee) + ","
        # Removes extra comma and closes bracket:
        string = string[:len(string)-1] + " ]"
        return string

    def getBees(self):
        return self.bees

    def getFinalBees(self):
        return self.finalbees

    def getPossibleCells(self):
        return self.possibleCells

    def getEmptyCells(self):
        return set(self.possibleCells) - set(self.bees)

    # Adds a bee to a hive cell
    def fill(self, x, y, z):
        self.bees.append((x,y,z))

    # Checks if a cell has at least 3 bees around it
    def shouldFill(self, x, y, z):
        counter = 0
        
        # neighbor 1
        bee = (x,y+1,z-1)
        if bee in self.bees:
            counter += 1

        # neighbor 2
        bee = (x,y-1,z+1)
        if bee in self.bees:
            counter += 1

        # neighbor 3
        bee = (x+1,y,z-1)
        if bee in self.bees:
            counter += 1

        # neighbor 4
        bee = (x-1,y,z+1)
        if bee in self.bees:
            counter += 1

        # neighbor 5
        bee = (x-1,y+1,z)
        if bee in self.bees:
            counter += 1

        # neighbor 6
        bee = (x+1,y-1,z)
        if bee in self.bees:
            counter += 1
        
        if counter > 2:
            return True
        return False

    def possibleInHive(self, x, y, z):
        if (x,y,z) in self.getPossibleCells():
            return True
        return False

    def beeIsInHive(self, x, y, z):
        if (x,y,z) in self.getBees():
            return True
        return False

    def getFitness(self):
        howManyInitialBees = len(self.getBees())
        fillCounter = 0

        # Fills as much cells as possible
        while len(self.getEmptyCells()) > 0:
            hasCellsLeftToFill = False
            for cell in self.getEmptyCells():
                x,y,z = cell
                if self.shouldFill(x, y, z):
                    self.fill(x, y, z)
                    fillCounter += 1
                    hasCellsLeftToFill = True
            # If there are no cells left to fill, break
            if not hasCellsLeftToFill:
                break

        # Fitness = final number of bees / initial number of bees
        return len(self.getBees()) / howManyInitialBees
# END of class Hive

def getBestIndividual():
    bestFitness = -1
    bestHive = []
    for hive in population:
        hiveCopy = copy.deepcopy(hive)
        fitness = hiveCopy.getFitness()
        hive.finalbees = hiveCopy.getBees()
        if fitness > bestFitness:
            bestFitness = fitness
            bestHive = hive
    return bestHive

def getWorstIndividual():
    worstFitness = 100000
    worstHive = []
    for hive in population:
        hiveCopy = copy.deepcopy(hive)
        fitness = hiveCopy.getFitness()
        if fitness < worstFitness:
            worstFitness = fitness
            worstHive = hive
    return worstHive

def getAveragePopulationFitness():
    average = 0
    populationsize = len(population)
    for hive in population:
        hiveCopy = copy.deepcopy(hive)
        fitness = hiveCopy.getFitness()
        average = average + fitness
    return average/populationsize

# Draws the best Hive and a scatter plot of best fitness by generation
def drawchart(x,y,average, the_worst_fitness, bestHive, ax):
    plt.figure(1)
    plt.scatter(x,y, s = 10, color = 'red', label="The best")
    plt.scatter(x,average, s = 10, color = 'blue', label="Average")
    plt.scatter(x,the_worst_fitness, s = 10, color = 'green', label="The worst")
    plt.pause(0.0001) 
    plt.show()

    # Draw the best and emptyCells - Adaptation made from reading this question: https://stackoverflow.com/questions/46525981/how-to-plot-x-y-z-coordinates-in-the-shape-of-a-hexagonal-grid
    plt.figure(2)

    # All hexagons
    coord = [[-4,4,0], [-3,4,-1], [-2,4,-2], [-1,4,-3], [0,4,-4], [4,-4,0], [3,-4,1], [2,-4,2], [1,-4,3], [0,-4,4],
            [1,3,-4], [0,3,-3], [-1,3,-2], [-2,3,-1], [-3,3,0], [-4,3,1], [-1,-3,4], [0,-3,3], [1,-3,2], [2,-3,1], [3,-3,0], [4,-3,-1], [-4,2,2],
            [-3,2,1], [-2,2,0], [-1,2,-1], [0,2,-2], [1,2,-3], [2,2,-4], [4,-2,-2], [3,-2,-1], [2,-2,0], [1,-2,1], [0,-2,2], [-1,-2,3], [-2,-2,4],
            [4,-1,-3], [3,-1,-2], [2,-1,-1], [1,-1,0], [0,-1,1], [-1,-1,2], [-2,-1,3], [-3,-1,4], [-4,1,3], [-3,1,2], [-2,1,1], [-1,1,0],
            [0,1,-1], [1,1,-2], [2,1,-3], [3,1,-4], [-4,0,4], [-3,0,3], [-2,0,2], [-1,0,1], [0,0,0], [1,0,-1], [2,0,-2], [3,0,-3], [4,0,-4]]
    # Horizontal cartesian coords
    hcoord = [c[0] for c in coord]
    # Vertical cartersian coords
    vcoord = [2. * np.sin(np.radians(60)) * (c[1] - c[2]) /3. for c in coord]
    ax.set_aspect('equal')

    # Add some coloured hexagons
    for x, y in zip(hcoord, vcoord):
        hex = RegularPolygon(
            (x, y), numVertices = 6, radius = 2./3., 
            orientation = np.radians(30), 
            facecolor = 'white', alpha=1, edgecolor='k'
        )
        ax.add_patch(hex)
    # Also add scatter points in hexagon centres
    ax.scatter(hcoord, vcoord, c = 'white', alpha=0)

    final_bees = bestHive.getFinalBees()
    hcoord3 = [c3[0] for c3 in final_bees]
    vcoord3 = [2. * np.sin(np.radians(60)) * (c3[1] - c3[2]) /3. for c3 in final_bees]
    ax.set_aspect('equal')
    # Add some coloured hexagons - Final bees = orange
    for x, y in zip(hcoord3, vcoord3):
        hex = RegularPolygon((x, y), numVertices=6, radius=2. / 3., 
                         orientation=np.radians(30), 
                         facecolor='orange', alpha=1, edgecolor='k')
        ax.add_patch(hex)
    # Also add scatter points in hexagon centres
    ax.scatter(hcoord3, vcoord3, c = 'orange', alpha=0)

    # Draws the best
    the_best_cromossom = bestHive.getBees()
    hcoord2 = [c2[0] for c2 in the_best_cromossom]
    vcoord2 = [2. * np.sin(np.radians(60)) * (c2[1] - c2[2]) /3. for c2 in the_best_cromossom]
    ax.set_aspect('equal')
    # Add some coloured hexagons - Initial bees = red
    for x, y in zip(hcoord2, vcoord2):
        hex = RegularPolygon((x, y), numVertices=6, radius=2. / 3., 
                         orientation=np.radians(30), 
                         facecolor='red', alpha=1, edgecolor='k')
        ax.add_patch(hex)
    # Also add scatter points in hexagon centres
    ax.scatter(hcoord2, vcoord2, c = 'red', alpha=0)
    plt.pause(0.0001) 
    plt.show()

# Crosses best Individual with all others
def elitism(bestHive):
    global population
    nextGeneration = []
    for hive in population:
        if hive is bestHive:
            continue
        bestBees = bestHive.getBees()
        currentHiveBees = hive.getBees()

        # Calculates average number of Bees from parent Hives
        numberOfBeesInChild = (len(currentHiveBees) + len(bestBees)) // 2

        # Copies the bestHive bees (so it doesn't alter it)
        bestBeesCopy = copy.deepcopy(bestBees)

        # Shuffles the best bees before crossing hives
        shuffle(bestBeesCopy)
        newBees = []
        while True:
            if len(newBees) >= numberOfBeesInChild:
                break
            try:
                newBees.append(bestBeesCopy.pop(0))
                auxiliar = currentHiveBees.pop(0)
                # Checks if it isn't duplicated
                if not auxiliar in newBees:
                    newBees.append(auxiliar)
            except IndexError:
                break

        # Shuffles the new Hive bees
        shuffle(newBees)
        # Creates new Hive (child)
        newHive = Hive(newBees)
        # Adds new Hive to next Generation
        nextGeneration.append(newHive)

    # Adds best Hive to next Generation
    nextGeneration.append(bestHive)
    
    population = nextGeneration

# Mutates population (except for the best Hive)
def mutate(bestHive, mutationProbability):
    global population

    # Fiz uma mutacao so para testar o funcionamento do algoritmo. Ela eh dividida em duas partes
    # A primeira parte da mutacao ocorre em toda geracao: todo individuo da populacao (menos o melhor de todos) tem um de seus genes trocado por um aleatorio.
    # A segunda parte da mutacao ocorre de forma aleatoria (depende do valor do mutationProbability): caso essa parte da mutacao ocorra ...
    # ... eh sorteado um numero entre 0 e a menor quantidade de abelhas  de um individuo da populacao. Esse valor sorteado sera a quantidade ...
    # ... de genes de cada um dos individuos da populacao (menos do melhor de todos) que serao trocados por valores aleatorios (por exemplo, ...
    # ... caso o valor sorteado seja 4, todos os individuos da populacao terao, cada um,  4 genes alterados para valores aleatorios)

    #Primeira parte da mutacao
    for hive in population:
        if hive is bestHive:
            continue
        currentHiveBees = hive.getBees()

        removeindex = randint(0, len(currentHiveBees)-1) #sorteia um gene para ser excluido

        currentHiveBees.pop(removeindex) #remove o gene

        #Sorteia um novo gene 

        newX = randint(-4, 4)
        newY = randint(-4, 4)
        newZ = randint(-4, 4)

        new_insertion = 1
        while new_insertion:
            if hive.possibleInHive(newX, newY, newZ) and not hive.beeIsInHive(newX, newY, newZ): #garante de que nao tenha genes repetidos
                new_insertion = 0
            else:
                newX = randint(-4, 4)
                newY = randint(-4, 4)
                newZ = randint(-4, 4)

        hive.bees.append((newX, newY, newZ)) #Adiciona o novo gene na lista de genes


    #Segunda parte da mutacao
    if(mutationProbability>random()):
        lowercromossomsize = 100000000000 
        print("Segunda parte da mutaçao - Probabilidade de ", mutationProbability)

        for hive in population: #calcula qual a menor quantidade de genes de um individuo da populacao
            if(len(hive.getBees()) < lowercromossomsize): 
                lowercromossomsize = len(hive.getBees()) 
        
        changebees = randint(0, lowercromossomsize -1) #sorteia qual a quantidade de genes que serao alterados de cada individuo

        for hive in population:
            if hive is bestHive:
                 continue
            currentHiveBees = hive.getBees()
            counter = changebees #Faz a contagem de quantos genes faltam ser alterados

            while counter: 

                counter = counter - 1
                removeindex = randint(0, len(currentHiveBees)-1) #Sorteia um gene para ser excluido

                currentHiveBees.pop(removeindex) #Exclui o gene

                #Sorteia um novo gene
                newX = randint(-4, 4)
                newY = randint(-4, 4)
                newZ = randint(-4, 4)
                new_insertion = 1
                while new_insertion:
                    if hive.possibleInHive(newX, newY, newZ) and not hive.beeIsInHive(newX, newY, newZ): #Garante que a posicao sorteada exista e que ela ja nao esteja na lista de genes
                        new_insertion = 0
                    else:
                        newX = randint(-4, 4)
                        newY = randint(-4, 4)
                        newZ = randint(-4, 4)

                currentHiveBees.append((newX, newY, newZ))

def genocide(bestHive):
    global population

    print("DEBUG: GENOCIDIO")
    counter = len(population)-1
    new_population = []

    while counter:
        counter = counter - 1
        newHive = Hive()
        # Randomizes the number of Bees in this Hive
        numberOfBees = randint(1, 30)
        for _ in range(numberOfBees):
            newX = randint(-4, 4)
            newY = randint(-4, 4)
            newZ = randint(-4, 4)

            new_insertion = 1
            while new_insertion:
                if newHive.possibleInHive(newX, newY, newZ) and not newHive.beeIsInHive(newX, newY, newZ): #Garante que a posicao exista e evita a insercao de genes repetidos
                    new_insertion = 0
                else:
                     newX = randint(-4, 4)
                     newY = randint(-4, 4)
                     newZ = randint(-4, 4)
            
            # Adds new Bee to Hive
            newHive.bees.append((newX, newY, newZ))
        # Adds new Hive to the algorithm's Population
        new_population.append(newHive)

    new_population.append(bestHive)
    population = new_population

def randomPredation(worstHive): #Troca o pior individuo por um aleatorio
    global population

    print("PREDACAO RANDOMICA")
    population.remove(worstHive) #Exclui o pior individuo

    newHive = Hive() #Cria um novo individuo

    numberOfBees = randint(1, 30) #Sorteia a quantidade de genes do individuo

    for _ in range(numberOfBees):
        newX = randint(-4, 4)
        newY = randint(-4, 4)
        newZ = randint(-4, 4)
        new_insertion = 1
        while new_insertion:
            if newHive.possibleInHive(newX, newY, newZ) and not newHive.beeIsInHive(newX, newY, newZ): #Garante que a posicao exista e evita a insercao de genes repetidos
                new_insertion = 0
            else:
                newX = randint(-4, 4)
                newY = randint(-4, 4)
                newZ = randint(-4, 4)
            
        # Adds new Bee to Hive
        newHive.bees.append((newX, newY, newZ))
        # Adds new Hive to the algorithm's Population
  
    population.append(newHive)
    
# Changes the worst individual for the average of the rest:
def sintesePredation(worstHive):
    global population

    # print("DEBUG: PREDACAO POR SINTESE")
    sum_cromossom_size = 0
    for hive in population:
        sum_cromossom_size = sum_cromossom_size + len(hive.getBees())

    newHive_number_genes = sum_cromossom_size // len(population)
    all_genes_on_population = []
    for hive in population:
        for (x,y,z) in hive.getBees():
            all_genes_on_population.append((x,y,z))
    population.remove(worstHive)
    newHive = Hive()
    for _ in range(newHive_number_genes):
        new_insertion = 1
        while new_insertion:
            index = randint(0, len(all_genes_on_population) - 1)
            (newX, newY, newZ) = all_genes_on_population.pop(index)
            # Checks if it's not duplicated
            if not newHive.beeIsInHive(newX, newY, newZ):
                new_insertion = 0
                newHive.bees.append((newX, newY, newZ))
    population.append(newHive) 

def main(mutationProbability2, numberOfHives2, genocide_interval2, random_predation_interval2):

    global population

    population = []

    mutationProbability = mutationProbability2 	# Probability that ANY mutation happens
    numberOfHives = numberOfHives2  		    # Number of Hives per Individual
    genocide_interval = genocide_interval2          # Minimum number of generations before running genocide
    random_predation_interval = random_predation_interval2 

    print("QUANTIDADE DE INDIVIDUOS " + str(numberOfHives))

    generation = 0		    		# Generation counter
    # Generates initial Individuals (population)
    for _ in range(numberOfHives):
        newHive = Hive()
        # Randomizes the number of Bees in this Hive
        numberOfBees = randint(1, 30)
        for _ in range(numberOfBees):
            newX = randint(-4, 4)
            newY = randint(-4, 4)
            newZ = randint(-4, 4)

            new_insertion = 1
            while new_insertion:
                # Checks if position generated is possible and if it isn't duplicated
                if newHive.possibleInHive(newX, newY, newZ) and not newHive.beeIsInHive(newX, newY, newZ):
                    new_insertion = 0
                else:
                    newX = randint(-4, 4)
                    newY = randint(-4, 4)
                    newZ = randint(-4, 4)

            # Adds new Bee to Hive
            newHive.bees.append((newX, newY, newZ))
        # Adds new Hive to the algorithm's Population
        population.append(newHive)

    # Print initial population
    #print("Population:")
    #for index, hive in enumerate(population):
        #print("\tHive", index, "=", hive)

    # Initializes the chart
   # plt.ion() 
  #  fig = plt.figure(1)
   # plt.axis([-0.5,100,-1,6])
   # plt.xlabel("Generation")
   # plt.ylabel("Fitness")
   # plt.scatter(-1000,-1000, s = 10, color = 'red', label = "The best")
   # plt.scatter(-1000,-1000, s = 10, color = 'blue', label = "Average")
   # plt.scatter(-1000,-1000, s = 10, color = 'green', label = "The worst") 


    #arquivo.write('Generation The_best Average The_worst\n')
 
   # plt.legend()
   # fig2, (ax) = plt.subplots(ncols=1, figsize=(5,5))
   # ax.set_title("The best")

    # List with the best fitness
    the_best_fitness_list = []

    change_mutation = 0 # Aux counter for changing the mutation probability
    genocide_counter = 0 # Aux counter for running a new genocide
    random_predation_counter = 0 # Aux counter for running a new random predation

    # Main Loop
    print("Type 'n' for next generation, 'a' to automatic solve problem, or 'q' to quit:")
    command = "a"
    while command != "q":
        #command = input()

        # Manual Loop
        if command == "n":
            # Gets best and the worst Individual
            bestHive = getBestIndividual()
            worstHive = getWorstIndividual()

            # Draws a chart of Best fitnesses x generation
            the_best_fitness = copy.deepcopy(bestHive).getFitness()
            the_worst_fitness = copy.deepcopy(worstHive).getFitness()

            the_best_fitness_list.append(the_best_fitness)
            #drawchart(generation, the_best_fitness, getAveragePopulationFitness(), the_worst_fitness,  copy.deepcopy(bestHive))

            # If reached the random predation interval, runs random predation
            if(random_predation_counter > random_predation_interval):
                randomPredation(worstHive)
                random_predation_counter = 0
            # If not, runs the synthesis predation
            else:
                sintesePredation(worstHive)

            # Crosses best Hive with all others (Elitism)
            elitism(bestHive)

            # If reached the genocide interval AND the best fitness hasn't improved in the last 20 generations,
            # runs a genocide
            if(genocide_counter > genocide_interval and (len(the_best_fitness_list)-21)>0 and the_best_fitness_list[len(the_best_fitness_list)-1] == the_best_fitness_list[len(the_best_fitness_list)-21]):
                    genocide(bestHive)
                    change_mutation = 0
                    genocide_counter = 0
                    mutationProbability = 0.005

            # If the mutation probability hasn't changed for 5 generations
            # AND the best fitness hasn't improved, doubles the mutationProbability
            if(change_mutation > 5  and (len(the_best_fitness_list)-11)>0 and the_best_fitness_list[len(the_best_fitness_list)-1] == the_best_fitness_list[len(the_best_fitness_list)-11]):
                mutationProbability = mutationProbability * 2
                # Checks if the probability is more than 100%, and sets it to 100%
                if(mutationProbability > 1):
                    mutationProbability = 1
                change_mutation = 0

            # Mutates population (except for the best Hive)
            mutate(bestHive, mutationProbability)

            # Increments counters
            generation += 1
            change_mutation += 1
            genocide_counter += 1
            random_predation_counter += 1

        # Automatic Loop
        elif command == "a":
            unsolved = True
            while unsolved:
                # If the best fitness stays the same for 50 generations, end program
                if (generation > 50 and the_best_fitness_list[len(the_best_fitness_list)-1] == the_best_fitness_list[len(the_best_fitness_list)-51]):
                    unsolved = False
                    # print("DEBUG: FIM DO PROCESSO")

                # Gets best and the worst Individual
                bestHive = getBestIndividual()
                worstHive = getWorstIndividual()

                # Draws a chart of Best fitnesses x generation
                the_best_fitness = copy.deepcopy(bestHive).getFitness()
                the_worst_fitness = copy.deepcopy(worstHive).getFitness()

                the_best_fitness_list.append(the_best_fitness)
                #drawchart(generation, the_best_fitness, getAveragePopulationFitness(), the_worst_fitness,  copy.deepcopy(bestHive), ax)

                print(generation)
                #arquivo.write(str(generation)+" "+ str(the_best_fitness)+" "+str(getAveragePopulationFitness())+" "+str(the_worst_fitness)+"\n")


                # If reached the random predation interval, runs random predation
                if(random_predation_counter > random_predation_interval):
                    randomPredation(worstHive)
                    random_predation_counter = 0
                # If not, runs the synthesis predation
                else:
                    sintesePredation(worstHive)

                # Crosses best Hive with all others (Elitism)
                elitism(bestHive)

                # If reached the genocide interval AND the best fitness hasn't improved in the last 20 generations,
                # runs a genocide
                if(genocide_counter > genocide_interval and (len(the_best_fitness_list)-21)>0  and  the_best_fitness_list[len(the_best_fitness_list)-1] == the_best_fitness_list[len(the_best_fitness_list)-21]):
                    genocide(bestHive)
                    change_mutation = 0
                    genocide_counter = 0
                    mutationProbability = mutationProbability2

                # If the mutation probability hasn't changed for 5 generations
                # AND the best fitness hasn't improved, doubles the mutationProbability
                if(change_mutation>5 and (len(the_best_fitness_list)-11)>0 and the_best_fitness_list[len(the_best_fitness_list)-1] == the_best_fitness_list[len(the_best_fitness_list)-11]):
                    mutationProbability = mutationProbability * 2
                    # Checks if the probability is more than 100%, and sets it to 100%
                    if(mutationProbability > 1):
                        mutationProbability = 1
                    change_mutation = 0

                # Mutates population (except for the best Hive)
                mutate(bestHive, mutationProbability)

                # Increments counters
                generation += 1
                change_mutation +=1
                genocide_counter += 1
                random_predation_counter += 1

            break
    # END of while command != "q"

    #arquivo.close()

    print("TAMANHO DA POPULAÇÃO AO FINAL " + str(len(population)))

    population = []

    return the_best_fitness

