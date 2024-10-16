import unittest
from unittest.mock import MagicMock

from src.models.box import Box
from src.models.instance_data import InstanceData
from src.models.order import Order
from src.models.product_quantity_pair import ProductQuantityPair
from src.models.product import Product
from src.modules.organise_boxes.OrganiseBoxesPSOV2 import OrganiseBoxesPSOV2, Particle


class TestOrganiseBoxesPSOV2(unittest.TestCase):
    def setUp(self):
        # Configurer les données d'instance et l'ordre pour les tests
        self.instance_data = MagicMock(spec=InstanceData)
        self.instance_data.max_weight = 100  # Exemple de poids max
        self.instance_data.max_volume = 200  # Exemple de volume max
        self.instance_data.orders = [MagicMock(spec=Order)]

        # Créer une liste de plus courts chemins (mimique de la structure utilisée)
        self.instance_data.shortest_paths = [
            MagicMock(start_localisation_id=1, end_localisation_id=2, distance=10),
            MagicMock(start_localisation_id=2, end_localisation_id=3, distance=20),
            MagicMock(start_localisation_id=1, end_localisation_id=3, distance=30),
        ]

        self.order = self.instance_data.orders[0]
        self.order.max_number_of_boxes = 5
        self.order.number_of_products = 10

        self.pso = OrganiseBoxesPSOV2(self.instance_data)

    def test_fitness(self):
        # Créer des produits avec des poids, volumes et localisation spécifiques
        product1 = Product(product_id=1, weight=20, volume=50, location_id=1)
        product2 = Product(product_id=2, weight=30, volume=60, location_id=2)
        product3 = Product(product_id=3, weight=50, volume=70, location_id=3)

        # Ajouter les produits avec des quantités
        pq1 = ProductQuantityPair(product=product1, quantity=1)
        pq2 = ProductQuantityPair(product=product2, quantity=1)
        pq3 = ProductQuantityPair(product=product3, quantity=1)

        # Aplatir la liste des produits
        flat_product_list = [pq1.product, pq2.product, pq3.product]

        # Initialiser une particule avec une position qui place chaque produit dans le premier carton
        particle_position = [1, 1, 2]  # product1 et product2 dans le carton 1, product3 dans le carton 2
        particle = Particle(self.order, particle_position)

        # Calculer la fitness
        fitness_value = self.pso.fitness(particle, self.order, flat_product_list)

        # Vérifier le calcul de la distance et des pénalités
        # On s'attend à ce qu'il n'y ait pas de pénalité de poids/volume, mais une distance totale :
        # Carton 1 : distance entre produit1 (loc 1) et produit2 (loc 2) = 10
        # Carton 2 : produit3 seul => distance nulle
        # Total expected distance = 10
        self.assertEqual(fitness_value, 10)

    def test_fitness_with_excess_weight(self):
        # Créer des produits avec des poids qui dépassent la limite
        product1 = Product(product_id=1, weight=120, volume=50, location_id=1)  # Dépasse le poids max
        product2 = Product(product_id=2, weight=30, volume=60, location_id=2)
        product3 = Product(product_id=3, weight=50, volume=70, location_id=3)

        # Ajouter les produits avec des quantités
        pq1 = ProductQuantityPair(product=product1, quantity=1)
        pq2 = ProductQuantityPair(product=product2, quantity=1)
        pq3 = ProductQuantityPair(product=product3, quantity=1)

        # Aplatir la liste des produits
        flat_product_list = [pq1.product, pq2.product, pq3.product]

        # Initialiser une particule avec une position qui place chaque produit dans le premier carton
        particle_position = [1, 1, 2]  # product1 et product2 dans le carton 1, product3 dans le carton 2
        # donc le carton 1 dépassera le poids max de 100 (120 + 30 = 150)
        # pénalité = 100000 * (150 - 100) = 500000
        particle = Particle(self.order, particle_position)

        # Calculer la fitness
        fitness_value = self.pso.fitness(particle, self.order, flat_product_list)

        self.assertEqual(200000020, fitness_value)

    def test_initialize_particles(self):
        """Test pour vérifier l'initialisation des particules."""
        order = MagicMock()  # Mock ou donnée réelle
        order.max_number_of_boxes = 5  # Nombre de boîtes maximum
        initial_positions = [1, 1, 2, 2, 3, 4, 1, 2]  # Positions initiales à définir
        particles = self.pso.initialize_particles(order, initial_positions)
        self.assertEqual(len(particles), self.pso.num_particles)
        self.assertIsInstance(particles[0], Particle)

    def test_calculate_box_distance(self):
        # Tester le calcul de la distance de la boîte
        product_locations_ids = [1, 2, 3]
        self.instance_data.shortest_paths = [
            MagicMock(start_localisation_id=1, end_localisation_id=2, distance=10),
            MagicMock(start_localisation_id=2, end_localisation_id=3, distance=5),
        ]
        distance = self.pso.calculate_box_distance(product_locations_ids)
        self.assertEqual(distance, 15)

    def test_convert_solution_to_position(self):
        # Instancier l'objet OrganiseBoxesPSO pour appeler la méthode convert_solution_to_position
        pso = OrganiseBoxesPSOV2(None)

        # Simuler des produits
        product1 = Product(product_id=1, weight=20, volume=10, location_id=101)
        product2 = Product(product_id=2, weight=30, volume=15, location_id=102)
        product3 = Product(product_id=3, weight=10, volume=5, location_id=103)

        # Simuler des ProductQuantityPairs
        pqp1 = ProductQuantityPair(product1, quantity=2)  # product1 avec quantité 2
        pqp2 = ProductQuantityPair(product2, quantity=1)  # product2 avec quantité 1
        pqp3 = ProductQuantityPair(product3, quantity=1)  # product3 avec quantité 1

        # Créer des boîtes factices
        box1 = Box(None, [pqp1])  # product1 (2 fois) dans box1
        box2 = Box(None, [pqp2])  # product2 dans box2
        box3 = Box(None, [pqp3])  # product3 dans box3

        # Liste des boîtes
        solution_boxes = [box1, box2, box3]

        # Appeler la méthode à tester
        position = pso.convert_boxes_to_position(solution_boxes)

        # La solution attendue est [1, 1, 2, 3] car :
        # - product1 (x2) est dans box1 (ID = 1),
        # - product2 est dans box2 (ID = 2),
        # - product3 est dans box3 (ID = 3).
        expected_position = [1, 1, 2, 3]

        # Vérifier que la position calculée est correcte
        self.assertEqual(position, expected_position)

    def test_convert_solution_to_position2(self):
        # Tester la conversion de la solution en position
        boxes = [Box(self.order, []) for _ in range(3)]
        product1 = Product(product_id=1, location_id=1, weight=10, volume=5)
        product2 = Product(product_id=2, location_id=1, weight=10, volume=5)
        boxes[0].add_product_quantity_pair(ProductQuantityPair(product1, 1))
        boxes[1].add_product_quantity_pair(ProductQuantityPair(product2, 1))

        flat_product_list = [product1, product2]
        positions = self.pso.convert_boxes_to_position(boxes)
        self.assertEqual(positions, [1, 2])  # Devrait correspondre aux IDs de boîte

    def test_convert_boxes_to_position_to_boxes(self):
        # Création de produits fictifs
        product1 = Product(product_id=1, location_id=1, weight=10, volume=5)
        product2 = Product(product_id=2, location_id=2, weight=10, volume=5)
        product3 = Product(product_id=3, location_id=3, weight=10, volume=5)
        product4 = Product(product_id=4, location_id=4, weight=10, volume=5)

        # Création de cartons avec des produits et leurs quantités
        box1 = Box(self.order, [])
        box1.add_product_quantity_pair(ProductQuantityPair(product1, 5))  # 5 de product1
        box1.add_product_quantity_pair(ProductQuantityPair(product2, 1))  # 1 de product2

        box2 = Box(self.order, [])
        box2.add_product_quantity_pair(ProductQuantityPair(product3, 8))  # 8 de product3

        box3 = Box(self.order, [])
        box3.add_product_quantity_pair(ProductQuantityPair(product4, 4))  # 4 de product4

        solution_boxes = [box1, box2, box3]

        # Aplatir la liste des produits
        flat_product_list = ProductQuantityPair.flatten_product_quantity_pairs_list(
            box1.product_quantity_pairs + box2.product_quantity_pairs + box3.product_quantity_pairs)

        # Convertir la solution en positions
        positions = self.pso.convert_boxes_to_position(solution_boxes)

        # Vérifier que les positions correspondent aux cartons
        self.assertEqual(positions, [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3])
        # 1 pour box1 (5 de product1 et 1 de product2)
        # 2 pour box2 (8 de product3)
        # 3 pour box3 (4 de product4)

        # Créer les cartons à partir de la meilleure position trouvée
        best_boxes = self.pso.convert_position_to_boxes(positions, self.order, flat_product_list)

        # Vérifier que les cartons ont les produits appropriés
        self.assertEqual(len(best_boxes[0].product_quantity_pairs), 2)  # box1 devrait avoir 2 produits
        self.assertEqual(len(best_boxes[1].product_quantity_pairs), 1)  # box2 devrait avoir 1 produit
        self.assertEqual(len(best_boxes[2].product_quantity_pairs), 1)  # box3 devrait avoir 1 produit

        # Vérifier les produits spécifiques dans chaque carton
        self.assertEqual(best_boxes[0].product_quantity_pairs[0].product.product_id, 1)
        self.assertEqual(best_boxes[0].product_quantity_pairs[1].product.product_id, 2)
        self.assertEqual(best_boxes[1].product_quantity_pairs[0].product.product_id, 3)
        self.assertEqual(best_boxes[2].product_quantity_pairs[0].product.product_id, 4)

        # Vérifier les quantités de produits dans chaque carton
        self.assertEqual(best_boxes[0].product_quantity_pairs[0].quantity, 5)
        self.assertEqual(best_boxes[0].product_quantity_pairs[1].quantity, 1)
        self.assertEqual(best_boxes[1].product_quantity_pairs[0].quantity, 8)
        self.assertEqual(best_boxes[2].product_quantity_pairs[0].quantity, 4)

        # Vérifier les poids et volumes utilisés dans chaque carton
        self.assertEqual(best_boxes[0].used_weight, 60)
        self.assertEqual(best_boxes[0].used_volume, 30)
        self.assertEqual(best_boxes[1].used_weight, 80)
        self.assertEqual(best_boxes[1].used_volume, 40)
        self.assertEqual(best_boxes[2].used_weight, 40)
        self.assertEqual(best_boxes[2].used_volume, 20)


    def test_generate_random_position_variation(self):
        # Tester la génération de variation de positions
        initial_positions = [1, 2, 3]
        max_boxes = 5
        variations = self.pso.generate_random_position_variation(initial_positions, max_boxes)

        # Vérifier que toutes les positions sont dans les limites
        for pos in variations:
            self.assertGreaterEqual(pos, 1)
            self.assertLessEqual(pos, max_boxes)

    # Fonction de test
    def test_repair_solution(self):
        # Créer des données d'instance avec des limites de poids et de volume
        self.instance_data.max_weight = 10
        self.instance_data.max_volume = 5

        # Créer une commande avec deux cartons et quelques produits
        order = MagicMock(spec=Order)
        order.max_number_of_boxes = 2

        # Créer des produits
        product1 = Product(product_id=1, weight=8, volume=3, location_id=1)  # Produit lourd
        product2 = Product(product_id=2, weight=5, volume=2, location_id=2)  # Produit léger
        product3 = Product(product_id=3, weight=2, volume=1, location_id=3)  # Produit léger

        # Liste aplatie de produits
        flat_product_list = [product1, product2, product3]

        # création des boîtes
        boxes = [Box(order) for _ in range(2)]
        boxes[0].add_product_quantity_pair(ProductQuantityPair(product1, 1))
        boxes[0].add_product_quantity_pair(ProductQuantityPair(product2, 1))
        boxes[1].add_product_quantity_pair(ProductQuantityPair(product3, 1))

        # Position initiale : produit1 dans le carton 1 et les autres dans le carton 2
        initial_position = [1, 1, 2]  # produit1 et produit2 dans le carton 1, produit3 dans le carton 2

        # Créer une particule avec une solution non valide
        particle = Particle(order, initial_position)

        # Appel de la fonction de réparation
        self.pso.repair_solution(particle, flat_product_list, order, boxes)

        self.assertEqual(True, particle.valid)

        expected_end_position = [1, 2, 2]

        self.assertEqual(expected_end_position, particle.position)

        # Vérifier que les cartons sont mis à jour
        self.assertEqual(len(boxes[0].product_quantity_pairs), 1)
        self.assertEqual(len(boxes[1].product_quantity_pairs), 2)

        #vérifier poids et volume final des cartons
        self.assertEqual(boxes[0].used_weight, 8)
        self.assertEqual(boxes[0].used_volume, 3)
        self.assertEqual(boxes[1].used_weight, 7)
        self.assertEqual(boxes[1].used_volume, 3)

    def test_repair_solution_should_be_invalid(self):
        # Créer des données d'instance avec des limites de poids et de volume
        self.instance_data.max_weight = 10
        self.instance_data.max_volume = 5

        # Créer une commande avec deux cartons et quelques produits
        order = MagicMock(spec=Order)
        order.max_number_of_boxes = 2

        # Créer des produits
        product1 = Product(product_id=1, weight=8, volume=3, location_id=1)  # Produit lourd
        product2 = Product(product_id=2, weight=8, volume=2, location_id=2)  # Produit léger
        product3 = Product(product_id=3, weight=3, volume=1, location_id=3)  # Produit léger

        # Liste aplatie de produits
        flat_product_list = [product1, product2, product3]

        # création des boîtes
        boxes = [Box(order) for _ in range(2)]
        boxes[0].add_product_quantity_pair(ProductQuantityPair(product1, 1))
        boxes[0].add_product_quantity_pair(ProductQuantityPair(product2, 1))
        boxes[1].add_product_quantity_pair(ProductQuantityPair(product3, 1))

        # Position initiale : produit1 dans le carton 1 et les autres dans le carton 2
        initial_position = [1, 1, 2]  # produit1 et produit2 dans le carton 1, produit3 dans le carton 2

        # Créer une particule avec une solution non valide
        particle = Particle(order, initial_position)

        # Appel de la fonction de réparation
        self.pso.repair_solution(particle, flat_product_list, order, boxes)

        self.assertEqual(False, particle.valid)

    def test_convert_position_to_boxes(self):
        self.products = [
            Product(1, 1, 1, 1),
            Product(2, 2, 1, 1),
            Product(2, 2, 1, 1),
            Product(3, 3, 1, 1),
            Product(4, 4, 1, 1),
            Product(4, 4, 1, 1),
            Product(5, 5, 1, 1),
        ]
        self.order = MagicMock(spec=Order)
        self.order.max_number_of_boxes = 4
        self.best_global_position = [1, 2, 1, 3, 2, 2, 4]  # Indices indiquant quelle boîte reçoit quel produit
        # Appel de la fonction à tester
        solution = self.pso.convert_position_to_boxes(self.best_global_position, self.order, self.products)

        # Vérifications
        self.assertEqual(len(solution), 4)  # On s'attend à 2 boîtes (car max_number_of_boxes = 4)

        # Boîte 1 doit contenir 1 produit d'id 1 et 1 produit d'id 2
        self.assertEqual(len(solution[0].product_quantity_pairs), 2)
        #1 produit d'id 1
        self.assertEqual(solution[0].product_quantity_pairs[0].product.product_id, 1)
        self.assertEqual(solution[0].product_quantity_pairs[0].quantity, 1)
        #1 produit d'id 2
        self.assertEqual(solution[0].product_quantity_pairs[1].product.product_id, 2)
        self.assertEqual(solution[0].product_quantity_pairs[1].quantity, 1)

        # Boîte 2 doit contenir 1 produit d'id 2 et 2 produit d'id 4
        self.assertEqual(len(solution[1].product_quantity_pairs), 2)
        #1 produit d'id 2
        self.assertEqual(solution[1].product_quantity_pairs[0].product.product_id, 2)
        self.assertEqual(solution[1].product_quantity_pairs[0].quantity, 1)
        #2 produit d'id 4
        self.assertEqual(solution[1].product_quantity_pairs[1].product.product_id, 4)
        self.assertEqual(solution[1].product_quantity_pairs[1].quantity, 2)

        # Boîte 3 doit contenir 1 produit d'id 3
        self.assertEqual(len(solution[2].product_quantity_pairs), 1)
        #1 produit d'id 3
        self.assertEqual(solution[2].product_quantity_pairs[0].product.product_id, 3)
        self.assertEqual(solution[2].product_quantity_pairs[0].quantity, 1)

        # Boîte 4 doit contenir 1 produit d'id 5
        self.assertEqual(len(solution[3].product_quantity_pairs), 1)
        #1 produit d'id 5
        self.assertEqual(solution[3].product_quantity_pairs[0].product.product_id, 5)
        self.assertEqual(solution[3].product_quantity_pairs[0].quantity, 1)


if __name__ == '__main__':
    unittest.main()