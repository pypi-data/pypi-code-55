from rslib.gym_envs import RecEnvSrc
from rslib.gym_envs.RecSim import RecSim
import numpy as np
from functools import reduce

class L20RecSim(RecSim):
    def __init__(self, recEnvSrc: RecEnvSrc, model, modelfile, sess, steps=9, batch_size=None, reward_sqr=False, use_rule=False):
        RecSim.__init__(self, recEnvSrc, model, modelfile, steps, batch_size)
        self.sess = sess
        self.reward_sqr = reward_sqr
        self.use_rule = use_rule

        self.layers = np.zeros([self.steps, self.batch_size], dtype=int) if self.batch_size else np.zeros(self.steps, dtype=int)
        self.paytypes = np.zeros([self.steps, self.batch_size], dtype=int) if self.batch_size else np.zeros(self.steps, dtype=int)

    def _step(self, rawstate, action, info):
        """ Given an action and return for prior period, calculates costs, navs,
            etc and returns the reward and a  summary of the day's activity. """

        new_rawstate = self.recEnvSrc.get_new_user_rawstate(rawstate, info)
        self.actions[self.step] = action

        self.layers[self.step] = np.array([self.recEnvSrc.action_dict[a]['layer'] for a in action])
        self.paytypes[self.step] = np.array([self.recEnvSrc.action_dict[a]['paytype'] for a in action])

        info['actions'] = self.actions
        info['layers'] = self.layers
        info['paytypes'] = self.paytypes

        # region 业务规则介绍
        '''
        业务规则：
            价格 1
            物品在对应层 1
            没有相同物品 1
            第一层必有铜钱或姻缘 1
            第二层必有红尘或红豆，且必有铜钱或姻缘 1
            第三层必有红豆，且必有铜钱或姻缘 1
            桃花不能同时出现1个以上 1
            桃花限制出现
            ssr不能同时出现1个以上 1
            ssr，两种限制方法：1 以一定概率添加惩罚
                               2 price 乘以一个定值
        '''
        # endregion

        # region 计算 业务规则
        self.t1 = self.recEnvSrc.t1_item
        self.t12 = self.recEnvSrc.t1_item | self.recEnvSrc.t2_item
        self.t34 = self.recEnvSrc.t3_item | self.recEnvSrc.t4_item
        self.t234 = self.recEnvSrc.t2_item | self.recEnvSrc.t3_item | self.recEnvSrc.t4_item
        self.ssr = self.recEnvSrc.l1_ssr_item | self.recEnvSrc.l2_ssr_item | self.recEnvSrc.l3_ssr_item

        layer_unique_check = [[1] * 3 for _ in range(self.batch_size)]
        layer_paytype_check = [[1] * 3 for _ in range(self.batch_size)]
        layer_item_in_layer_check = [[1] * 3 for _ in range(self.batch_size)]

        item_unique_check = [[1] * 9 for _ in range(self.batch_size)]
        item_paytype_check = [[1] * 9 for _ in range(self.batch_size)]
        item_item_in_layer_check = [[1] * 9 for _ in range(self.batch_size)]

        unique_check = [1 for _ in range(self.batch_size)]
        paytype_check = [1 for _ in range(self.batch_size)]
        item_in_layer_check = [1 for _ in range(self.batch_size)]
        taohua_check = [1 for _ in range(self.batch_size)]
        ssr_check = [1 for _ in range(self.batch_size)]

        # taohua_si

        step = self.step + 1
        prices = [[0] * 9 for _ in range(self.batch_size)]
        for batch_i in range(self.batch_size):
            #  region item-wise 业务规则, 目前主要是 paytype 的规则
            if step == 1:
                item = self.actions[step - 1, batch_i]
                item_paytype_check[batch_i][0] = 1 if item in self.t34 else 0
            elif step == 2:
                item = self.actions[step - 1, batch_i]
                item_paytype_check[batch_i][1] = 1 if item in self.t234 else 0
            elif step == 3:
                item_paytype_check[batch_i][2] = 1
            elif step == 4:
                item = self.actions[step - 1, batch_i]
                item_paytype_check[batch_i][3] = 1 if item in self.t12 else 0
            elif step == 5:
                item = self.actions[step - 1, batch_i]
                item_paytype_check[batch_i][4] = 1 if item in self.t34 else 0
            elif step == 6:
                item_paytype_check[batch_i][5] = 1
            elif step == 7:
                item = self.actions[step - 1, batch_i]
                item_paytype_check[batch_i][6] = 1 if item in self.t1 else 0
            elif step == 8:
                item = self.actions[step - 1, batch_i]
                item_paytype_check[batch_i][7] = 1 if item in self.t34 else 0
            elif step == 9:
                item_paytype_check[batch_i][8] = 1
            else:
                raise Exception("Invalid step!")
            # endregion

            # region layer-wise 业务规则
            item_in_layer123 = set(self.actions[0:step, batch_i])
            if step <= 3:
                item_in_layer1 = set(self.actions[0:step, batch_i])

                layer_unique_check[batch_i][0] = 1 if len(item_in_layer1) == step else 0
                layer_paytype_check[batch_i][0] = 1 if step < 3 or item_in_layer1 & self.t34 else 0
                layer_item_in_layer_check[batch_i][0] = 1 if len(item_in_layer1 & self.recEnvSrc.l1_item) == step else 0

            elif step <= 6:
                item_in_layer1 = set(self.actions[0:3, batch_i])
                item_in_layer2 = set(self.actions[3:step, batch_i])

                layer_unique_check[batch_i][0] = 1 if len(item_in_layer1) == 3 else 0
                layer_paytype_check[batch_i][0] = 1 if item_in_layer1 & self.t34 else 0
                layer_item_in_layer_check[batch_i][0] = 1 if len(item_in_layer1 & self.recEnvSrc.l1_item) == 3 else 0

                layer_unique_check[batch_i][1] = 1 if len(item_in_layer2) == step - 3 else 0
                layer_paytype_check[batch_i][1] = 1 if step == 4 or (step == 5 and (item_in_layer2 & self.t34 or item_in_layer2 & self.t12)) or \
                                                       (step == 6 and (item_in_layer2 & self.t34 and item_in_layer2 & self.t12)) else 0
                layer_item_in_layer_check[batch_i][1] = 1 if len(item_in_layer2 & self.recEnvSrc.l2_item) == step - 3 else 0

            else:
                item_in_layer1 = set(self.actions[0:3, batch_i])
                item_in_layer2 = set(self.actions[3:6, batch_i])
                item_in_layer3 = set(self.actions[6:step, batch_i])

                layer_unique_check[batch_i][0] = 1 if len(item_in_layer1) == 3 else 0
                layer_paytype_check[batch_i][0] = 1 if item_in_layer1 & self.t34 else 0
                layer_item_in_layer_check[batch_i][0] = 1 if len(item_in_layer1 & self.recEnvSrc.l1_item) == 3 else 0

                layer_unique_check[batch_i][1] = 1 if len(item_in_layer2) == 3 else 0
                layer_paytype_check[batch_i][1] = 1 if item_in_layer2 & self.t34 and item_in_layer2 & self.t12 else 0
                layer_item_in_layer_check[batch_i][1] = 1 if len(item_in_layer2 & self.recEnvSrc.l2_item) == 3 else 0

                layer_unique_check[batch_i][2] = 1 if len(item_in_layer3) == step - 6 else 0
                layer_paytype_check[batch_i][2] = 1 if step == 7 or (step == 8 and (item_in_layer3 & self.t34 or item_in_layer3 & self.t1)) or \
                                                       (step == 9 and (item_in_layer3 & self.t34 and item_in_layer3 & self.t1)) else 0
                layer_item_in_layer_check[batch_i][2] = 1 if len(item_in_layer3 & self.recEnvSrc.l3_item) == step - 6 else 0

            # endregion

            # region session-wise 业务规则
            taohua_check[batch_i] = 1 if len(item_in_layer123 & self.recEnvSrc.taohua_item) <= 1 else 0
            ssr_check[batch_i] = 1 if len(item_in_layer123 & self.ssr) <= 1 else 0
            # taohua_check[batch_i] = 1
            # ssr_check[batch_i] = 1
            # endregion

            # region 业务规则整合
            unique_check[batch_i] = reduce(lambda x, y: x & y, layer_unique_check[batch_i], 1)
            # paytype_check[batch_i] = layer_paytype_check[batch_i][0] & layer_paytype_check[batch_i][1] & layer_paytype_check[batch_i][2]
            paytype_check[batch_i] = reduce(lambda x, y: x & y, layer_paytype_check[batch_i], 1) & reduce(lambda x, y: x & y, item_paytype_check[batch_i], 1)
            item_in_layer_check[batch_i] = reduce(lambda x, y: x & y, layer_item_in_layer_check[batch_i], 1)
            # endregion

            # region 在最后一步获取已选物品的价格
            if step == self.steps:
                price = [self.recEnvSrc.get_item_price(i) if i in self.recEnvSrc.available_item else -1 for i in self.actions[0:9, batch_i]]
                if self.reward_sqr:
                    price = np.sqrt(price)
                prices[batch_i] = price
            # endregion
        # endregion
        a = 1

        # region 计算reward
        rewards = [[] for _ in range(self.batch_size)]
        reward = [0 for _ in range(self.batch_size)]
        done = [0 for _ in range(self.batch_size)]

        if step < self.steps:
            for batch_i in range(self.batch_size):
                if self.use_rule:
                    check = unique_check[batch_i] and paytype_check[batch_i] and item_in_layer_check[batch_i] and taohua_check[batch_i] and ssr_check[batch_i] \
                            and (self.step == 0 or not self.dones[self.step - 1, batch_i])
                else:
                    check = unique_check[batch_i] and item_in_layer_check[batch_i] \
                            and (self.step == 0 or not self.dones[self.step - 1, batch_i])
                # if check:
                if True:
                    reward[batch_i] = 0.1
                    done[batch_i] = 0
                elif not paytype_check[batch_i]:
                    reward[batch_i] = -0.11
                    done[batch_i] = 1
                # elif not item_in_layer_check[batch_i] or not unique_check[batch_i]:
                #     reward[batch_i] = -0.11
                #     done[batch_i] = 1
            #     elif not paytype_check[batch_i] and self.use_rule:
            #         reward[batch_i] = -0.12
            #         done[batch_i] = 1
            #     elif (not taohua_check[batch_i] or not ssr_check[batch_i]) and self.use_rule:
            #         reward[batch_i] = -0.13
            #         done[batch_i] = 1
            #     else:
            #         reward[batch_i] = -0.14
            #         done[batch_i] = 1
            #
            # if len([x for x in info['actions'] if x>0])>3:
            #     print('actions:' + str(info['actions']))
            #     print('rewards:' + str(rewards))
            #     print('reward:' + str(reward))

        else:
            model = self.model
            # print('actions' + str(info['actions']))
            # region 获得监督模型的 feature
            raw_feats = []
            for item in self.actions[0:3]:
                info['pred_items'] = np.concatenate((self.actions[0:0], [item]))
                raw_feat = self.recEnvSrc.get_new_user_rawstate(rawstate, info)
                raw_feats.extend(raw_feat)

            for item in self.actions[3:6]:
                info['pred_items'] = np.concatenate((self.actions[0:3], [item]))
                raw_feat = self.recEnvSrc.get_new_user_rawstate(rawstate, info)
                raw_feats.extend(raw_feat)

            for item in self.actions[6:9]:
                info['pred_items'] = np.concatenate((self.actions[0:6], [item]))
                raw_feat = self.recEnvSrc.get_new_user_rawstate(rawstate, info)
                raw_feats.extend(raw_feat)

            info['pred_items'] = self.actions[0:3]
            raw_feat = self.recEnvSrc.get_new_user_rawstate(rawstate, info)
            raw_feats.extend(raw_feat)

            info['pred_items'] = self.actions[0:6]
            raw_feat = self.recEnvSrc.get_new_user_rawstate(rawstate, info)
            raw_feats.extend(raw_feat)
            # endregion

            # region 计算 ctr
            feat = self.recEnvSrc.rawstate_to_state(raw_feats)
            ctr = self.predict_all(model, feat, self.sess)
            ctr = np.reshape(ctr, [11, self.batch_size])
            self.probs = ctr
            # endregion

            for batch_i in range(self.batch_size):
                rewards[batch_i] += [ctr[i][batch_i] * prices[batch_i][i] for i in range(0, 3)]
                rewards[batch_i] += [ctr[i][batch_i] * prices[batch_i][i] for i in range(3, 6)]
                rewards[batch_i] += [ctr[i][batch_i] * prices[batch_i][i] for i in range(6, 9)]
                # rewards[batch_i] += [ctr[9][batch_i] * ctr[i][batch_i] * prices[batch_i][i] for i in range(3, 6)]
                # rewards[batch_i] += [ctr[10][batch_i] * ctr[i][batch_i] * prices[batch_i][i] for i in range(6, 9)]

                if self.use_rule:
                    check = unique_check[batch_i] and paytype_check[batch_i] and item_in_layer_check[batch_i] and taohua_check[batch_i] and ssr_check[batch_i] \
                            and (self.step == 0 or not self.dones[self.step - 1, batch_i])
                else:
                    check = unique_check[batch_i] and item_in_layer_check[batch_i] \
                            and (self.step == 0 or not self.dones[self.step - 1, batch_i])

                # if check:
                if True:
                    reward[batch_i] = sum(rewards[batch_i])
                    done[batch_i] = 1
                elif not item_in_layer_check[batch_i] or not unique_check[batch_i]:
                    reward[batch_i] = -0.11
                    done[batch_i] = 1
                elif not paytype_check[batch_i] and self.use_rule:
                    reward[batch_i] = -0.12
                    done[batch_i] = 1
                elif (not taohua_check[batch_i] or not ssr_check[batch_i]) and self.use_rule:
                    reward[batch_i] = -0.13
                    done[batch_i] = 1
                else:
                    reward[batch_i] = -0.14
                    done[batch_i] = 1

            # print('actions:' + str(info['actions']))
            # print('rewards:' + str(rewards))
            # print('reward:' + str(reward))

        # endregion

        self.dones[self.step] = done
        # print('actions:' + str(info['actions'][:, 0]))
        # print('actions:' + str(info['actions']))
        # print('rewards:' + str(rewards))
        # print('reward:' + str(reward))

        info['reward'] = reward
        info['rewards'] = rewards
        info['gmv'] = self.gmv[self.step]
        info['probs'] = self.probs
        # info['len'] = np.sum(self.dones[:self.step + 1], axis=0)
        # print(info['len'])

        self.step += 1
        return new_rawstate, reward, done, info