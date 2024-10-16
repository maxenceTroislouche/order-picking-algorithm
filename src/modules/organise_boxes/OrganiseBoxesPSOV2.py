from src.models.box import Box
from src.models.instance_data import InstanceData
from src.models.order import Order
from src.models.product_quantity_pair import ProductQuantityPair
from src.modules.organise_boxes.OrganiseBoxesDummyV2 import OrganiseBoxesDummyV2
from src.modules.organise_boxes.base import BaseOrganiseBoxesModule
from src.models.product import Product
import random


class Particle:
    def __init__(self, order: Order, initial_position: list[int]):
        # Utilisation de la solution initiale fournie par OrganiseOrderBoxes pour la position
        self.position = initial_position[:]  # Position basée sur une première solution intelligente
        self.velocity = [0] * len(initial_position)  # Vitesse initiale à 0
        self.best_position = self.position[:]  # Meilleure position personnelle
        self.best_fitness = float('inf')  # Meilleure fitness personnelle
        self.fitness = float('inf')  # Fitness actuelle
        self.order = order
        self.valid = False  # Indicateur pour marquer les particules invalides


class OrganiseBoxesPSOV2(BaseOrganiseBoxesModule):
    def __init__(self, instance_data: InstanceData, max_iter=100, num_particles=10):
        self.max_iter = max_iter
        self.num_particles = num_particles
        self.omega = 0.5  # Facteur d'inertie
        self.phi_p = 1.5  # Composante cognitive
        self.phi_g = 1.5  # Composante sociale
        super().__init__(instance_data)

    def run(self) -> list[Box]:
        """Implémente l'algorithme PSO pour organiser les boîtes."""
        boxes = []
        for order in self.instance_data.orders:
            boxes.extend(self.run_pso_order(order))
        return boxes

    def run_pso_order(self, order: Order) -> list[Box]:
        # Aplatir la liste des produits pour obtenir une liste de produits individuels
        flat_product_list = ProductQuantityPair.flatten_product_quantity_pairs_list(order.products)

        # Initialiser une première solution basée sur "OrganiseOrderBoxes"
        initial_solution = OrganiseBoxesDummyV2(self.instance_data).organise_order_boxes(order)
        initial_positions = self.convert_boxes_to_position(initial_solution)

        # Initialiser les particules
        particles = self.initialize_particles(order, initial_positions)

        # Initialiser la meilleure position globale
        particles[0].best_position = particles[0].position[:]
        particles[0].best_fitness = self.fitness(particles[0], order, flat_product_list)
        best_global_position = particles[0].best_position[:][:]  # Copie de la meilleure position
        best_global_fitness = particles[0].best_fitness

        # Affichage du résultat initial
        self.display_initial_solution(initial_solution, best_global_fitness, best_global_position)

        # Boucle principale de PSO
        for iteration in range(self.max_iter):
            print(f"Iteration {iteration + 1}/{self.max_iter}")

            # Mise à jour des meilleures solutions
            best_global_position, best_global_fitness = self.update_global_best(particles, best_global_position,
                                                                                best_global_fitness, order,
                                                                                flat_product_list)
            print(f"Meilleure fitness de cette itération : {best_global_fitness}")

            # Mise à jour des vitesses et des positions des particules
            self.update_particle_positions(particles, best_global_position, order)

        # Créer la solution finale
        best_boxes = self.convert_position_to_boxes(best_global_position, order, flat_product_list)

        # Affichage du résultat final
        self.display_final_solution(best_boxes, best_global_fitness, best_global_position)

        return best_boxes

    def fitness(self, particle: Particle, order: Order, flat_product_list: list[Product]) -> float:
        """Calcul de la fitness pour une particule, basé sur la somme des distances."""
        total_distance = float(0.0)
        max_weight = self.instance_data.max_weight
        max_volume = self.instance_data.max_volume

        boxes = self.convert_position_to_boxes(particle.position, order, flat_product_list)
        self.repair_solution(particle, flat_product_list, order, boxes)

        for box in boxes:
            weight_excess = max(0, box.used_weight - max_weight)
            volume_excess = max(0, box.used_volume - max_volume)
            if weight_excess > 0 or volume_excess > 0:
                total_distance += 1000000 * float(10 * weight_excess + volume_excess)
            elif box.product_quantity_pairs:
                product_locations = sorted([p.product.location_id for p in box.product_quantity_pairs])
                total_distance += float(self.calculate_box_distance(product_locations))

        return total_distance

    def initialize_particles(self, order: Order, initial_positions: list[int]) -> list[Particle]:
        """Initialise les particules avec une solution initiale et des variations aléatoires."""
        particles = [Particle(order, initial_positions)]  # Solution initiale basée sur OrganiseBoxesDummyV2
        half_particles = (self.num_particles - 1) // 2  # -1 pour tenir compte de la première particule initiale

        # Générer la moitié des particules de manière aléatoire
        for i in range(half_particles):
            random_positions = [random.randint(1, order.max_number_of_boxes) for _ in range(order.number_of_products)]
            particles.append(Particle(order, random_positions))

        # Générer l'autre moitié avec des variations proches de la solution initiale
        for i in range(self.num_particles - 1 - half_particles):
            random_positions = self.generate_random_position_variation(initial_positions, order.max_number_of_boxes)
            particles.append(Particle(order, random_positions))

        return particles

    def update_global_best(self, particles: list[Particle], best_global_position: list[int], best_global_fitness: float,
                           order: Order, flat_product_list: list[Product]) -> tuple[list[int], float]:
        """Mise à jour de la meilleure position globale et des fitness des particules."""
        for particle in particles:
            particle.fitness = self.fitness(particle, order, flat_product_list)

            # Mise à jour de la meilleure position personnelle
            if particle.valid and particle.fitness < particle.best_fitness:
                particle.best_fitness = particle.fitness
                particle.best_position = particle.position[:]

            # Mise à jour de la meilleure position globale
            if particle.valid and particle.fitness < best_global_fitness:
                best_global_fitness = particle.fitness
                best_global_position = particle.position[:]
                print("--------------------")
                print(f"Amélioration du best fitness : {best_global_fitness}")

        return best_global_position, best_global_fitness

    def update_particle_positions(self, particles: list[Particle], best_global_position: list[int], order: Order):
        """Mise à jour des vitesses et positions des particules selon l'algorithme PSO."""
        for particle in particles:
            for i in range(order.number_of_products):
                r_p = random.random()
                r_g = random.random()
                particle.velocity[i] = (self.omega * particle.velocity[i]
                                        + self.phi_p * r_p * (particle.best_position[i] - particle.position[i])
                                        + self.phi_g * r_g * (best_global_position[i] - particle.position[i]))
                particle.position[i] = int(particle.position[i] + particle.velocity[i])
                particle.position[i] = max(1, min(order.max_number_of_boxes, particle.position[i]))

    def repair_solution(self, particle: Particle, flat_product_list: list[Product], order: Order, boxes: list[Box] = None):
        """Répare une solution pour s'assurer qu'elle respecte les contraintes de poids et de volume."""
        max_weight = self.instance_data.max_weight
        max_volume = self.instance_data.max_volume

        if boxes is None:
            boxes = self.convert_position_to_boxes(particle.position, order, flat_product_list)

        particle.valid = True
        for box in boxes:
            attempt_counter = 0
            max_attempts = len(box.product_quantity_pairs)
            while (box.used_weight > max_weight or box.used_volume > max_volume) and attempt_counter < max_attempts:
                attempt_counter += 1
                lightest_product = min(box.product_quantity_pairs, key=lambda pqp: pqp.product.weight)

                moved = False
                for target_box in boxes:
                    if target_box.id != box.id and target_box.used_weight + lightest_product.product.weight <= max_weight \
                            and target_box.used_volume + lightest_product.product.volume <= max_volume:
                        box.remove_product(lightest_product.product)
                        target_box.add_product(lightest_product.product)
                        moved = True
                        break

                if not moved:
                    particle.valid = False
                    break
            else:
                if not (box.used_weight <= max_weight and box.used_volume <= max_volume):
                    particle.valid = False

        new_position = []
        for idx, product in enumerate(flat_product_list):
            for box_id, box in enumerate(boxes):
                if any(pqp.product.product_id == product.product_id for pqp in box.product_quantity_pairs):
                    new_position.append(box_id + 1)
                    break
        particle.position = new_position

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

    def generate_random_position_variation(self, base_position: list[int], max_number_of_boxes: int) -> list[int]:
        """Génère une variation aléatoire autour d'une position de base."""
        return [random.randint(max(1, base - 2), min(max_number_of_boxes, base + 2)) for base in base_position]

    def calculate_box_distance(self, product_locations_ids: list[int]) -> float:
        """Calculer la distance totale pour une boîte donnée (les produits triés par localisation)."""
        distance = 0
        # Utilise l'ordre des localisations et la fonction de plus court chemin pour calculer la distance
        for i in range(len(product_locations_ids) - 1):
            start = product_locations_ids[i]
            end = product_locations_ids[i + 1]
            if start == end:
                # Ignorer les distances nulles
                continue
            path = next(sp.distance for sp in self.instance_data.shortest_paths if
                        sp.start_localisation_id == start and sp.end_localisation_id == end)
            distance += path
        return distance

    def display_initial_solution(self, solution, fitness, position):
        print("Résultat de départ des cartons :")
        print(f"Poids maximal autorisé : {self.instance_data.max_weight}, Volume maximal autorisé : {self.instance_data.max_volume}")
        for i, box in enumerate(solution):
            print(f"Carton {box.id}: poids={str(box.used_weight)}; volume={str(box.used_volume)} ")
        print(f"Fitness de départ : ", fitness)
        # affichage de la position finale
        print("Position de départ : ", position)

    def display_final_solution(self, solution, fitness, position):
        print("Résultat final des cartons :")
        print(f"Poids maximal autorisé : {self.instance_data.max_weight}, Volume maximal autorisé : {self.instance_data.max_volume}")
        for i, box in enumerate(solution):
            print(f"Carton {box.id}: poids={str(box.used_weight)}; volume={str(box.used_volume)} ")
        print(f"Fitness finale : ", fitness)
        print("Position finale : ", position)
