# Data wrangling 
import pandas as pd 

# Array math
import numpy as np 

# Quick value count calculator
from collections import Counter

class node: 
    """
    Class for creating the nodes for a DT
    """
    def __init__(
        self,
        Y: list,
        X: pd.DataFrame,
        min_samples_split=None,
        max_depth=None,
        depth=None,
        node_type=None,
        rule=None
    ):
        #saving the data to the node
        self.Y = Y
        self.X = X

        #saving the hyper parameter
        self.min_samples_split = min_samples_split if min_samples_split else 20
        self.max_depth = max_depth if max_depth else 5

        #default current depth of node
        self.depth = depth if depth else 0

        #extracting all the features
        self.features = list(self.X.columns)

        #type of node 
        self.node_type = node_type if node_type else 'root'

        #rule for spliting 
        self.rule = rule if rule else ""

        #calculating the counts of Y in the node 
        self.counts = Counter(Y)

        #getting the GINI impurity based on the Y distribution
        self.gini_impurity = self.get_GINI()

        #sorting the counts and saving the final prediction of the node 
        counts_sorted = list(sorted(self.counts.items(), key=lambda item: item[1]))