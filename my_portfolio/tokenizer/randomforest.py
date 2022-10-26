from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split


class RF(RandomForestClassifier):
	name = "RF"
	RFC_grid = {RandomForestClassifier(): {"n_estimators": [i for i in range(1, 25)],
                                    "criterion": ["gini", "entropy"],
                                    "max_depth":[i for i in range(1, 5)],
                                    "random_state": [i for i in range(0, 101)]
                                    }}
	def __init__(self):
		super().__init__(max_depth=10, n_estimators=50, random_state=10)

	def train(self, x, y):
		self.fit(x, y)
	
	def predict(self, x):
		return super().predict(x)

	def predict_prob(self, x):
		return super().predict_proba(x)[0][:,1]




