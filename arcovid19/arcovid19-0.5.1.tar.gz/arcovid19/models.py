#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2020, Bruno Sanchez, Mauricio Koraj, Vanessa Daza,
#                     Juan B Cabral, Mariano Dominguez, Marcelo Lares,
#                     Nadia Luczywo, Dante Paz, Rodrigo Quiroga,
#                     Martín de los Ríos, Federico Stasyszyn
#                     Cristian Giuppone.
# License: BSD-3-Clause
#   Full Text: https://raw.githubusercontent.com/ivco19/libs/master/LICENSE


# =============================================================================
# DOCS
# =============================================================================

"""Utilities to Utility function to parse all the actual cases of the
COVID-19 in Argentina.

"""

__all__ = [
    "NodeNotFoundError",
    "Node", "Graph", "InfectionCurve",
    "load_infection_curve"]


# =============================================================================
# IMPORTS
# =============================================================================

import pandas as pd

from matplotlib import pyplot as plt
import matplotlib.ticker as ticker

import seaborn as sns

import attr

from . import core


# =============================================================================
# CONSTANTS
# =============================================================================

# =============================================================================
# EXCEPTIONS
# =============================================================================

class NodeNotFoundError(KeyError):
    """If a node is not found inside a graph"""


# =============================================================================
# GRAPHS
# =============================================================================

@attr.s(repr=False, hash=True)
class Node:
    """This class is used to create and manipulated nodes.

    """

    id = attr.ib()
    value = attr.ib(eq=False)
    outgoing = attr.ib(factory=dict, eq=False)
    incoming = attr.ib(factory=dict, eq=False)

    def __repr__(self):
        string = (
            f"{self.id} node, "
            f"outgoing: {[x.id for x in self.outgoing]} "
            f"incoming: {[x.id for x in self.incoming]}")
        return string

    def add_neighbor(self, neighbor, names, values):
        self.outgoing[neighbor] = {}
        for n, v in zip(names, values):
            self.outgoing[neighbor][n] = v

    def be_neighbor(self, neighbor, names, values):
        self.incoming[neighbor] = {}
        for n, v in zip(names, values):
            self.incoming[neighbor][n] = v

    def get_connections(self):
        return self.outgoing.keys()

    def get_weight(self, neighbor):
        return self.outgoing[neighbor]


