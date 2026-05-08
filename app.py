"""
WAREHOUSE 4.0 - AI OPTIMIZED LOGISTICS SYSTEM
------------------------------------------------
Features:
1. Dynamic layout optimization (AI-driven slotting)
2. Two zones:
   - Heavy & Special Products Zone
   - Normal Products Zone
3. Picking time optimization
4. Scalability (modular + distributed-ready design)
5. Event-driven system for unexpected events
6. Heuristic + ML-ready architecture

Author: AI Assistant (for educational/industrial prototype)
"""

import math
import random
from collections import defaultdict
from datetime import datetime

# =============================
# DATA MODELS
# =============================

class Product:
    def __init__(self, product_id, weight, frequency, special=False):
        self.product_id = product_id
        self.weight = weight
        self.frequency = frequency  # demand frequency
        self.special = special      # fragile / dangerous / heavy

class Location:
    def __init__(self, loc_id, x, y, zone):
        self.loc_id = loc_id
        self.x = x
        self.y = y
        self.zone = zone  # 'HEAVY' or 'NORMAL'
        self.assigned_product = None

class Order:
    def __init__(self, order_id, products):
        self.order_id = order_id
        self.products = products

# =============================
# WAREHOUSE MODEL
# =============================

class Warehouse:
    def __init__(self):
        self.locations = []
        self.products = {}
        self.distance_cache = {}

    def add_location(self, loc):
        self.locations.append(loc)

    def add_product(self, product):
        self.products[product.product_id] = product

    # Euclidean distance (can be replaced by real path routing)
    def distance(self, loc1, loc2):
        return math.sqrt((loc1.x - loc2.x)**2 + (loc1.y - loc2.y)**2)

# =============================
# INITIAL LAYOUT DESIGN
# =============================

class LayoutOptimizer:

    def __init__(self, warehouse):
        self.wh = warehouse

    def score_location(self, product, location):
        """
        Higher score = better placement
        - High frequency products near picking station (0,0)
        - Heavy products in heavy zone
        """
        base_distance = math.sqrt(location.x**2 + location.y**2)

        score = product.frequency * (1 / (1 + base_distance))

        if product.special and location.zone != "HEAVY":
            score -= 100  # penalty

        if product.weight > 20 and location.zone != "HEAVY":
            score -= 50

        return score

    def optimize_layout(self):
        unassigned_products = list(self.wh.products.values())
        available_locations = self.wh.locations.copy()

        # Sort products by importance (frequency)
        unassigned_products.sort(key=lambda p: p.frequency, reverse=True)

        for product in unassigned_products:
            best_loc = None
            best_score = -99999

            for loc in available_locations:
                score = self.score_location(product, loc)
                if score > best_score:
                    best_score = score
                    best_loc = loc

            if best_loc:
                best_loc.assigned_product = product.product_id
                available_locations.remove(best_loc)

# =============================
# PICKING OPTIMIZATION
# =============================

class PickerOptimizer:

    def __init__(self, warehouse):
        self.wh = warehouse

    def route_distance(self, route):
        total = 0
        for i in range(len(route) - 1):
            total += self.wh.distance(route[i], route[i+1])
        return total

    def optimize_order(self, order):
        locations = []

        for loc in self.wh.locations:
            if loc.assigned_product in order.products:
                locations.append(loc)

        # Simple nearest neighbor heuristic
        start = Location("START", 0, 0, "DEPOT")
        route = [start]
        remaining = locations.copy()

        current = start

        while remaining:
            next_loc = min(remaining, key=lambda l: self.wh.distance(current, l))
            route.append(next_loc)
            remaining.remove(next_loc)
            current = next_loc

        route.append(start)

        return route, self.route_distance(route)

# =============================
# EVENT HANDLING SYSTEM
# =============================

class EventSystem:

    def __init__(self, warehouse):
        self.wh = warehouse

    def handle_event(self, event):
        if event["type"] == "STOCK_OUT":
            self.reallocate(event["product_id"])

        elif event["type"] == "NEW_DEMAND_PATTERN":
            self.reoptimize_layout()

        elif event["type"] == "LOCATION_BLOCKED":
            self.free_alternative(event["loc_id"])

    def reallocate(self, product_id):
        print(f"Reallocating product {product_id}")

    def reoptimize_layout(self):
        print("Reoptimizing full layout...")
        optimizer = LayoutOptimizer(self.wh)
        optimizer.optimize_layout()

    def free_alternative(self, loc_id):
        print(f"Finding alternative for blocked location {loc_id}")

# =============================
# SCALABILITY DESIGN (SIMULATED)
# =============================

class DistributedWarehouseNode:
    def __init__(self, node_id):
        self.node_id = node_id
        self.local_data = {}

    def sync(self, global_state):
        self.local_data.update(global_state)

class WarehouseCluster:
    def __init__(self):
        self.nodes = []

    def add_node(self, node):
        self.nodes.append(node)

    def broadcast(self, state):
        for node in self.nodes:
            node.sync(state)

# =============================
# SIMULATION ENGINE
# =============================

class WarehouseSimulation:

    def __init__(self):
        self.wh = Warehouse()
        self.event_system = EventSystem(self.wh)

    def setup(self):
        # Create locations (grid)
        for i in range(5):
            for j in range(5):
                zone = "HEAVY" if i < 2 else "NORMAL"
                self.wh.add_location(Location(f"L{i}{j}", i, j, zone))

        # Create products
        for i in range(10):
            self.wh.add_product(Product(
                f"P{i}",
                weight=random.randint(1, 50),
                frequency=random.randint(1, 100),
                special=random.choice([True, False])
            ))

    def run(self):
        optimizer = LayoutOptimizer(self.wh)
        optimizer.optimize_layout()

        picker = PickerOptimizer(self.wh)

        order = Order("O1", ["P1", "P2", "P3"])
        route, dist = picker.optimize_order(order)

        print("Optimized picking distance:", dist)

        # simulate event
        self.event_system.handle_event({
            "type": "NEW_DEMAND_PATTERN"
        })

# =============================
# MAIN
# =============================

if __name__ == "__main__":
    sim = WarehouseSimulation()
    sim.setup()
    sim.run()

"""
EXTENSIONS POSSIBLES (INDUSTRIAL REAL):
---------------------------------------
1. Reinforcement Learning (RL) for layout optimization
2. Real-time IoT integration (RFID, sensors)
3. Digital Twin (3D warehouse simulation)
4. Multi-warehouse coordination (supply chain network)
5. Graph-based shortest path (A* algorithm instead of greedy)
6. Predictive demand forecasting (LSTM / Prophet)
"""
