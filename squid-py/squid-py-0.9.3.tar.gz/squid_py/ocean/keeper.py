import logging

from eth_utils import add_0x_prefix
from ocean_keeper import Keeper
from ocean_keeper.event_filter import EventFilter
from ocean_keeper.web3_provider import Web3Provider


class SquidKeeper(Keeper):

    @staticmethod
    def get_instance(contract_names=None):
        return SquidKeeper(contract_names)

    def get_agreement_template_id(self, service_type):
        template_name = self.template_manager.SERVICE_TO_TEMPLATE_NAME[service_type]
        template_id = self.template_manager.create_template_id(template_name)
        return template_id

    def get_agreement_type(self, template_id):
        for _type in self.template_manager.SERVICE_TO_TEMPLATE_NAME.keys():
            if template_id == self.get_agreement_template_id(_type):
                return _type

        return None

    def _get_agreement_actor_event(self, agreement_id, from_block=0, to_block='latest'):
        _filter = {'agreementId': Web3Provider.get_web3().toBytes(hexstr=agreement_id)}

        event_filter = EventFilter(
            self.agreement_manager.AGREEMENT_ACTOR_ADDED_EVENT,
            self.agreement_manager._get_contract_agreement_actor_added_event(),
            _filter,
            from_block=from_block,
            to_block=to_block
        )
        event_filter.set_poll_interval(0.5)
        return event_filter

    def get_agreement_consumer(self, agreement_id):
        event_logs = self._get_agreement_actor_event(agreement_id).get_all_entries()
        if not event_logs:
            return False

        agreement_values = self.agreement_manager.get_agreement(agreement_id)
        template_mgr = self.template_manager
        template = self.template_manager.get_template(agreement_values.template_id)
        actor_type_to_id = {template_mgr.get_template_actor_type_value(_id): _id for _id in template.actor_type_ids}
        consumer_actor_type_id = actor_type_to_id['consumer']
        for event in event_logs:
            if add_0x_prefix(event.args.actorType.hex()) == consumer_actor_type_id:
                return event.args.actor

        return None

    def get_condition_name_by_address(self, address):
        """Return the condition name for a given address."""
        if self.lock_reward_condition.address == address:
            return 'lockReward'
        elif self.access_secret_store_condition.address == address:
            return 'accessSecretStore'
        elif self.compute_execution_condition.address == address:
            return 'computeExecution'
        elif self.escrow_reward_condition.address == address:
            return 'escrowReward'
        else:
            logging.error(f'The current address {address} is not a condition address')
