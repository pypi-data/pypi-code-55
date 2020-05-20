from rslib.gym_envs.RecEnvSrc import RecEnvSrc

class L20RecEnvSrc(RecEnvSrc):
    def __init__(self, config, statefile, actionfile, batch_size=None, reward_type='ctr_price'):
        RecEnvSrc.__init__(self, config, statefile, actionfile, batch_size=batch_size, reward_type=reward_type)


    def get_user_rawstate(self, role_ids):
        '''

        :param role_ids:
        :return:
        '''
        rawstates = []
        for role_id in role_ids:
            rawstate = self.state_dict[str(role_id)]
            seq_feat = rawstate.split('@')[2].split(';')
            seq_feat_init = ';'.join([seq_feat[0], seq_feat[1], '0:0', '0:0'])
            rawstate = '@'.join(rawstate.split('@')[:2] + [seq_feat_init] + rawstate.split('@')[3:])

            rawstates.append(rawstate)
        return rawstates

    def get_new_user_rawstate(self, rawstates, info):
        '''

        :param rawstates:
        :param info:
        :return:
        '''
        # 只有最后一步才改变状态，才有奖励
        # assert type(rawstates) == type('')

        if 'actions' in info and info['actions'][-1][0] >= 0:
            new_rawstates = []
            for i, rawstate in enumerate(rawstates):
                seq_feat = rawstate.split('@')[2].split(';')
                expose_feat = ', '.join([str(x) + ':1' for x in info['actions'][:, i]])
                predict_feat = ', '.join([str(x) + ':1' for x in info['pred_items'][:, i]])
                seq_feat_actions = ';'.join([seq_feat[0], seq_feat[1], expose_feat, predict_feat])
                new_rawstate = '@'.join(rawstate.split('@')[:2] + [seq_feat_actions] + rawstate.split('@')[3:])
                new_rawstates.append(new_rawstate)
            return new_rawstates
        else:
            return rawstates