@attr.s(repr=False, frozen=True)
class Graph:
    """ This class is used to create and manipulated graphs.

    It makes a heavy use of the node class
    A graph is made of nodes and edges.  This class allows to store
    a value for each node and different "weights" for each edge.
    Also, edges are directed.

    Example
    -------

    >>> g = Graph()
    >>> for i, inode in enumerate(['A','B','C','D']):
    ...     print(i)
    ...     g.add_node(inode, 0)

    >>> nms = ['x', 'y']
    >>> g.add_edge('A', 'B', nms, [1, 100])
    >>> g.add_edge('A', 'C', nms, [2, 200])
    >>> g.add_edge('B', 'D', nms, [3, 300])
    >>> g.add_edge('D', 'B', nms, [4, 400])
    >>> g.add_edge('D', 'C', nms, [5, 500])
    >>> g.add_edge('C', 'C', nms, [6, 600])

    # A node can be connected to itself.
    >>> g.add_edge('B', 'B', nms, [333, 333])
    >>> g.show()
    ...

    Attributes
    ----------
    vert_dict: dict
        a dict containing the vertices

    """

    vert_dict = attr.ib(factory=dict)

    def __len__(self):
        return len(self.vert_dict)

    def __iter__(self):
        return iter(self.vert_dict.values())

    # node functions --------------------------------------
    def add_node(self, nnode, value):
        """Adds a new node to a graph.

        The node must have a value.

        """
        new_node = Node(nnode, value)
        self.vert_dict[nnode] = new_node
        return new_node

    def get_node(self, n):
        """Retrieve a node if exists.

        Parameters
        ----------
           n: str

        Returns
        -------
           node: a node object

        """
        return self.vert_dict.get(n)

    def get_node_value(self, n):
        """Returns the value of the node.

        Parameters
        ----------
           n: str

        Returns
        -------
           value: float

        """
        node = self.get_node(n)
        if node:
            return node.value

    def set_node(self, n, value):
        """Updates the Node value. The node must exists inside the graph.

        Parameters
        ----------
           n: str
              The ID or name of the node
           value: float
              The value to be assigned to the node

        """
        node = self.get_node(n)
        if node:
            node.value = value

    def get_node_ids(self):
        return list(self.vert_dict.keys())

    def get_nodes_to(self, nnode):
        v = self.get_node(nnode) or []
        c = [i.id for i in v.incoming]
        return c

    def get_nodes_from(self, nnode):
        v = self.get_node(nnode) or []
        c = [i.id for i in v.outgoing]
        return c

    # edge functions --------------------------------------
    def add_edge(self, frm, to, names=None, values=0):
        """Link two nodes inside a graph.

        Notes
        -----
            Does not verify if edge already exists

        Raises
        ------

        NodeNotFound:
            If one of the node are not tregistered in the graph

        """
        if names is None:
            names = []
        try:
            self.vert_dict[frm].add_neighbor(self.vert_dict[to], names, values)
            self.vert_dict[to].be_neighbor(self.vert_dict[frm], names, values)
        except KeyError as e:
            raise NodeNotFoundError from e

    def get_edge(self, frm, to, field):
        if frm not in self.vert_dict:
            self.add_node(frm)
        if to not in self.vert_dict:
            self.add_node(to)

        v_frm = self.get_node(frm)
        v_to = self.get_node(to)
        ws = v_frm.get_weight(v_to)
        return ws[field]

    # graph functions --------------------------------------
    def resume_weights(self):
        resume = []
        for v in self:
            nr = {"id": v.id, "value": v.value, "conections": []}
            for w in v.get_connections():
                nr["conections"].append({
                    "id": w.id, "weight": v.get_weight(w)})
            resume.append(nr)
        return resume

    def format_weights(self):
        formats = []
        for nr in self.resume_weights():
            nr_id = nr['id']
            nf = [f"Node {nr_id}: {nr['value']}"]
            for c in nr["conections"]:
                nf.append(f"\t{nr_id} -> {c['id']} {c['weight']}")
            formats.append(nf)
        return "\n".join(formats)

    def resume_connections(self):
        resume = []
        for inode in self.get_node_ids():
            nr = {
                "node": inode,
                "from": self.get_nodes_from(inode),
                "to": self.get_nodes_to(inode)}
            resume.append(nr)
        return resume

    def format_connections(self):
        formats = []
        for nr in self.resume_connections():
            nf = [
                f"Nodes from {nr['node']}: {nr['from']}",
                f"Nodes to {nr['node']}: {nr['to']}"]
            formats.append(nf)
        return "\n".join(formats)

    # computation functions --------------------------------
    def node_activation(self, nnode, key):
        nodes_to = self.get_nodes_to(nnode)
        activations = []
        for v in nodes_to:
            a = self.get_node(v)
            activations.append(self.get_edge(a.id, nnode, key))
        return activations

    def node_upgrade(self, nnode, key):
        nodes_to = self.get_nodes_to(nnode)
        upgrades = []
        for v in nodes_to:
            a = self.get_node(v)
            upgrades.append(self.get_edge(a.id, nnode, key))
        return upgrades


# =============================================================================
# API
# =============================================================================

class ModelResultPlotter(core.Plotter):
    default_plot_name_method = "infection_curve"

    def infection_curve(
        self, only=None, fill=False,
        log=False, ax=None, **kwargs
    ):
        """Plots the infection curve.

        Parameters
        ----------
        only : list, optional
            List of subset of columns of the models to be plotted.
        fill : boolean of float, optional
            If its true a all the area bellow the curve are filled with the
            same color of the curve with en alpha of ``0.1``. If fill is a
            float the value is interpreted as the alpha of the fill.
        log : boolean, default=False
            if
        ax : matplotlib Axes, optional
            Axes object to draw the plot onto, otherwise uses the current Axes.
        kwargs : key, value mappings
            Other keyword arguments are passed down to
            :meth:`seaborn.lineplot`.

        Returns
        -------
        ax : matplotlib Axes
            Returns the Axes object with the plot drawn onto it.

        """
        df = self.frame.df
        if only is not None:
            df = df[only]

        if ax is None:
            ax = plt.gca()

        if log:
            ax.set(yscale="log")
            ax.yaxis.set_major_formatter(
                ticker.FuncFormatter(lambda y, _: '{:g}'.format(y)))

        # our default values
        kwargs.setdefault("linewidth", 2)
        kwargs.setdefault("sort", False)
        kwargs.setdefault("dashes", False)

        sns.lineplot(data=df, ax=ax, **kwargs)

        if fill:
            alpha = 0.1 if isinstance(fill, bool) else fill
            for line in ax.lines[:len(df.columns)]:
                color = line.get_color()
                line_x = line.get_xydata()[:, 0]
                line_y = line.get_xydata()[:, 1]
                ax.fill_between(line_x, line_y, color=color, alpha=alpha)

        ax.set_xlabel('Time [days]')
        ax.set_ylabel('Number infected')

        mname = self.frame.model_name
        pop = self.frame.population
        ax.set_title(
            f"Infection curve - Model: {mname} - Population: {pop}")

        return ax


