import importlib
import json
import logging

class CalcAlgorithmInterface:
    def __init__(self):
        self.data = None
        self.algorithm = None
        self.results = None
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)
    
    def calc(self):
        calc.load_data("data.json")
        calc.load_algorithm("algorithms", "simple_grading")
        calc.compute_grades()
        print(calc.get_results())
        calc.save_results("results.json")

    def load_data(self, file_path):
        """Load data from a JSON file."""
        try:
            with open(file_path, 'r') as file:
                self.data = json.load(file)
            self.logger.info(f"Data loaded from {file_path}")
        except Exception as e:
            self.logger.error(f"Error loading data: {e}")
            raise

    def load_algorithm(self, module_name, function_name):
        """Load algorithm dynamically from a module."""
        try:
            module = importlib.import_module(module_name)
            self.algorithm = getattr(module, function_name)
            self.logger.info(f"Algorithm {function_name} loaded from {module_name}")
        except Exception as e:
            self.logger.error(f"Error loading algorithm: {e}")
            raise

    def compute_grades(self):
        """Compute grades using the loaded algorithm."""
        if not self.data or not self.algorithm:
            raise ValueError("Data or algorithm not loaded.")
        
        try:
            self.results = self.algorithm(self.data)
            self.logger.info("Grades computed successfully.")
        except Exception as e:
            self.logger.error(f"Error computing grades: {e}")
            raise

    def get_results(self):
        """Return computed results."""
        return self.results

    def save_results(self, file_path):
        """Save results to a JSON file."""
        try:
            with open(file_path, 'w') as file:
                json.dump(self.results, file, indent=4)
            self.logger.info(f"Results saved to {file_path}")
        except Exception as e:
            self.logger.error(f"Error saving results: {e}")
            raise
