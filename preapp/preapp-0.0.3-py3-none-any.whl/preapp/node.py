from abc import ABC
from typing import Dict, Any, Callable, List, Tuple
import json
from PyInquirer import prompt
from queue import PriorityQueue
from .question import Question


class Node(ABC):
    """Base class for a node in the input tree """

    _full_response: Dict[str, Any] = dict()
    """This is a json representation in memory of the final config generated
    """

    _node_table: Dict[str, Tuple["Node", bool]] = dict()
    """This is a table of all the nodes registered and if they have been processed yet
    """

    def __init__(
        self,
        name: str,
        questions: List[Question],
        parents: List[str] = [],
        children: List[str] = [],
        priority: int = 0,
        serializable: bool = True,
    ):
        """Creates a new Node

        Args:
            :param name (str): the unique string identifier of this node
            :param questions (List[Question]): a list of user input for this node
            :param parents (List[str]): the names of nodes that need to be processed before this node
            :param children (List[str]): the names of nodes that should be processed after this node
            :param priority (int): the exection priority of this node. lower values get processed first
            :param serializable (bool): flag if the data from this node should be printed to the config file generated
        """
        self.name = name
        self.questions = questions
        self._parents = parents
        self.parents = PriorityQueue()
        self._children = children
        self.children = PriorityQueue()
        self.priority = priority
        self.serializable = serializable

    def pre_process(self) -> None:
        """Method called before this node processes its questions

        Note:
            this method does not need to be implemented if it is not used
        """
        pass

    def post_process(self, responses: Dict[str, Any]) -> None:
        """Method called after this node processes its questions

        Note:
            this method does not need to be implemented if it is not used
        """
        pass

    def process(self) -> None:
        """Processes this node
        """

        # this guarentees this value isn't oevr written by a file input
        self.add_attribute({"serializable": self.serializable})

        for key in self._parents:
            node: "Node" = Node._node_table[key][0]
            self.parents.put((node.priority, node))

        for key in self._children:
            node: "Node" = Node._node_table[key][0]
            self.children.put((node.priority, node))

        # process all the required nodes frist
        while self.parents.qsize():
            self.parents.get()[1].process()

        # if the node has not been processed then process it
        # if not Node._triggered_table[self.name]:
        if not Node._node_table[self.name][1]:
            # run code to prepare this node to be processed
            self.pre_process()

            # process the questions for this node
            for question in self.questions:
                if not question.name() in Node._full_response[self.name]:
                    self.add_attribute(prompt(question.json()))

            # run code to finialize the processing of this node
            self.post_process(Node._full_response[self.name])

            # mark the node as executed
            # Node._triggered_table[self.name] = True
            Node._node_table[self.name] = (Node._node_table[self.name][0], True)

        # execute the nodes that this triggers
        while self.children.qsize():
            self.children.get()[1].process()

    def add_attribute(self, attribute: Dict[str, Any]) -> None:
        """Adds an attribute to the config file generated

        Args:
            :param attribute (Dict[str, Any]): the attribute being added to the config file
        """
        sub_list: List[Any] = []
        sub_list.append(Node._full_response[self.name])
        sub_list.append(attribute)
        sub_dict: Dict[str, Any] = dict()
        for item in sub_list:
            for key, value in item.items():
                sub_dict[key] = value

        Node._full_response[self.name] = sub_dict

    def add_question(self, question: Question) -> None:
        """Adds a question to this node

        Args:
            :param question (Question): the question being added
        """
        self.questions.append(question)

    def add_child(self, key: str) -> None:
        """Adds a child node to be processed after this node is processed

        Args:
            :param key (str): the name of the child node to be processed
        """
        node: "Node" = Node._node_table[key][0]
        self.children.put((node.priority, node))

    @staticmethod
    def get_full_response() -> Dict[str, Any]:
        """Gets the full response to this time of all nodes currently run
        
        Returns:
            Dict[str, Any]: dictionary of all of the nodes run in json format
        
        """
        return Node._full_response

    @staticmethod
    def is_registered(node: "Node") -> bool:
        """Returns True of this node has been registered globally
        """
        return node.name in Node._node_table

    @staticmethod
    def register(node: "Node") -> None:
        """Registers a node globally
        """
        if not Node.is_registered(node):
            Node._full_response[node.name] = {}
            Node._node_table[node.name] = (node, False)

    @staticmethod
    def reset() -> None:
        """Clears the full response maintained statically by this class """
        Node._full_response.clear()

    def __lt__(self, value):
        return self.priority >= value.priority
