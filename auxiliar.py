from principal import main
from random import choice, randint, random, shuffle, uniform
import math

population = []

arquivo = open("segundo_ag.txt", "w")
arquivo2 = open("parametros.txt", "w")


class HoneybeePopulation(object):
    def __init__(self, mutationProbability, numberOfHives, genocide_interval, random_predation_interval):
        self.mutationProbability = mutationProbability
        self.numberOfHives = numberOfHives
        self.genocide_interval = genocide_interval
        self.random_predation_interval = random_predation_interval
        self.fitness = []

    def setFitness(self):
        the_best_fitness = main(self.mutationProbability, self.numberOfHives, self.genocide_interval, self.random_predation_interval)
        self.fitness = the_best_fitness
        return the_best_fitness

    def setParameters(self, mutationProbability, numberOfHives, genocide_interval, random_predation_interval):
        self.mutationProbability = mutationProbability
        self.numberOfHives = numberOfHives
        self.genocide_interval = genocide_interval
        self.random_predation_interval = random_predation_interval

    def getFitness(self):
        return self.fitness

    def getParameters_mutationProbability(self):
        return  self.mutationProbability

    def getParameters_numberOfHives(self):
        return self.numberOfHives

    def getParameters_genocide_interval(self):
        return  self.genocide_interval

    def getParameters_random_predation_interval(self):
        return  self.random_predation_interval    
    
    def getParameters(self):
        return  self.mutationProbability, self.numberOfHives, self.genocide_interval, self.random_predation_interval  

########################################

def getBestIndividual(bestPopulationHive, generation): #Calcula o fitness de toda a populacao e retorna o melhor de todos

    if(generation == 0): # Caso seja a primeira iteracao
        bestFitness = -1
        bestpopHive = []
        for pop_hive in population:
            fitness = pop_hive.setFitness()
            if fitness > bestFitness:
                bestFitness = fitness
                bestpopHive = pop_hive
        return bestpopHive

    if(generation != 0): #Caso contrario, para garantir que o fitness do melhor nao mude
        bestFitness = -1
        bestpopHive = []
        for pop_hive in population:
            if pop_hive is bestPopulationHive:
                continue
            fitness = pop_hive.setFitness()
            if fitness > bestFitness:
                bestFitness = fitness
                bestpopHive = pop_hive

        if(bestPopulationHive.getFitness() > bestFitness):
            return bestPopulationHive
        else: 
            return bestpopHive

############################################

def getWorstIndividual(): #Retorna o individuo com menor fitness
    worstFitness = 100000
    worstHive_pop = []
    for hive_pop in population:
        fitness = hive_pop.getFitness()
        if fitness < worstFitness:
            worstFitness = fitness
            worstHive_pop = hive_pop
    return worstHive_pop

#######################################

def getAveragePopulationFitness(): #Retorna o fitness medio da populacao
    average = 0
    populationsize = len(population)
    for hive_pop in population:
        fitness = hive_pop.getFitness()
        average = average + fitness
    return average/populationsize

#########################################

def randomPredation(worstHivepop): #Troca o pior individuo por um aleatorio
    global population

    print("PREDACAO RANDOMICA")
    population.remove(worstHivepop) #Exclui o pior individuo

    gene_mutationProbability = randint(1, 500) / 10000 #Sorteia os genes do algoritmo original
    gene_numberOfHives = randint(2, 50)
    gene_genocide_interval = randint(1, 30)
    gene_random_predation_interval =  randint(1, 20)

    newPopulation = HoneybeePopulation(gene_mutationProbability, gene_numberOfHives, gene_genocide_interval, gene_random_predation_interval)

    population.append(newPopulation)

###########################################

