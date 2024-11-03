import math
import random
import matplotlib.pyplot as plt
from src.models.box import Box
from src.models.instance_data import InstanceData
from src.models.order import Order
from src.models.product import Product
from src.models.product_quantity_pair import ProductQuantityPair
from src.modules.organise_boxes.base import BaseOrganiseBoxesModule
from src.modules.organise_boxes.OrganiseBoxesDummyV2 import OrganiseBoxesDummyV2


class OrganiseBoxesSAV(BaseOrganiseBoxesModule):
    def __init__(self, instance_data: InstanceData, max_iter=500, initial_temp=5000, cooling_rate=0.995):
        self.max_iter = max_iter  # Nombre d'itérations
        self.initial_temp = initial_temp  # Température initiale
        self.cooling_rate = cooling_rate  # Facteur de refroidissement
        self.fitness_history = []  # Historique des fitness pour traçage
        self.global_fitness_history = []  # Historique de la fitness globale
        super().__init__(instance_data)

    def run(self) -> list[Box]:
        """Implémente l'algorithme de recuit simulé pour organiser les boîtes."""
        boxes = []
        for order in self.instance_data.orders:
            boxes.extend(self.run_sa_order(order))
        return boxes

    def run_sa_order(self, order: Order) -> list[Box]:
        flat_product_list = ProductQuantityPair.flatten_product_quantity_pairs_list(order.products)
        initial_solution = OrganiseBoxesDummyV2(self.instance_data).organise_order_boxes(order)
        current_position = self.convert_boxes_to_position(initial_solution)

        # Calculer la fitness initiale
        current_fitness = self.fitness(current_position, order, flat_product_list)
        best_position = current_position[:]
        best_fitness = current_fitness
        temperature = self.initial_temp

        # Affichage de la solution initiale
        self.display_initial_solution(initial_solution, best_fitness, best_position)

        for iteration in range(self.max_iter):
            print(f"Iteration {iteration + 1}/{self.max_iter}, Température: {temperature:.2f}, Fitness: {current_fitness:.2f}")

            # Générer une nouvelle solution en faisant une petite perturbation
            new_position = self.generate_random_position_variation(current_position, order.max_number_of_boxes)
            new_fitness = self.fitness(new_position, order, flat_product_list)

            # Calculer la variation de fitness
            delta_fitness = new_fitness - current_fitness

            # Accepter la nouvelle solution si elle est meilleure ou avec une certaine probabilité
            if delta_fitness < 0 or random.random() < math.exp(-delta_fitness / temperature):
                current_position = new_position[:]
                current_fitness = new_fitness

            # Mise à jour de la meilleure solution trouvée
            if current_fitness < best_fitness:
                best_position = current_position[:]
                best_fitness = current_fitness
                print(f"Amélioration de la meilleure fitness: {best_fitness}")

            # Refroidissement de la température
            temperature *= self.cooling_rate

            # Stocker les fitness pour traçage
            self.fitness_history.append(current_fitness)
            self.global_fitness_history.append(best_fitness)

        # Créer la solution finale
        best_boxes = self.convert_position_to_boxes(best_position, order, flat_product_list)

        # Affichage du résultat final
        self.display_final_solution(best_boxes, best_fitness, best_position)

        # Afficher l'évolution des fitness
        self.plot_fitness_history()

        return best_boxes

    def fitness(self, position: list[int], order: Order, flat_product_list: list[Product]) -> float:
        """Calcul de la fitness, basé sur la somme des distances."""
        total_distance = 0.0
        max_weight = self.instance_data.max_weight
        max_volume = self.instance_data.max_volume

        boxes = self.convert_position_to_boxes(position, order, flat_product_list)

        for box in boxes:
            weight_excess = max(0, box.used_weight - max_weight)
            volume_excess = max(0, box.used_volume - max_volume)
            if weight_excess > 0 or volume_excess > 0:
                total_distance += 100 * (10 * weight_excess + volume_excess)
            elif box.product_quantity_pairs:
                product_locations = sorted([p.product.location_id for p in box.product_quantity_pairs])
                total_distance += self.calculate_box_distance(product_locations)

        return total_distance

    def generate_random_position_variation(self, base_position: list[int], max_number_of_boxes: int) -> list[int]:
        """Génère une variation aléatoire en échangeant des produits entre cartons adjacents."""
        if len(base_position) == 1:
            return base_position
        new_position = base_position[:]
        id = random.randint(0, max_number_of_boxes - 1)
        box = new_position[id]

        if box == 1 :
            new_position[id] = 2
        elif box == max_number_of_boxes:
            new_position[id] = max_number_of_boxes - 1
        else:
            new_position[id] += -1 if random.random() < 0.5 else 1

        return new_position


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

    def plot_fitness_history(self):
        """Trace l'évolution des fitness au cours des itérations."""
        plt.figure(figsize=(10, 6))
        plt.plot(self.global_fitness_history, label='Best Global Fitness', color='blue', linewidth=2)
        plt.plot(self.fitness_history, label='Fitness', color='red', linewidth=2)
        plt.title("Evolution of Fitness Over Iterations")
        plt.xlabel("Iteration")
        plt.ylabel("Fitness")
        #plt.ylim(0, 200000)
        plt.legend()
        plt.grid(True)
        plt.show()
