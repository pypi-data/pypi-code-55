# File & Folder setup
from AoE2ScenarioParser.aoe2_scenario import AoE2Scenario
from AoE2ScenarioParser.datasets.conditions import Condition
from AoE2ScenarioParser.datasets.effects import Effect
from AoE2ScenarioParser.datasets.players import Player
from AoE2ScenarioParser.datasets.trigger_lists import DiplomacyState, Operator, ButtonLocation, PanelLocation, \
    TimeUnit, VisibilityState, DifficultyLevel, TechnologyState, Comparison, ObjectAttribute, Attribute

scenario_folder = "C:/Users/Kerwin Sneijders/Games/Age of Empires 2 DE/76561198140740017/resources/_common/scenario/"
read_file = scenario_folder + "AllEffectConditionLists.aoe2scenario"
write_to_file = scenario_folder + "AllEffectConditionLists2.aoe2scenario"

scenario = AoE2Scenario(read_file)

trigger_manager = scenario.object_manager.trigger_manager

trigger = trigger_manager.add_trigger("Inform Betrayal!")
condition = trigger.add_condition(Condition.DIPLOMACY_STATE)
condition.amount_or_quantity = DiplomacyState.ALLY
condition.player = Player.TWO
condition.target_player = Player.THREE

effect = trigger.add_effect(Effect.DISPLAY_INSTRUCTIONS)
effect.player_source = Player.ONE
effect.message = "Spy: Your ally has betrayed you! He allied the enemy!"
effect.instruction_panel_position = PanelLocation.CENTER
effect.display_time = 10


scenario.write_to_file(write_to_file)



