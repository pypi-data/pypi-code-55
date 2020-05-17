"""Defines the feature selection process.

"""


from conML.shared.logger import SelectionInfo, WinnerSelectionInfo


class WinnerSelector:
    def determine_winner(self, reliability_dict, ml_models):
        """Determine the winner among all pragmatic machine learning models.

        Args:
            reliability_dict (dict): Map reliability to list of models.
            ml_models (list): Supervised machine learnign models.

        Returns:
            tuple:
                Logging Info and PragmaticMachineLearningModel.

        """
        if not reliability_dict:
            return (
                WinnerSelectionInfo(WinnerSelectionInfo.State.FAILED),
                None
            )

        reliability_winner = self.models_with_the_biggest_reliability(reliability_dict)
        domain_winner = self.models_with_the_smallest_domain(reliability_winner)
        accuracy_winner = self.models_with_the_biggest_accuracy(domain_winner)
        priority_winner = self.model_with_highest_priority_winner(
            accuracy_winner, ml_models
        )

        return (
            WinnerSelectionInfo(
                WinnerSelectionInfo.State.SELECTED,
                priority_winner.uid,
                priority_winner.subject,
                priority_winner.accuracy,
                priority_winner.reliability
            ),
            priority_winner
        )

    def models_with_the_biggest_reliability(self, reliability_dict):
        """Select models with the biggest reliability.

        Args:
            reliability_dict (dict): Map reliability to list of models.

        Returns:
            List:
                Pragmatic machine learning models with the biggest reliability.

        """
        biggest_reliabllity = max(reliability_dict.keys())
        winners = reliability_dict[biggest_reliabllity]
        return winners

    def models_with_the_smallest_domain(self, winners):
        """Select models with the smalles feature set.

        Args:
            winners (list): List of pragmatic machine learning models.

        Returns:
            list:
                Pragmatic machine learning models with the smallest features set.

        """
        max_domain_length = float("inf")
        winner_group = []

        for model in winners:
            if len(model.learnblock_features) < max_domain_length:
                max_domain_length = len(model.learnblock_features)

        for model in winners:
            if len(model.learnblock_features) == max_domain_length:
                winner_group.append(model)

        return winner_group

    def models_with_the_biggest_accuracy(self, winners):
        """Select the pragmatic machine learning models with the highest accuracy.

        Args:
            winners (list): List of pragmatic machine learning models.

        Returns:
            dict:
                Map of subject (abbreviation) to pragmatic machine learning model
                with the highest accuracy.

        """
        winner_accuracy = max([m.accuracy for m in winners])
        return {m.subject: m for m in winners if m.accuracy == winner_accuracy}

    def model_with_highest_priority_winner(self, winners, ml_models):
        """Select the pragmatic machine learning model with the biggest priority.

        Args:
            winners (dict): Map subject (abbreviation) to model.
            ml_models (list): Supervised machine learnign models.

        Returns:
            PragmaticMachineLearningModel:
                Model with the highest priority accoring the order of ml_models.

        """
        winner_subjects = set(winners.keys())

        if len(winners) > 1:
            for m in ml_models:
                if m.subject in winner_subjects:
                    return winners[m.subject]

        return winners.popitem()[1]


