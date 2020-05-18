from .agent import Agent
from .model import Model
import numpy as np
import pandas as pd
import seaborn as sns
from bayes_opt import BayesianOptimization
sns.set()

class IonBayes:
    accbest = 0.0
    def __init__(
        self,
        path: str = '../dataset/TSLA.csv',
        window_size:int = 30,
        skip: int = 5,
        max_buy: int = 5,
        max_sell: int = 5,
        money: int = 10_000
    ) -> None:
        self.window_size = window_size
        self.skip = skip
        self.df = pd.read_csv(path)
        self.close = self.df.Close.values.tolist()
        self.l = len(self.close) - 1
        self.money = money, 
        self.max_buy = max_buy, 
        self.max_sell = max_sell, 
    def agent(
        self,
        window_size: int,
        skip: int,
        population_size: int,
        sigma: float,
        learning_rate: float,
        size_network: int
    ):
        model = Model(window_size, size_network, 3)
        agent = Agent(
            population_size,
            sigma,
            learning_rate,
            model,
            10000,
            5,
            5,
            skip,
            window_size,
        )
        try:
            agent.fit(100, 1000)
            return agent.es.reward_function(agent.es.weights)
        except:
            return 0

    def find_agent(
        self,
        window_size,
        skip,
        population_size,
        sigma,
        learning_rate,
        size_network
    ):
        param = {
            'window_size': int(np.around(window_size)),
            'skip': int(np.around(skip)),
            'population_size': int(np.around(population_size)),
            'sigma': max(min(sigma, 1), 0.0001),
            'learning_rate': max(min(learning_rate, 0.5), 0.000001),
            'size_network': int(np.around(size_network)),
        }
        print('\nSearch parameters %s' % (param))
        investment = self.agent(**param)
        print('stop after 100 iteration with investment %f' % (investment))
        if investment > self.accbest:
            self.accbest = investment
        return investment
    def bayes_maximize(self):
        self.NN_BAYESIAN = BayesianOptimization(
            self.find_agent,
            {
                'window_size': (2, 50),
                'skip': (1, 15),
                'population_size': (1, 50),
                'sigma': (0.01, 0.99),
                'learning_rate': (0.000001, 0.49),
                'size_network': (10, 1000),
            },
        )
        return self.NN_BAYESIAN.maximize(init_points = 30, n_iter = 50, acq = 'ei', xi = 0.0)
    def run(self):
        max_params = self.NN_BAYESIAN.res['max']['max_params']
        self.agent(
            window_size = int(np.around(max_params['window_size'])), 
            skip = int(np.around(max_params['skip'])), 
            population_size = int(np.around(max_params['population_size'])), 
            sigma = max_params['sigma'], 
            learning_rate = max_params['learning_rate'], 
            size_network = int(np.around(max_params['size_network']))
        )
        model = Model(
            input_size = int(np.around(max_params['window_size'])), 
            layer_size = int(np.around(max_params['size_network'])), 
            output_size = 3
        )
        agent = Agent(
            population_size = int(np.around(max_params['population_size'])), 
            sigma = max_params['sigma'], 
            learning_rate = max_params['learning_rate'], 
            model = model, 
            money = self.money, 
            max_buy = self.max_buy, 
            max_sell = self.max_sell, 
            skip = int(np.around(max_params['skip'])), 
            window_size = int(np.around(max_params['window_size']))
        )
        agent.fit(500, 100)
        agent.buy()