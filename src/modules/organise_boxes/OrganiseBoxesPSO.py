import random
from typing import List

from src.models.box import Box
from src.models.instance_data import InstanceData
from src.models.order import Order
from src.models.product_quantity_pair import ProductQuantityPair
from src.modules.organise_boxes.base import BaseOrganiseBoxesModule
from src.models.product import Product


class Particle:
    def __init__(self, order: Order, max_boxes: int):
        # Initialisation des particules
        # La position est la répartition des produits dans les cartons : [1, 2, 1, 3, 2, 1, ...] =
        # produit 1 dans le carton 1, produit 2 dans le carton 2, produit 3 dans le carton 1, etc.
        self.position = [random.randint(1, max_boxes) for _ in
                         range(order.number_of_products)]  # Assignation aléatoire de produits aux cartons
        self.velocity = [0] * order.number_of_products  # Vitesse initiale
        self.best_position = self.position[:]  # Meilleure position personnelle
        self.best_fitness = float('inf')  # Meilleure fitness personnelle
        self.fitness = float('inf')  # Fitness actuelle
        self.order = order



class OrganiseBoxesPSO(BaseOrganiseBoxesModule):
    def __init__(self, instance_data: InstanceData, max_iter=30, num_particles=10):
        self.max_iter = max_iter
        self.num_particles = num_particles
        self.omega = 0.5  # Facteur d'inertie
        self.phi_p = 1.5  # Composante cognitive
        self.phi_g = 1.5  # Composante sociale
        super().__init__(instance_data)

    def fitness(self, particle: Particle, order: Order, flat_product_list : list[Product]) -> float:
        """Calcul de la fitness pour une particule, basé sur la somme des distances."""
        total_distance = 0
        max_weight = self.instance_data.max_weight
        max_volume = self.instance_data.max_volume

        # Créer une liste de boîtes
        boxes = [Box(order, []) for _ in range(order.max_number_of_boxes)]

        # Itérer sur les positions des particules (chaque élément correspond à un produit dans la liste aplatie)
        for idx, carton in enumerate(particle.position):
            product = flat_product_list[idx]  # Utiliser la liste aplatie

            # Ajouter le produit à la boîte en utilisant la nouvelle méthode add_product
            boxes[carton - 1].add_product(product)

        for box in boxes:
            # Calculer l'exces de poids et de volume
            weight_excess = max(0, box.used_weight - max_weight)
            volume_excess = max(0, box.used_volume - max_volume)
            # Si le poids ou le volume dépasse la limite, calculer la pénalité
            if weight_excess > 0 or volume_excess > 0:
                total_distance += 10000 * (10 * weight_excess + volume_excess)
            # Calculer la somme des distances des boîtes (chemin total parcouru par chaque picker)
            elif box.product_quantity_pairs:
                # Trier les localisations des produits dans chaque boîte
                product_locations = sorted([p.product.location_id for p in box.product_quantity_pairs])
                total_distance += self.calculate_box_distance(product_locations)

        return total_distance

    def calculate_box_distance(self, product_locations_ids: List[int]) -> float:
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

    def run(self) -> List[Box]:
        """Implémente l'algorithme PSO pour organiser les boîtes."""
        boxes = []
        for order in self.instance_data.orders:
            boxes.extend(self.runPSOOrder(order))
        return boxes

    def runPSOOrder(self, order: Order) -> List[Box]:
        best_global_position = None
        best_global_fitness = float('inf')

        # Aplatir la liste des produits pour obtenir une liste de produits individuels
        flat_product_list = ProductQuantityPair.flatten_product_quantity_pairs_list(order.products)

        # Initialiser les particules
        particles = [Particle(order, order.max_number_of_boxes)  for _ in range(self.num_particles)]

        # Assure-toi que la taille de best_global_position correspond à celle de particle.position
        if particles:
            best_global_position = particles[0].position[
                                   :]  # Utilise la première particule pour définir la taille correcte

        for iter in range(self.max_iter):
            print(f"Iteration {iter + 1}/{self.max_iter}")
            for particle in particles:
                order = particle.order

                # Évaluer la fitness de la particule
                particle.fitness = self.fitness(particle, order, flat_product_list)

                # Mettre à jour la meilleure position personnelle
                if particle.fitness < particle.best_fitness:
                    particle.best_fitness = particle.fitness
                    particle.best_position = particle.position[:]

                # Mettre à jour la meilleure position globale
                if particle.fitness < best_global_fitness:
                    best_global_fitness = particle.fitness
                    best_global_position = particle.position[:]  # Copie la position correcte ici

            # Affichage de la meilleure fitness trouvée à chaque itération
            print(f"Meilleure fitness de cette itération : {best_global_fitness}")

            # Mise à jour des vitesses et des positions
            for particle in particles:
                order = particle.order
                for i in range(order.number_of_products):
                    r_p = random.random()
                    r_g = random.random()

                    # Mise à jour de la vitesse selon l'équation PSO
                    particle.velocity[i] = (self.omega * particle.velocity[i]
                                            + self.phi_p * r_p * (particle.best_position[i] - particle.position[i])
                                            + self.phi_g * r_g * (best_global_position[i] - particle.position[i]))

                    # Mise à jour de la position (répartition des produits)
                    particle.position[i] = int(particle.position[i] + particle.velocity[i])
                    # On s'assure que la position reste dans les limites (1 à max_number_of_boxes)
                    particle.position[i] = max(1, min(order.max_number_of_boxes, particle.position[i]))



        # Une fois les itérations terminées, retourner les boîtes correspondant à la meilleure solution
        best_boxes = [Box(order, []) for _ in range(order.max_number_of_boxes)]
        for i_product, box_id in enumerate(best_global_position):
            product = flat_product_list[i_product]
            best_boxes[box_id - 1].add_product(product)

        # Affichage du résultat final
        print("Résultat final des cartons :")
        for i, box in enumerate(best_boxes):
            product_list = [f"produit {pq.product.product_id} (quantité: {pq.quantity})" for pq in box.product_quantity_pairs]
            print(f"Carton {box.id}: {', '.join(product_list) if product_list else 'Vide'}")

        return best_boxes
