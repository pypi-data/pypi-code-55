from . import optilab_pb2
from . import optimizer_model_pb2
from . import parallel_model
from . import evolutionary_model_pb2
from .evolutionary_problem import EvolutionaryModelType
from . import evolutionary_problem
from . import genetic_problem
from .EvolutionaryModels.Chromosome import Chromosome

import numpy as np
import logging
import string

class OptimizerEvolutionaryModel(parallel_model.ParallelModel):
    """OptiLab Evolutionary model solved by back-end optimizers"""

    model_type = None
    model_name = ""
    evolutionary_model = None

    def __init__(self, name, model_type):
        """Generates a new evolutionary model"""
        if not name.strip():
            err_msg = "OptimizerEvolutionaryModel - empty model name"
            logging.error(err_msg)
            raise Exception(err_msg)
        self.model_name = name

        if not isinstance(model_type, EvolutionaryModelType):
            err_msg = "OptimizerEvolutionaryModel - invalid model type " + type(model_type)
            logging.error(err_msg)
            raise Exception(err_msg)
        self.model_type = model_type
        if self.model_type is EvolutionaryModelType.GENETIC:
            self.evolutionary_model = genetic_problem.GeneticProblem(self.model_name)
        else:
            err_msg = "OptimizerEvolutionaryModel - unrecognized evolutionary model"
            logging.error(err_msg)
            raise Exception(err_msg)

    def on_message_impl(self, optilab_reply_message):
        if optilab_reply_message.details.Is(evolutionary_model_pb2.EvolutionarySolutionProto.DESCRIPTOR):
            # Capture the protobuf solution
            sol_proto = evolutionary_model_pb2.EvolutionarySolutionProto()
            optilab_reply_message.details.Unpack(sol_proto)
            self.upload_proto_solution(sol_proto)
        else:
            msg = "OptimizerEvolutionaryModel - received an unrecognized back-end message"
            logging.error(err_msg)
            print(msg)

    def upload_proto_solution(self, evolutionary_model_solution_proto):
        # Upload the solution on the routing model itself
        self.evolutionary_model.upload_proto_solution(evolutionary_model_solution_proto)

    def get_model(self):
        """Returns the typed-instance of the routing model"""
        return self.evolutionary_model

    def get_instance(self):
        """Returns the typed-instance of the routing model"""
        return self.evolutionary_model

    def get_solution(self):
        return self.evolutionary_model.get_solution()

    def name(self):
        """Returns the name of this model"""
        return self.model_name

    def serialize(self):
        return self.to_protobuf().SerializeToString()

    def to_protobuf(self):
        """To protocol buffer method: to be overriden by derived classes"""
        return self.evolutionary_model.to_protobuf()