def sintesePredation(worstHivepop): #Troca o pior individuo pela media dos demais
    global population

    population.remove(worstHivepop) #Exclui o pior individuo

    sum_gene_1 = 0 #Auxiliares
    sum_gene_2 = 0
    sum_gene_3 = 0
    sum_gene_4 = 0

    for hivepop in population:

        gene_1, gene_2, gene_3, gene_4 = hivepop.getParameters()

        sum_gene_1 = sum_gene_1 + gene_1 
        sum_gene_2 = sum_gene_2 + gene_2
        sum_gene_3 = sum_gene_3 + gene_3
        sum_gene_4 = sum_gene_4 + gene_4

    #Cria um novo individuo com base na media dos genes
    newPopulation = HoneybeePopulation(sum_gene_1/len(population), sum_gene_2//len(population), sum_gene_3//len(population), sum_gene_4//len(population))

    population.append(newPopulation)

##################################

# Crosses best Individual with all others
def elitism(bestHivepop):
    global population
    nextGeneration = []

    best_gene_1, best_gene_2, best_gene_3, best_gene_4 = bestHivepop.getParameters() #Genes do melhor individuo

    for hivepop in population:
        if hivepop is bestHivepop:
            continue

        gene_1, gene_2, gene_3, gene_4 = hivepop.getParameters()
      
        #Cria um novo individuo com base na media dos genes com o melhor de todos
        newHivepop = HoneybeePopulation((gene_1 + best_gene_1)/2, (gene_2 + best_gene_2)//2, (gene_3 + best_gene_3)//2, (gene_4 + best_gene_4)//2)
        
        nextGeneration.append(newHivepop)

    # Adds best Hive to next Generation
    nextGeneration.append(bestHivepop)
    population = nextGeneration

####################################

def mutation(bestHivepop, mutation_rate): # Realiza  a mutacao

    global population
   
    for hivepop in population:
        if hivepop is bestHivepop:
            continue

        change_gene = randint(1, 4) #Escolhe um gene para sofrer mutacao
        mutation_value = choice([-1*mutation_rate, mutation_rate]) #Valor de mutacao (pode ser positivo ou negativo)

        gene_1, gene_2, gene_3, gene_4 = hivepop.getParameters()

        if(change_gene == 1):
            hivepop.setParameters(gene_1 + mutation_value * 0.05 , gene_2, gene_3, gene_4) # Considerando que o eixo da mutacao vai ate 0.05

        if(change_gene == 2):
            hivepop.setParameters(gene_1 , math.ceil(gene_2 + mutation_value * 50) , gene_3, gene_4) # Considerando que o eixo do numberOfHives vai até 50

        if(change_gene == 3):
            hivepop.setParameters(gene_1  , gene_2, math.ceil(gene_3 + mutation_value * 30), gene_4) # Considerando que o eixo do intervalo de genocidio vai até 30

        if(change_gene == 4):
            hivepop.setParameters(gene_1  , gene_2, gene_3, math.ceil(gene_4 + mutation_value * 20)) # Considerando que o eixo do intervalo de predacao randomica vai até 20

########################################

def genocide(bestHivepop):
    global population

    print("DEBUG: GENOCIDIO")
    counter = len(population)-1
    new_population = []

    while counter:
        counter = counter - 1

        gene_mutationProbability = randint(1, 500) / 10000 #Sorteia os genes do algoritmo original
        gene_numberOfHives = randint(1, 50)
        gene_genocide_interval = randint(1, 30)
        gene_random_predation_interval =  randint(1, 20)

        newPopulationHive = HoneybeePopulation(gene_mutationProbability, gene_numberOfHives, gene_genocide_interval, gene_random_predation_interval)

        new_population.append(newPopulationHive)

    new_population.append(bestHivepop)
    population = new_population

#########################################

if __name__ == '__main__':

    numberofPopulation = 5 #Tamanho da populacao
    generation = 0
    mutation_rate = 0.05 #Taxa de mutacao para esse algoritmo
    random_predation_interval = 5 #Intervalo para uma predacao randomica
    genocide_interval = 10 #Intervalo para o genocidio

    for _ in range(numberofPopulation): #Inicia a populacao

        gene_mutationProbability = randint(1, 500) / 10000 #Sorteia os genes do algoritmo original
        gene_numberOfHives = randint(1, 50)
        gene_genocide_interval = randint(1, 30)
        gene_random_predation_interval =  randint(1, 20)

        newPopulation = HoneybeePopulation(gene_mutationProbability, gene_numberOfHives, gene_genocide_interval, gene_random_predation_interval)

        print("PARAMETROS:    " + str(newPopulation.getParameters()))
        population.append(newPopulation) 


    arquivo.write('Generation The_best Average The_worst\n')
    arquivo2.write('Generation Mutation numberofHives genocide_interval random_predation_interval\n')

    bestPopulationHive = []

     # List with the best fitness
    the_best_fitness_list = []

    genocide_counter = 0 # Aux counter for running a new genocide
    random_predation_counter = 0 # Aux counter for running a new random predation

    while True:

        aux = bestPopulationHive

        bestPopulationHive = getBestIndividual(aux, generation) #Retorna o melhor e o pior individuo
        worstPopulationHive = getWorstIndividual()

        #Salva em arquivo
        arquivo.write(str(generation)+" "+ str(bestPopulationHive.getFitness())+" "+str(getAveragePopulationFitness())+" "+str(worstPopulationHive.getFitness())+"\n")
        arquivo2.write(str(generation)+" "+ str(bestPopulationHive.getParameters_mutationProbability())+" "+str(bestPopulationHive.getParameters_numberOfHives())+" "+str(bestPopulationHive.getParameters_genocide_interval())+" "+str(bestPopulationHive.getParameters_random_predation_interval())+"\n")

        print("Geracao : " + str(generation))
        print("Parametros : " + str(bestPopulationHive.getParameters()))
        print("Fitness : " + str(bestPopulationHive.getFitness()))


        the_best_fitness_list.append(bestPopulationHive.getFitness())

        # If reached the random predation interval, runs random predation
        if(random_predation_counter > random_predation_interval):
            randomPredation(worstPopulationHive)
            random_predation_counter = 0
        # If not, runs the synthesis predation
        else:
            sintesePredation(worstPopulationHive)

        # Crosses bestpopulation Hive with all others (Elitism)
        elitism(bestPopulationHive)

        # If reached the genocide interval AND the best fitness hasn't improved in the last 10 generations,
        # runs a genocide
        if(genocide_counter > genocide_interval  and  the_best_fitness_list[len(the_best_fitness_list)-1] == the_best_fitness_list[len(the_best_fitness_list)-11]):
            genocide(bestPopulationHive)
            genocide_counter = 0


        # Mutates population (except for the best popHive)
        mutation(bestPopulationHive, mutation_rate)

        # Increments counters
        generation = generation + 1
        random_predation_counter += 1
        genocide_counter += 1


        if(generation == 20): #Executa ate a geracao 50
            break


    arquivo.close()
    arquivo2.close()

    




