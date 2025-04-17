

import csv
import pandas as pd

class AlgRunner:
 def __init__(self):
     self.csv_file_path = "./uploads/export_6.csv"
     self.algorithms = [    {"ANOVA": 5},
                          {"PCA": 5},
                          {"alg13": 5},
                          {"alg41": 5}  ]
     
     
 def runner(self):    
    try:

        df = pd.read_csv(self.csv_file_path)
        print(df.head())
        print("got it!")

    except FileNotFoundError:
        print(f"File not found: {json_file_path}")
        self.algorithms = []
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        self.algorithms = []

    # Iterate through the list of algorithms
    for idx, algo in enumerate(self.algorithms, start=1):
        #module = algo.get("module")
        #function = algo.get("function")
        print(algo)
        #print(f"Algorithm {idx}: Module = {module}, Function = {function}")

        #calc = CalcAlgorithmInterface()
        #calc.calc()