class FeatureSelector:
    """Responsible for selecting a sub set of features.

    Args:
        filter_method (MachineLearningModel): Encapsulates filter methods.
        embedded_method (MachineLearningModel): Encapsulates embed methods.
        settings (FeatureSelectionSettings):
            Controlls behavior of the feature selection.

    """
    def __init__(self, filter_method, embedded_method, settings):
        self.filter_method = filter_method
        self.embedded_method = embedded_method
        self.settings = settings

    def __str__(self):
        return "\n".join([
                "{:20}: {}".format("Filter Method", str(self.filter_method)),
                "{:20}: {}".format("Embedded Method", str(self.embedded_method)),
                str(self.settings)
            ]
        )

    def __repr__(self):
        return ", ".join([
            "{}={}".format("Filter Method", str(self.filter_method)),
            "{}={}".format("Embedded Method", str(self.embedded_method)),
            repr(self.settings)
            ]
        )

    def select(self, lb):
        """Try sub selecting the feature set of a learnblock.

        Args:
            lb (PandasBlock): Processing learnblock.

        Returns:
            tuple:
                Logging info and if selection process succeded the reduced
                learnblock else None.

        """
        while 1:
            if self.reduce_constraint(lb):
                past_n_feature = lb.n_columns(effective=True)
                self.reduce(lb)
                if self.none_reducible_valid_learnblock(past_n_feature, lb):
                    return (
                        SelectionInfo(SelectionInfo.State.REDUCIBLE, lb),
                        lb
                    )

                elif self.none_reducible_invalid_learnblock(past_n_feature, lb):
                    return (
                        SelectionInfo(SelectionInfo.State.NON_REDUCIBLE, lb),
                        None
                    )

            else:
                return SelectionInfo(SelectionInfo.State.REDUCIBLE, lb), lb

    def reduce(self, learnblock):
        """Reduce features set of the given learnblock.

        Args:
            learnblock (PandasBlock): Processing learnblock.

        """
        if self._filter_method_criteria(learnblock.n_columns(effective=True),
                                        learnblock.n_rows()):
            remove_features = self.filtering(learnblock)
            learnblock.drop_columns(remove_features, by_index=True)

        else:
            remove_features = self.embedding(learnblock)
            learnblock.drop_columns(remove_features, by_index=True)

    def reduce_constraint(self, lb):
        """Check if the feature set should be reduced.

        Args:
            lb (PandasBlock): Processing learnblock.

        Returns:
            bool:
                True if the learnblock should be further reduced.

        """
        return (
            self._to_many_features(lb.n_columns(effective=True)) or
            self.settings.max_model_reduction and not
            lb.n_columns(effective=True) == 2
        )

    def none_reducible_valid_learnblock(self, past_n_features, lb):
        """Check if the learnblock cannot be further reduced but has
        the correct number of features.

        Args:
            past_n_features (int): Number of features before feature selection.
            lb (PandasBlock): Learnblock after feature selection.

        Returns:
            bool:
                True, learnblock cannot be further reduced and has to many
                features.

        """
        return (
            past_n_features == lb.n_columns(effective=True) and not
            self._to_many_features(lb.n_columns(effective=True))
        )

    def none_reducible_invalid_learnblock(self, past_n_features, lb):
        """Check if the learnblock cannot be further reduced and has
        still to many features.

        Args:
            past_n_features (int): Number of features before feature selection.
            lb (PandasBlock): Learnblock after feature selection.

        Returns:
            bool:
                True, learnblock cannot be further reduced and has to many
                features.

        """
        return (
            past_n_features == lb.n_columns(effective=True) and
            self._to_many_features(lb.n_columns(effective=True))
        )

    def filtering(self, learnblock):
        """Reduce feature number with embedding methods.

        Args:
            learnblock (PandasBlock): Learnblock.

        Returns:
            PandasBlock:
                PandasBlock after feature reduction.

        """
        self.filter_method.train(learnblock)
        return self.filter_method.reduce(learnblock)

    def embedding(self, learnblock):
        """Reduce features number with embedding methods.

        Args:
            learnblock (PandasBlock): Learnblock.

        Returns:
            PandasBlock:
                PandasBlock after feature reduction.

        """
        self.embedded_method.train(learnblock)
        return self.embedded_method.reduce(learnblock)

    def _to_many_features(self, learn_cols):
        """Check if learnblock contains to many features.

        Args:
            learn_cols (int): Number of learnblock features.

        Returns:
            bool:
                Number of features exceeds the allowed minimum number.

        """
        return learn_cols > self.settings.max_features

    def _filter_method_criteria(self, learn_cols, samples_count):
        """Check if the filter method criteria is fullfilled.

        Args:
            learn_cols (int): Number of features of processing learnblock.
            samples_count (int): number of samples of processing learnblock.

        Returns:
            bool:
                Number of features or number of samples exceeding filter method
                criteria.

        """
        return (
            learn_cols > self.settings.max_filter_x or
            samples_count > self.settings.max_filter_y
        )
