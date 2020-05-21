import pandas as pd
from ...data.struct import AssetWeight, AssetPrice, AssetPosition, AssetValue
from ...data.struct import TAAParam, FAParam, FundWeightItem, FundWeight, TaaTunerParam
from . import Helper


class SAAHelper(Helper):

    def __init__(self):
        pass

    def setup(self, saa: AssetWeight):
        self.saa = saa

    def on_price(self, dt, asset_price: AssetPrice):
        cur_saa = self.saa.copy()
        for k, v in asset_price.__dict__.items():
            if asset_price.isnan(v):
                cur_saa.__dict__[k] = 0
        cur_saa.rebalance()
        return cur_saa


class TAAStatusMode:
    NORMAL = 'normal'
    IN_LOW = 'low'
    IN_HIGH = 'high'

class TAAHelper(Helper):

    # 1. let each asset use same taa param: set taa_params and taa_param_details == None
    # 2. let some asset use special taa param and others default: set taa_params and make special params in taa_param_details
    # 3. stop some asset from using taa: make taa_param_details[index_id] = None
    # 4. only asset in taa_param_details has taa: make taa_params = None
    def __init__(self, taa_params: TAAParam=None, taa_param_details: dict=None):
        self.params = taa_params or TAAParam()
        self.param_details = taa_param_details or {}
        self.tactic_status = {}
        self.tactic_history = {}

    def on_price(self, dt, asset_price: AssetPrice, cur_saa: AssetWeight, asset_pct: pd.DataFrame):
        taa = cur_saa.copy()
        taa_effected = False
        mode_changed = False
        tactic_dt = {}
        for index_id, target_w in taa.__dict__.items():
            cur_params = self.param_details.get(index_id, self.params)
            if target_w == 0 or cur_params is None:
                continue
            if index_id in TaaTunerParam.POOL:
                #assert index_id in asset_pct.index, f'{index_id} pct not exsit'
                # 无估值跳过  大部分资产08年之前没有估值百分位
                if index_id not in asset_pct.index:
                    continue
                val_pct = asset_pct.loc[index_id, TaaTunerParam.POOL[index_id]]
                cur_mode = self.tactic_status.get(index_id, TAAStatusMode.NORMAL)
                new_mode = TAAStatusMode.NORMAL
                tactic_w = target_w

                if cur_mode == TAAStatusMode.NORMAL:

                    if val_pct >= cur_params.HighThreshold:
                        tactic_w = max(target_w - cur_params.HighMinus, 0)
                        new_mode = TAAStatusMode.IN_HIGH
                    elif val_pct <= cur_params.LowThreshold:
                        tactic_w = min(target_w + cur_params.LowPlus, 1)
                        new_mode = TAAStatusMode.IN_LOW
                    
                elif cur_mode == TAAStatusMode.IN_LOW:

                    if val_pct < cur_params.LowStop:
                        tactic_w = min(target_w + cur_params.LowPlus, 1)
                        new_mode = TAAStatusMode.IN_LOW

                elif cur_mode == TAAStatusMode.IN_HIGH:

                    if val_pct > cur_params.HighStop:
                        tactic_w = max(target_w - cur_params.HighMinus, 0)
                        new_mode = TAAStatusMode.IN_HIGH
                else:
                    assert False, 'should not be here!'

                self.tactic_status[index_id] = new_mode
                if new_mode != TAAStatusMode.NORMAL:
                    taa.__dict__[index_id] = tactic_w

                mode_changed = mode_changed or new_mode != cur_mode
                taa_effected = taa_effected or new_mode != TAAStatusMode.NORMAL
                tactic_dt[index_id] = new_mode
        self.tactic_history[dt] = tactic_dt

        self.rebalance_taa(taa, self.params.TuneCash)
        if taa_effected:
            #print(f'taa: {dt} (mode){mode_changed} (taa){taa_effected} (saa){cur_saa} (taa){taa}')
            pass
        return taa

    def rebalance_taa(self, asset_weight:AssetWeight, to_tune_cash:bool):
        asset_weight = asset_weight.__dict__
        _sum = 0.0
        for k, v in asset_weight.items():
            assert round(v,8) >= 0, f'{k} has negative value'
            _sum += v
        assert _sum > 0, 'param sum value must be positive'
        # 验证过的非现金类资产rebalance
        if not to_tune_cash:
            _sum = (_sum - asset_weight['cash']) / (1 - asset_weight['cash'])
        # 不调整cash
        for k, v in asset_weight.items():
            if k == 'cash' and (not to_tune_cash):
                continue
            asset_weight[k] /= _sum


class FAHelper(Helper):
    
    def __init__(self, fa_params: FAParam=None):
        self.params = fa_params or FAParam()

    def on_price(self, dt, cur_asset_allocation: AssetWeight, cur_fund_score: dict):

        res = FundWeight()
        for index_id in cur_asset_allocation.__dict__.keys():
            if index_id == 'cash':
                continue
            asset_wgt = cur_asset_allocation.__dict__[index_id]
            if asset_wgt > 0:
                _scores = sorted(cur_fund_score.get(index_id, {}).items(), key=lambda item: item[1], reverse=True)
                local_max_fund_num = max(round(asset_wgt / 0.05, 0), 1) # for a single asset, for each 5% wgt it gots, they should take 1 extra fund
                fund_weights = {}
                fund_tot_weight = 0
                fund_selected_num = 0
                for i in range(0, len(_scores)):
                    fund_id, score_as_weight = _scores[i]
                    # 最多不超过 MaxFundNumUnderAsset 个基金
                    fund_weights[fund_id] = score_as_weight
                    fund_tot_weight += score_as_weight
                    fund_selected_num += 1
                    if fund_selected_num >= self.params.MaxFundNumUnderAsset or fund_selected_num >= local_max_fund_num:
                        break
                assert fund_selected_num > 0, f'no fund is selected in {index_id}'
                assert fund_tot_weight > 0, f'fund total weigth is not positive: {fund_tot_weight}'
                
                for fund_id, raw_weight in fund_weights.items():
                    fund_wgt_in_asset = raw_weight / fund_tot_weight
                    fund_weight_item = FundWeightItem(fund_id=fund_id, index_id=index_id, asset_wgt=asset_wgt, fund_wgt_in_asset=fund_wgt_in_asset)
                    res.add(fund_weight_item)
        return res