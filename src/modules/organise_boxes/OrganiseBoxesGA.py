import random
import matplotlib.pyplot as plt
from src.models.box import Box
from src.models.instance_data import InstanceData
from src.models.order import Order
from src.models.product import Product
from src.models.product_quantity_pair import ProductQuantityPair
from src.modules.organise_boxes.OrganiseBoxesDummyV2 import OrganiseBoxesDummyV2
from src.modules.organise_boxes.base import BaseOrganiseBoxesModule

class OrganiseBoxesGA(BaseOrganiseBoxesModule):
    def __init__(self, instance_data: InstanceData, population_size=20, generations=20, crossover_rate=0.8):
        self.population_size = population_size  # Taille de la population
        self.generations = generations  # Nombre de générations
        self.crossover_rate = crossover_rate  # Taux de croisement
        self.fitness_history = []  # Historique des fitness pour traçage
        super().__init__(instance_data)

    def run(self) -> list[Box]:
        """Exécute l'algorithme génétique pour organiser les boîtes."""
        boxes = []
        for order in self.instance_data.orders:
            boxes.extend(self.run_ga_order(order))
        return boxes

    def run_ga_order(self, order: Order) -> list[Box]:
        flat_product_list = ProductQuantityPair.flatten_product_quantity_pairs_list(order.products)

        # Étape 1: Initialisation de la population
        initial_solution = OrganiseBoxesDummyV2(self.instance_data).organise_order_boxes(order)
        initial_positions = self.convert_boxes_to_position(initial_solution)
        population = [initial_positions[:]]

        population.extend(self.initialize_solutions(order, initial_positions))
        fitness_scores = [self.fitness(individual, order, flat_product_list) for individual in population]

        # Historique de la meilleure solution
        best_individual = population[fitness_scores.index(min(fitness_scores))][:]
        best_fitness = min(fitness_scores)

        for generation in range(self.generations):
            print(f"Génération {generation + 1}/{self.generations}, Best Fitness: {best_fitness:.2f}")

            # Sélection des 4 meilleurs parents uniquement
            best_parents_indices = sorted(range(len(fitness_scores)), key=lambda x: fitness_scores[x])[:4]
            best_parents = [population[i] for i in best_parents_indices]

            new_population = []

            # Étape 3: Reproduction sexuée (croisement sans mutation pour 4 enfants)
            for i in range(0, len(best_parents), 2):
                parent1 = best_parents[i]
                parent2 = best_parents[i + 1]
                child1, child2 = self.crossover(parent1, parent2)
                new_population.extend([child1, child2])

            # Étape 4: Remplir la population par des enfants issus de reproduction assexuée
            while len(new_population) < self.population_size:
                parent = random.choice(best_parents)
                new_individual = self.mutate(parent, order)  # Taux de mutation plus élevé
                new_population.append(new_individual)

            # S'assurer que la taille de la population reste correcte
            new_population = new_population[:self.population_size]

            # Sélection aléatoire de 4 individus à remplacer dans la nouvelle population
            random_indices = random.sample(range(len(new_population)), 4)

            # Remplacement de ces individus par les 4 meilleurs de la génération précédente
            for i, index in enumerate(random_indices):
                new_population[index] = best_parents[i]

            # Mise à jour de la population et recalcul des fitness
            population = new_population
            fitness_scores = [self.fitness(individual, order, flat_product_list) for individual in population]

            # Mise à jour de la meilleure solution
            best_in_generation = min(population, key=lambda x: self.fitness(x, order, flat_product_list))
            best_fitness_in_generation = min(fitness_scores)
            if best_fitness_in_generation < best_fitness:
                best_fitness = best_fitness_in_generation
                best_individual = best_in_generation

            # Stocker la meilleure fitness pour traçage
            self.fitness_history.append(best_fitness)

            # Affichage des 10 meilleures solutions de chaque génération
            best_individuals = sorted(population, key=lambda x: self.fitness(x, order, flat_product_list))[:10]
            self.plot_best_individuals(generation, best_individuals, order, flat_product_list)


        # Affichage de la solution finale
        best_boxes = self.convert_position_to_boxes(best_individual, order, flat_product_list)
        self.display_final_solution(best_boxes, best_fitness, best_individual)
        self.plot_fitness_history()

        return best_boxes

    def initialize_solutions(self, order: Order, initial_positions: list[int]) -> list[list[int]]:
        """Initialise les particules avec une solution initiale et des variations aléatoires."""
        half = (self.population_size - 1) // 2  # -1 pour tenir compte de la première particule initiale

        solutions = []

        for i in range(half):
            random_positions = self.generate_balanced_positions(order)
            solutions.append(random_positions)

        # Générer l'autre moitié avec des variations proches de la solution initiale
        for i in range(self.population_size - half - 1):
            random_positions = self.mutate(initial_positions, order)
            solutions.append(random_positions)

        return solutions

    def generate_balanced_positions(self, order: Order) -> list[int]:
        """Génère une position équilibrée où chaque carton reçoit un nombre similaire de produits."""
        num_products = order.number_of_products
        num_boxes = order.max_number_of_boxes

        # Initialiser la répartition des produits
        balanced_positions = []

        last_seen_box = 0
        # Distribuer les produits de manière équilibrée dans les cartons
        for i in range(num_products):
            # Assigner un carton de manière à ce que les produits soient distribués équitablement
            box_id = random.randint(1, num_boxes)
            if box_id > last_seen_box + 1 :
                box_id = last_seen_box + 1
                last_seen_box = box_id
            balanced_positions.append(box_id)

        return balanced_positions



    def random_solution(self, order: Order, flat_product_list: list[Product]) -> list[int]:
        """Génère une solution aléatoire (position des produits dans les cartons)."""
        return [random.randint(1, order.max_number_of_boxes) for _ in flat_product_list]

    def fitness(self, position: list[int], order: Order, flat_product_list: list[Product]) -> float:
        """Calcule la fitness d'une solution (somme des distances parcourues)."""
        total_distance = 0.0
        max_weight = self.instance_data.max_weight
        max_volume = self.instance_data.max_volume
        boxes = self.convert_position_to_boxes(position, order, flat_product_list)

        for box in boxes:
            weight_excess = max(0, box.used_weight - max_weight)
            volume_excess = max(0, box.used_volume - max_volume)
            if weight_excess > 0 or volume_excess > 0:
                total_distance += 10000 * (10 * weight_excess + volume_excess)
            elif box.product_quantity_pairs:
                product_locations = sorted([p.product.location_id for p in box.product_quantity_pairs])
                total_distance += self.calculate_box_distance(product_locations)

        return total_distance

    def selection(self, population: list[list[int]], fitness_scores: list[float]) -> list[list[int]]:
        """Sélectionne des parents via une roulette biaisée et optimise en forçant le meilleur individu."""

        # Calcul de la fitness inversée (car une fitness plus basse est meilleure dans ce cas)
        max_fitness = max(fitness_scores)
        scaled_fitness = [max_fitness - score for score in fitness_scores]  # Inverser la fitness

        if max_fitness == 0:
            return population

        # Calcul des probabilités de sélection en fonction de la fitness
        total_fitness = sum(scaled_fitness)
        selection_probs = [fitness / total_fitness for fitness in scaled_fitness]

        # Sélection de n/4 couples sur la roue biaisée
        selected = random.choices(population, weights=selection_probs, k=self.population_size // 2)

        # Optimisation : ajout du meilleur individu si non sélectionné
        best_individual = population[fitness_scores.index(min(fitness_scores))]

        if best_individual not in selected:
            # Remplacer un individu aléatoire par le meilleur
            random_idx = random.randint(0, len(selected) - 1)
            selected[random_idx] = best_individual

        # On duplique les individus sélectionnés pour compléter la nouvelle génération
        return selected * 2  # Retourner une population complète

    def crossover(self, parent1: list[int], parent2: list[int], prob_crossover: float = 0.7) -> tuple[
        list[int], list[int]]:
        """Applique un croisement en deux points avec une probabilité donnée."""
        if random.random() < prob_crossover:
            # Croisement en deux points
            point1, point2 = sorted(random.sample(range(1, len(parent1) - 1), 2))
            child1 = parent1[:point1] + parent2[point1:point2] + parent1[point2:]
            child2 = parent2[:point1] + parent1[point1:point2] + parent2[point2:]
        else:
            # Pas de croisement, les enfants sont copies des parents
            child1, child2 = parent1[:], parent2[:]

        return child1, child2

    def mutate(self, individual: list[int], order: Order, prob_mutation: float = None) -> list[int]:
        """Applique une mutation à un individu avec une probabilité donnée."""
        if prob_mutation is None:
            prob_mutation = 1 / len(individual) # Probabilité de mutation par bit

        mutated_individual = individual[:]

        for i in range(len(individual)):
            if random.random() < prob_mutation:
                # Mutation : on peut inverser un bit ou assigner une valeur au hasard
                # On bouge le produit d'un carton à un autre (adjacent)
                box = mutated_individual[i]
                if box == 1:
                    mutated_individual[i] = 2
                elif box == order.max_number_of_boxes:
                    mutated_individual[i] = order.max_number_of_boxes - 1
                else:
                    mutated_individual[i] = box + random.choice([-1, 1])


        return mutated_individual

    def calculate_box_distance(self, product_locations_ids: list[int]) -> float:
        """Calcul de la distance totale pour une boîte donnée."""
        distance = 0
        for i in range(len(product_locations_ids) - 1):
            start = product_locations_ids[i]
            end = product_locations_ids[i + 1]
            if start == end:
                continue
            path = next(sp.distance for sp in self.instance_data.shortest_paths if
                        sp.start_localisation_id == start and sp.end_localisation_id == end)
            distance += path
        return distance

    def convert_position_to_boxes(self, position: list[int], order: Order, flat_product_list: list[Product]) -> list[Box]:
        """Convertit une position en liste de boîtes."""
        boxes = [Box(order, []) for _ in range(order.max_number_of_boxes)]
        for i_product, box_id in enumerate(position):
            product = flat_product_list[i_product]
            boxes[box_id - 1].add_product(product)
        return boxes

    def convert_boxes_to_position(self, solution_boxes: list[Box]) -> list[int]:
        """Convertit une solution en liste de positions (i.e., quel produit dans quel carton)."""
        position = []
        mapping_product_id_to_box = []
        for i_box, box in enumerate(solution_boxes):
            for pqp in box.product_quantity_pairs:
                mapping_product_id_to_box.extend([(pqp.product.product_id, i_box + 1)] * pqp.quantity)

        mapping_product_id_to_box = sorted(mapping_product_id_to_box, key=lambda x: x[0])
        position = [box_id for _, box_id in mapping_product_id_to_box]
        return position


    def display_initial_solution(self, solution, fitness, position):
        print("Résultat de départ des cartons :")
        print(f"Poids maximal autorisé : {self.instance_data.max_weight}, Volume maximal autorisé : {self.instance_data.max_volume}")
        for i, box in enumerate(solution):
            print(f"Carton {box.id}: poids={box.used_weight}; volume={box.used_volume}")
        print(f"Fitness de départ : {fitness}")
        print("Position de départ : ", position)

    def display_final_solution(self, solution, fitness, position):
        print("Résultat final des cartons :")
        print(f"Poids maximal autorisé : {self.instance_data.max_weight}, Volume maximal autorisé : {self.instance_data.max_volume}")
        for i, box in enumerate(solution):
            print(f"Carton {box.id}: poids={box.used_weight}; volume={box.used_volume}")
        print(f"Fitness finale : {fitness}")
        print("Position finale : ", position)

    def plot_best_individuals(self, generation: int, best_individuals: list[list[int]], order: Order,
                              flat_product_list: list[Product]):
        """Affiche les 3 meilleures solutions de la génération actuelle avec leurs fitness."""
        fitness_values = [self.fitness(ind, order, flat_product_list) for ind in best_individuals]

        # Préparer le graphique
        plt.figure(figsize=(10, 6))

        for i, individual in enumerate(best_individuals):
            plt.plot(individual, label=f'Solution {i + 1} - Fitness: {fitness_values[i]:.2f}')

        plt.title(f'Top 3 Solutions at Generation {generation}')
        plt.xlabel('Index du produit')
        plt.ylabel('Carton attribué')
        plt.legend()
        plt.grid(True)

        # Afficher le graphique
        plt.show()

    def plot_fitness_history(self):
        """Affiche l'évolution des fitness au cours des générations."""
        plt.figure(figsize=(10, 6))
        plt.plot(self.fitness_history, label='Best Fitness', color='blue', linewidth=2)
        plt.title("Evolution of Fitness Over Generations")
        plt.xlabel("Generation")
        plt.ylabel("Fitness")
        plt.legend()
        plt.grid(True)
        plt.show()
