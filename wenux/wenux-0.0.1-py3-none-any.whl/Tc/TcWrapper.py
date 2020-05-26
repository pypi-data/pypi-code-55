import logging
import datetime
import time

from Utils.Subprocess import call, check_call
from Tc.Tbf import TbfCollection, Tbf
from Tc.Filter import Filter, TcFilter
from Tc.Netem import NetemCollection, Duplicate, Delay, Loss, Reorder, Corrupt


class TcWrapper(object):
    def __init__(self, **kwargs):
        for key in kwargs:
            setattr(self, key, kwargs[key])
        self.real_nic = "ifb1" if self.ingress else self.nic

    def tbf(self, operation):
        tbf = Tbf(self.limit,
                  self.burst,
                  self.latency)

        tbf_collection = TbfCollection(self.real_nic)
        tbf_collection.append(tbf)
        tbf_collection.apply_cmd(operation=operation)

    def netem(self, operation):
        loss = Loss(self.loss_ratio,
                    self.loss_corr)

        dupl = Duplicate(self.dupl_ratio,
                         self.dupl_corr)

        delay = Delay(self.delay,
                      self.jitter,
                      self.delay_jitter_corr)

        reorder = Reorder(self.reorder_ratio,
                          self.reorder_corr)

        corrupt = Corrupt(self.corrupt_ratio)

        netem_collection = NetemCollection(self.real_nic)
        netem_collection.extend([loss, dupl, delay, reorder, corrupt])
        netem_collection.apply_cmd(operation=operation)

    # TODO - ingress, bidirectional, calls elsewhere
    def initialize(self):
        logging.info("Initializing and cleaning up previous configuration.")

        if self.ingress:
            check_call("modprobe ifb")
            check_call(f"ip link set dev {self.nic} up")
            call(f"tc qdisc del dev {self.real_nic} ingress ")
            check_call(f"tc qdisc replace dev {self.real_nic} ingress")
            check_call(f"tc filter replace dev {self.real_nic} parent ffff: protocol "
                       f"ip prio 1u 32 match u32 0 0 flowid 1:1 action mirred egress "
                       f"redirect dev {self.nic}")

        call(f"tc qdisc del root dev {self.nic} ")
        check_call(f"tc qdisc add dev {self.nic} root handle 1: prio")

        exclude_filters, exclude_filters_ipv6 = Filter.generate_filters(self.exclude)

        TcFilter(exclude_filters, self.nic, "ip", "exclude")
        TcFilter(exclude_filters, self.nic, "ipv6", "exclude")

        include_filters, include_filters_ipv6 = Filter.generate_filters(self.include)

        TcFilter(include_filters, self.nic, "ip", "include")
        TcFilter(include_filters_ipv6, self.nic, "ipv6", "include")

    def teardown(self):
        if self.ingress:
            call(f"tc filter del dev {self.real_nic} parent ffff: protocol ip prio 1")
            call(f"tc qdisc del dev {self.real_nic} ingress")
            call("ip link set dev ifb0 down")

        call(f"tc qdisc del root dev {self.nic}")
        logging.info("Network impairment emulation teardown complete.")