class ModelResultFrame(core.Frame):
    """Wrapper around the model results table..

    This class adds functionalities around the dataframe.

    The name of the model can be accesed as ``instance.modelname``.

    """
    plot_cls = ModelResultPlotter


@attr.s(frozen=True)
class InfectionCurve:
    """MArce documentame me siento sola.

    Parameters
    ----------

    population: int (default=600000)
        Population.
    N_init: int (default=10)
        Number of initial infections.
    R: float (default=1.2)
        Reproduction number.
    intervention_start: int (default=15)
        Start intervention days.
    intervention_end: int (default=25)
        End intervention days.
    intervention_decrease: float (default=70)
        Decrease in transmission for intervention, percentage (0-100)
        100 means total isolation.
    t_incubation: float (default=5.)
        Length of incubation period.
    t_infectiou: = (default=9.)
        Duration patient is infectious.
    t_death: float (default=32.)
        Time from end of incubation to death.
    mild_recovery: float (default=0.2)
        Recovery time for mild (not severnot severe) cases, days
        hospitalization rate (fraction).
    bed_stay: float (default=28.)
        Length of hospital stay, days.
    bed_rate: float (default=0.2)
        Hospitalization rate (fraction).
    bed_wait: int (default=5)
        Time from first synthoms to hospitalization (days).
    beta: float (default=1.236)
        SEIR Model beta ($\\beta$).
    sigma: float (default=1.1)
        SEIR Model sigma ($\\sigma$).
    gamma: float (default=1.1)
        SEIR Model gamma ($\\gamma$).

    References
    ----------

    “Stochastic SIR model with Python,” epirecipes. [Online].
     Available: https://tinyurl.com/y8zwvfk4. [Accessed: 09-May-2020].

    """

    population: int = attr.ib(default=600000)
    N_init: int = attr.ib(default=10)
    R: float = attr.ib(default=1.2)
    intervention_start: int = attr.ib(default=15)
    intervention_end: int = attr.ib(default=25)
    intervention_decrease: float = attr.ib(default=70)
    t_incubation: float = attr.ib(default=5.)
    t_infectious: float = attr.ib(default=9.)
    t_death: float = attr.ib(default=32.)
    mild_recovery: float = attr.ib(default=11.)
    bed_stay: float = attr.ib(default=28.)
    bed_rate: float = attr.ib(default=0.2)
    bed_wait: int = attr.ib(default=5)
    beta: float = attr.ib(default=1.236)
    sigma: float = attr.ib(default=1.1)
    gamma: float = attr.ib(default=1.1)

    def do_SIR(self, t_max=200, dt=1.):
        """This function implements a SIR model without vital dynamics
        under the assumption of a closed population.

        Recovered individuals become immune for ever.
        In this model exposed individuals become instantly infectious,
        i.e., there is no latency period like in the SEIR model.

        Parameters
        ----------
        t_max: int (default=200)
            Time range [days].
        dt: float (default=1.)
            Time step [days].

        Returns
        -------
           value: Time series for S, I and R

        """
        dt = float(dt)

        g = Graph()

        for node in ['I', 'C', 'R', 'H', 'B', 'U', 'D']:
            g.add_node(node, 0)

        g.set_node('I', self.N_init)

        # cumulative time series
        I = [g.get_node_value('I')]  # noqa Infected
        C = [g.get_node_value('C')]  # Confirmed
        R = [g.get_node_value('R')]  # Recovered

        ts = [0.]  # time series
        nms = ['prob', 'lag']

        # En este modelo todos los infectados se confirman a los 10
        # dias y se curan a los 20 dias de confirmados
        T_IC = int(self.t_incubation / dt)
        T_CR = 20
        f_IC = 1.
        f_CR = 1.

        g.add_edge('I', 'I', nms, [self.R, 0])
        g.add_edge('I', 'C', nms, [f_IC, T_IC])
        g.add_edge('C', 'R', nms, [f_CR, T_CR])

        t, time_steps = 0., 0
        while t < t_max:

            time_steps = time_steps + 1

            t = t + dt
            ts.append(t)

            # (( I ))
            prob_II = g.get_edge('I', 'I', 'prob')

            prob_IC = g.get_edge('I', 'C', 'prob')
            lag_IC = g.get_edge('I', 'C', 'lag')
            update_IC = I[-lag_IC] if lag_IC < len(I) else 0.

            n_I = (
                min(I[-1] + I[-1] * prob_II * dt, self.population) - # noqa
                update_IC * prob_IC * dt)
            n_I = max(n_I, 0)

            I.append(n_I)

            # (( C ))
            prob_CR = g.get_edge('C', 'R', 'prob')
            lag_CR = g.get_edge('C', 'R', 'lag')
            update_CR = C[-lag_CR] if lag_CR < len(C) else 0.

            n_C = (
                min(C[-1] + update_IC * prob_IC * dt, self.population) -  # noqa
                update_CR * prob_CR * dt)
            n_C = max(n_C, 0)
            C.append(n_C)

            # (( R ))
            # recuperados nuevos
            n_R = min(R[-1] + update_CR * prob_CR * dt, self.population)
            n_R = max(n_R, 0)
            R.append(n_R)

        df = pd.DataFrame(
            {'ts': ts, 'I': I, 'C': C, 'R': R}).set_index("ts")

        extra = attr.asdict(self)
        extra["model_name"] = "SIR"
        return ModelResultFrame(df=df, extra=extra)

    def do_SEIR(self, t_max=200, dt=1.):
        """This function implements a SEIR model without vital dynamics
        under the assumption of a closed population.
        Recovered individuals become immune for ever.
        ref.: https://www.idmod.org/docs/hiv/model-seir.html

        Parameters
        ----------
        t_max: int (default=200)
            Time range [days].
        dt: float (default=1.)
            Time step [days].

        Returns
        -------
           value: Time series for S, E, I and R


        """
        dt = float(dt)
        g = Graph()

        for node in ['S', 'E', 'I', 'R']:
            g.add_node(node, 0)

        g.set_node('S', self.population)
        g.set_node('E', 0)
        g.set_node('I', self.N_init)
        g.set_node('R', 0)

        # cumulative time series
        S = [g.get_node_value('S')]  # Susceptible
        E = [g.get_node_value('E')]  # Exposed
        I = [g.get_node_value('I')]  # noqa Infected
        R = [g.get_node_value('R')]  # Recovered

        ts = [0.]  # time series
        nms = ['prob', 'lag']

        g.add_edge('S', 'S', nms, [0.1, 2])
        g.add_edge('E', 'E', nms, [0.4, 21])
        g.add_edge('I', 'I', nms, [0.1, 2])

        g.add_edge('S', 'E', nms, [1.2, 1])
        g.add_edge('E', 'I', nms, [0.1, 14])  # [, tiempo de incubacion]
        g.add_edge('I', 'R', nms, [0.7, 2])  # [, tiempo de recuperacion]

        t, time_steps = 0., 0
        while t < t_max:

            time_steps = time_steps + 1

            t = t + dt
            ts.append(t)

            # (( S ))
            prob_SS = g.get_edge('S', 'S', 'prob')  # beta

            dS = - S[-1] * (I[-1] / self.population) * prob_SS

            # n_S = min(S[-1] + min(dS * dt, 0), self.population)
            n_S = S[-1] + dS * dt

            # (( E ))
            prob_EE = g.get_edge('E', 'E', 'prob')
            dE = - dS - prob_EE * E[-1]

            # n_E = min(E[-1] + max(dE * dt, 0), self.population)
            n_E = E[-1] + dE * dt

            # (( I ))
            prob_EI = g.get_edge('E', 'I', 'prob')
            lag_EI = g.get_edge('E', 'I', 'lag')
            update_EI = E[-lag_EI] if lag_EI < len(E) else 0.

            prob_IR = g.get_edge('I', 'R', 'prob')
            lag_IR = g.get_edge('I', 'R', 'lag')
            update_IR = I[-lag_IR] if lag_IR < len(I) else 0.

            prob_II = g.get_edge('I', 'I', 'prob')

            dI = prob_EI * update_EI - prob_IR * update_IR
            dI = -dI   # porque ????
            n_I = min(I[-1] + dI * dt, self.population)

            # (( R ))
            prob_II = g.get_edge('I', 'I', 'prob')
            dR = prob_II * I[-1]
            n_R = min(R[-1] + max(dR * dt, 0), self.population)

            S.append(n_S)
            E.append(n_E)
            I.append(n_I)
            R.append(n_R)

        df = pd.DataFrame(
            {'ts': ts, 'S': S, 'E': E, 'I': I, 'R': R}).set_index("ts")

        extra = attr.asdict(self)
        extra["model_name"] = "SEIR"
        return ModelResultFrame(df=df, extra=extra)

    def do_SEIRF(self, t_max=200, dt=1.):
        """Documentame MARCE

        Parameters
        ----------
        t_max: int (default=200)
            Time range [days].
        dt: float (default=1.)
            Time step [days].

        Returns
        -------
           value: Time series for S, E, I, R and F

        """
        dt = float(dt)
        g = Graph()

        for node in ['S', 'E', 'I', 'R', 'F']:
            g.add_node(node, 0)

        g.set_node('S', self.population)
        g.set_node('E', 0)
        g.set_node('I', self.N_init)
        g.set_node('R', 0)
        g.set_node('F', 0)

        # cumulative time series
        S = [g.get_node_value('S')]  # Susceptible
        E = [g.get_node_value('E')]  # Exposed
        I = [g.get_node_value('I')]  # noqa Infected
        R = [g.get_node_value('R')]  # Recovered
        F = [g.get_node_value('F')]  # Fatalities

        ts = [0.]  # time series
        nms = ['prob', 'lag']

        g.add_edge('S', 'E', nms, [0.2, 0])
        g.add_edge('E', 'E', nms, [0.1, 0])
        g.add_edge('E', 'I', nms, [0.7, 14])
        g.add_edge('I', 'I', nms, [1.2, 14])
        g.add_edge('I', 'R', nms, [0.98, 30])
        g.add_edge('I', 'F', nms, [0.02, 30])

        t, time_steps = 0., 0
        while t < t_max:

            time_steps = time_steps + 1

            t = t + dt
            ts.append(t)

            # (( S ))
            prob_SE = g.get_edge('S', 'E', 'prob')  # beta
            dS = - S[-1] * (I[-1] / self.population) * prob_SE
            n_S = S[-1] + dS * dt

            # (( E ))
            prob_EE = g.get_edge('E', 'E', 'prob')
            lag_EE = g.get_edge('E', 'E', 'lag')
            update_EE = E[-lag_EE] if lag_EE < len(E) else 0.

            dE = - dS - prob_EE * update_EE
            n_E = E[-1] + dE * dt

            # (( I ))
            prob_EI = g.get_edge('E', 'I', 'prob')
            lag_EI = g.get_edge('E', 'I', 'lag')
            update_EI = E[-lag_EI] if lag_EI < len(E) else 0.

            prob_II = g.get_edge('I', 'I', 'prob')
            lag_II = g.get_edge('I', 'I', 'lag')
            update_II = I[-lag_II] if lag_II < len(I) else 0.

            prob_IR = g.get_edge('I', 'R', 'prob')
            lag_IR = g.get_edge('I', 'R', 'lag')
            update_IR = I[-lag_IR] if lag_IR < len(I) else 0.

            prob_II = g.get_edge('I', 'I', 'prob')

            dI = (
                prob_EI * update_EI +  # noqa
                prob_II * update_II -  # noqa
                prob_IR * update_IR)
            n_I = min(I[-1] + dI * dt, self.population)

            # (( R ))
            prob_IF = g.get_edge('I', 'F', 'prob')
            lag_IF = g.get_edge('I', 'F', 'lag')
            update_IF = I[-lag_IF] if lag_IF < len(R) else 0.

            dR = prob_IR * update_IR - prob_IF * update_IF
            n_R = min(R[-1] + max(dR * dt, 0), self.population)

            # (( F ))
            n_F = min(I[-1] + max(dR * dt, 0), self.population)

            S.append(n_S)
            E.append(n_E)
            I.append(n_I)
            R.append(n_R)
            F.append(n_F)

        df = pd.DataFrame(
            {'ts': ts, 'S': S, 'E': E, 'I': I, 'R': R, 'F': F}).set_index("ts")

        extra = attr.asdict(self)
        extra["model_name"] = "SEIRF"
        return ModelResultFrame(df=df, extra=extra)


# =============================================================================
# FUNCTION
# =============================================================================

def load_infection_curve(**kwargs):
    """Return a new instance of infection curve."""
    # aca se va a leer los archivos remotos y se va a cargar
    # en InfectionCurve de alguna forma aun no establecida
    return InfectionCurve(**kwargs)
