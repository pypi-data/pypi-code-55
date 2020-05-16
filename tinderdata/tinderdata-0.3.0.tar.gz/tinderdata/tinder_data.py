"""
Created on 2019.08.30
:author: Felix Soubelet

A callable script to process and get insight on your Tinder data.
All functionality is packed in a class and can be imported.
"""

import argparse
import json
import sys
import warnings
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from fsbox.contexts import timeit
from fsbox.plotting import PLOT_PARAMS
from loguru import logger

sns.set_style("whitegrid")
sns.set_palette("pastel")
plt.rcParams.update(PLOT_PARAMS)

MESSAGE_DATE_FORMAT = "%a, %d %b %Y %H:%M:%S %Z"
WEEK_DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

warnings.filterwarnings("ignore")


class TinderData:
    """
    A class to handle storing the json data given out by Tinder if required at
    `https://account.gotinder.com/data`. It has methods to give you simple insights on
    different aspects of your use of the Tinder service, or plot more complicated ones.
    It can also output the proper string to input into `http://sankeymatic.com/` to get a
    Sankey diagram of this data.
    """

    def __init__(self, json_data_path: str = None) -> None:
        """
        Instantiate, will store the entire json as an attribute, then two pandas DataFrame.
        One contains usage data, the other contains messages data.

        Args:
            json_data_path: string, path (absolute or relative) to json file with your Tinder data.
        """
        self.json_file_path: Path = Path(json_data_path).absolute()
        with timeit(lambda spanned: logger.debug(f"Loaded json data in {spanned:.4f} seconds")):
            with self.json_file_path.open("r") as f:
                self.json_data = json.load(f)
        with timeit(lambda spanned: logger.debug(f"Processed usage data in {spanned:.4f} seconds")):
            self.usage_df: pd.DataFrame = pd.DataFrame.from_dict(self.json_data["Usage"])
            self.usage_df.index = pd.to_datetime(self.usage_df.index)
        with timeit(
            lambda spanned: logger.debug(f"Processed message data in {spanned:.4f} seconds")
        ):
            self.messages_df: pd.DataFrame = pd.DataFrame(self.json_data["Messages"])
            self.messages_df.match_id = self.messages_df.match_id.apply(
                lambda x: int(x.split(" ")[1])
            )
            self.messages_df.set_index("match_id", inplace=True)
            self.messages_df.sort_index(inplace=True)
        logger.debug("Initialisation complete")

    def sankey_metrics(self) -> dict:
        """
        Extract and return usage and message metrics from the 'usage_df' and 'messages_df'
        dataframes,that will be necessary for the Sankey diagram.
        The 'usage_df' dataframe is indexed by date and fairly simple.
        The 'messages_df' dataframe is indexed by match ID (starting at 1) and its 'messages'
        column is a list in which is a dictionnary for each message sent to the specific match,
        with keys 'to', 'from' and 'message'.

        The values calculated from 'usage_df' are simply summation over time of columns.
        Some insight on keys taken from 'messages_df' and their values' calculation:
            contacted: number of rows without an empty list as values.
            replied: number of rows with >= 3 dicts (messages sent) in the list. Since Tinder
                     doesn't give messages sent by your matches, I assume you sending 3 or more
                     means they've answered.
            short_conversations: number of rows with <= 4 dicts (messages sent) in the list.
            long-conversations: number of rows with >= 20 dicts (messages sent) in the list.

        Returns:
            A dictionary with the different usage metrics, all integers.
        """
        with timeit(
            lambda spanned: logger.debug(
                f"Gathered Sankey general metrics in {spanned:.4f} seconds"
            )
        ):
            sankey_dict: dict = {
                "passes": self.usage_df.swipes_passes.sum(),
                "likes": self.usage_df.swipes_likes.sum(),
                "swipes": self.usage_df.swipes_passes.sum() + self.usage_df.swipes_likes.sum(),
                "matches": self.usage_df.matches.sum(),
                "sent_messages": self.usage_df.messages_sent.sum(),
                "received_messages": self.usage_df.messages_received.sum(),
            }
        with timeit(
            lambda spanned: logger.debug(
                f"Gathered Sankey message metrics in {spanned:.4f} seconds"
            )
        ):
            sankey_messages_dict = {
                "contacted": self.messages_df.messages.size
                - sum(1 for _ in self.messages_df.messages if len(_) is 0),
                "replied": sum(1 for e in self.messages_df.messages if len(e) >= 3),
                "short_conversations": sum(1 for e in self.messages_df.messages if len(e) <= 4),
                "long_conversations": sum(1 for e in self.messages_df.messages if len(e) >= 20),
            }
        return dict(sankey_dict, **sankey_messages_dict)

    @staticmethod
    def check_plot_dir() -> None:
        """
        Checks the `plots` output directory exists, creates it otherwise.
        """
        output_directory = Path("plots")
        if not Path("plots").is_dir():
            logger.debug(f"Creating output directory {output_directory.absolute()}")
            output_directory.mkdir()
        else:
            logger.warning(
                f"Output directory '{output_directory.absolute()}' already present. "
                f"This may lead to unexpected behaviour"
            )

    def output_message_statistics(self) -> None:
        """
        Compute and output some statistics on messages from your Tinder data.

        Returns:
            Nothing, will just print.
        """
        with timeit(
            lambda spanned: logger.debug(f"Gathered message statistics in {spanned:.4f} seconds")
        ):
            total_messages_sent: int = self.usage_df.messages_sent.sum()
            total_messages_received: int = self.usage_df.messages_received.sum()
        print("\n---- Message Statistics ----")
        print(f"Sent a total of {total_messages_sent} messages")
        print(f"Received a total of {total_messages_received} messages")

    def output_usage_statistics(self) -> None:
        """
        Print out some statistics about your Tinder usage through the period you've used it.

        Returns:
            Nothing, will just print.
        """
        with timeit(
            lambda spanned: logger.debug(f"Gathered usage statistics in {spanned:.4f} seconds")
        ):
            app_opens: pd.Series = self.usage_df.app_opens
            creation_date: str = app_opens.index.min()
            last_use_date: str = app_opens.index.max()
            days_with_use: int = app_opens[app_opens != 0].size
            time_period = pd.to_timedelta(last_use_date - creation_date)

        print("\n---- Usage Statistics ----")
        print(f"Account creation date: {creation_date}")
        print(f"Last usage date: {last_use_date}")
        print(f"Days spent with an active Tinder account: {time_period.days}")
        print(
            f"Opened on {days_with_use} unique days, and untouched on "
            f"{time_period.days - days_with_use} unique days."
        )
        print(f"Average app-open per usage-day: {app_opens[app_opens != 0].mean():.1f}")

    def output_success_statistics(self) -> None:
        """
        Print out some statistics about your Tinder success through the period you've used it.

        Returns:
            Nothing, will just print.
        """
        metrics: dict = self.sankey_metrics()

        print("\n---- Success Statistics ----")
        print(f"Matched on {100 * metrics['matches'] / metrics['likes']:.2f}% of sent likes")
        print(f"Contacted {100 * metrics['contacted'] / metrics['matches']:.2f}% of matches")
        print(
            f"Got a reply in {100 * metrics['replied'] / metrics['contacted']:.2f}% "
            "of conversations"
        )
        print(
            f"Kept it going in {100 * metrics['long_conversations'] / metrics['replied']:.2f}% "
            "of conversations"
        )

    def output_sankey_string(self) -> None:
        """
        Print out the exact text to intput at `http://sankeymatic.com/` in order to get this data
        in the form of a clean Sankey diagram. Might need some tuning on the colors, size and
        other parameters.

        Returns:
            Nothing, will just print.
        """
        metrics: dict = self.sankey_metrics()
        print(f"\n---- Sankey Diagram Input ----")
        print(
            f"""Swipes [{metrics['passes']}] Left
Swipes [{metrics['likes']}] Right
Right [{metrics['matches']}] Matches
Right [{metrics['likes'] - metrics['matches']}] No Match
Matches [{metrics['contacted']}] Contacted
Matches [{metrics['matches'] - metrics['contacted']}] Nothing
Contacted [{metrics['replied']}] Replied
Contacted [{metrics['contacted'] - metrics['replied']}] No Reply
Replied [{metrics['long_conversations']}] Long Conversations
Replied [{metrics['replied'] - metrics['long_conversations']}] Short Conversations
Short Conversations [{metrics['replied'] - metrics['long_conversations']}] Ghosted\n"""
        )

    def output_swipes_statistics(self) -> None:
        """
        Print out some statistics about your Tinder swipes through the period you've used it.

        Returns:
            Nothing, will just print.
        """
        metrics = self.sankey_metrics()

        print("\n---- Swipes Statistics ----")
        print(f"Swiped a total of {metrics['swipes']} profiles")
        print(
            f"Liked {metrics['likes']} ({100 * metrics['likes'] / metrics['swipes']:.1f}%) "
            "of profiles"
        )
        print(
            f"Passed on {metrics['passes']} ({100 * metrics['passes'] / metrics['swipes']:.1f}%) "
            "of profiles"
        )
        print(
            f"Matched with {metrics['matches']} ("
            f"{100 * metrics['matches'] / metrics['swipes']:.1f}%) profiles"
        )

    def plot_messages_loyalty(
        self, figsize: tuple = (16, 10), showfig: bool = False, savefig: bool = True
    ) -> None:
        """
        Plot the duration of conversations with different matches. Simply plots a point at height
        'Match ID' for each day a message was sent.

        Args:
            figsize: figure size
            showfig: if this is set to True, the figure will be shown. Defaults to False.
            savefig: if this is set to True, the figure will be saved. Defaults to True.

        Returns:
            Nothing, just plots.
        """
        logger.debug("Plotting messages loyalty insight")
        fig, axis = plt.subplots(figsize=figsize)

        for index, conversation in self.messages_df.messages.items():
            dates = [
                datetime.strptime(message["sent_date"], MESSAGE_DATE_FORMAT)
                for message in conversation
            ]
            axis.plot(dates, [index] * len(dates), ".", c="royalblue")

        axis.tick_params(axis="x", rotation=35)
        axis.set_xlabel("Date")
        axis.set_ylabel("Match ID")
        axis.set_title("Message Loyality: Duration of Conversation with Different Matches")
        fig.tight_layout()

        if showfig:
            logger.debug("Showing message loyalty figure")
            plt.show()
        if savefig:
            logger.debug("Saving message loyalty figure")
            fig.savefig("plots/message_loyalty.png", format="png", dpi=500)
            logger.success("Saved message loyalty plot as 'plots/message_loyalty.png'")

    def plot_messages_monthly_stats(
        self, figsize: tuple = (20, 12), showfig: bool = False, savefig: bool = True
    ) -> None:
        """
        Compute the monthly sent and received number of messages, then output it as a stacked
        barplot. Also plot the % of received/sent ratio.

        Args:
            figsize: figure size
            showfig: if this is set to True, the figure will be shown. Defaults to False.
            savefig: if this is set to True, the figure will be saved. Defaults to True.

        Returns:
            Nothing, just plots.
        """
        logger.debug("Plotting messages monthly insights")

        with timeit(
            lambda spanned: logger.debug(
                f"Gathered monthly message statistics in {spanned:.4f} seconds"
            )
        ):
            vals_monthly = self.usage_df.groupby(pd.Grouper(freq="M")).sum()
            vals_monthly["ratio"] = (
                100 * vals_monthly.messages_received / vals_monthly.messages_sent
            )
            vals_monthly.fillna(0, inplace=True)

        fig, axis1 = plt.subplots(figsize=figsize)
        axis2 = axis1.twinx()

        axis1.bar(
            vals_monthly.index,
            vals_monthly.messages_sent,
            width=1,
            label="Messages Sent",
            color="blue",
            alpha=0.4,
        )
        axis1.bar(
            vals_monthly.index,
            vals_monthly.messages_received,
            bottom=vals_monthly.messages_sent,
            width=1,
            label="Messages Received",
            color="red",
            alpha=0.4,
        )
        axis2.plot(vals_monthly.index, vals_monthly.ratio, color="grey", lw=1.5)

        axis1.set_xlabel("Date")
        axis1.set_ylabel("Number of Messages")
        axis1.set_title("Messages per Month")
        axis1.tick_params(axis="x", rotation=75)
        axis1.legend()
        axis2.set_ylabel("Received/Sent [%]", color="grey")
        axis2.tick_params(axis="y", labelcolor="grey")
        axis2.grid(False)
        fig.tight_layout()

        if showfig:
            logger.debug("Showing message monthly stats figure")
            plt.show()
        if savefig:
            logger.debug("Saving message monthly stats figure")
            fig.savefig("plots/messages_monthly_stats.png", format="png", dpi=500)
            logger.success("Saved message monthly stats plot as 'plots/messages_monthly_stats.png'")

    def plot_messages_weekday_stats(
        self, figsize: tuple = (20, 12), showfig: bool = False, savefig: bool = True
    ) -> None:
        """
        Compute the sent and received number of messages for each day of the week, then output it
        as a stacked barplot. Also plot the % of received/sent ratio.

        Args:
            figsize: figure size
            showfig: if this is set to True, the figure will be shown. Defaults to False.
            savefig: if this is set to True, the figure will be saved. Defaults to True.

        Returns:
            Nothing, just plots.
        """
        logger.debug("Plotting messages weekday insights")

        with timeit(
            lambda spanned: logger.debug(
                f"Gathered weekday message statistics in {spanned:.4f} seconds"
            )
        ):
            # Careful, index sorts alphabetically for now
            vals_weekday = self.usage_df.groupby(self.usage_df.index.weekday_name).sum()
            vals_weekday["ratio"] = (
                100 * vals_weekday.messages_received / vals_weekday.messages_sent
            )
            vals_weekday.fillna(0, inplace=True)

            # Getting index as categorical properly ordered weekdays
            weekday_categories = pd.api.types.CategoricalDtype(categories=WEEK_DAYS, ordered=True)
            vals_weekday.index = vals_weekday.index.astype(weekday_categories)
            vals_weekday.sort_index(inplace=True)

        fig, axis1 = plt.subplots(figsize=figsize)
        axis2 = axis1.twinx()

        axis1.bar(
            vals_weekday.index,
            vals_weekday.messages_sent,
            label="Messages Sent",
            color="blue",
            alpha=0.4,
        )
        axis1.bar(
            vals_weekday.index,
            vals_weekday.messages_received,
            bottom=vals_weekday.messages_sent,
            label="Messages Received",
            color="red",
            alpha=0.4,
        )
        axis2.plot(vals_weekday.index, vals_weekday.ratio, color="grey", lw=1.5)

        axis1.set_xlabel("Date")
        axis1.set_ylabel("Number of Messages")
        axis1.set_title("Messages per Month")
        axis1.tick_params(axis="x", rotation=75)
        axis1.legend()
        axis2.set_ylabel("Received/Sent [%]", color="grey")
        axis2.tick_params(axis="y", labelcolor="grey")
        axis2.grid(False)
        fig.tight_layout()

        if showfig:
            logger.debug("Showing message weekday stats figure")
            plt.show()
        if savefig:
            logger.debug("Saving message weekday stats figure")
            fig.savefig("plots/messages_weekday_stats.png", format="png", dpi=500)
            logger.success(
                "Saved messages weekday stats plot as " "'plots/messages_weekday_stats.png'"
            )

    def plot_swipes_monthly_stats(
        self, figsize: tuple = (20, 12), showfig: bool = False, savefig: bool = True
    ):
        """
        Compute the monthly left and right swipes, then output it as a stacked barplot. Also plot
        the monthly number of matches.

        Args:
            figsize: figure size
            showfig: if this is set to True, the figure will be shown. Defaults to False.
            savefig: if this is set to True, the figure will be saved. Defaults to True.

        Returns:
            Nothing, just plots.
        """
        logger.debug("Plotting swipes monthly insights")

        with timeit(
            lambda spanned: logger.debug(
                f"Gathered monthly swipe statistics in {spanned:.4f} seconds"
            )
        ):
            vals_monthly = self.usage_df.groupby(pd.Grouper(freq="M")).sum()
            vals_monthly.fillna(0, inplace=True)

        fig, axis1 = plt.subplots(figsize=figsize)
        axis2 = axis1.twinx()

        axis1.bar(
            vals_monthly.index,
            vals_monthly.swipes_likes,
            width=1,
            label="'Like' Swipes",
            color="blue",
            alpha=0.4,
        )
        axis1.bar(
            vals_monthly.index,
            vals_monthly.swipes_passes,
            bottom=vals_monthly.swipes_likes,
            width=1,
            label="'Pass' Likes",
            color="red",
            alpha=0.4,
        )
        axis2.plot(vals_monthly.index, vals_monthly.matches, color="grey", label="Matches", lw=1.5)

        axis1.set_xlabel("Date")
        axis1.set_ylabel("Number of Swipes")
        axis1.set_title("Swipes per Month")
        axis1.tick_params(axis="x", rotation=75)
        axis2.set_ylabel("Number of Matches", color="grey")
        axis2.tick_params(axis="y", labelcolor="grey")
        axis2.grid(False)
        fig.legend(loc=2, bbox_to_anchor=(0, 1), bbox_transform=axis1.transAxes)
        fig.tight_layout()

        if showfig:
            logger.debug("Showing swipes monthly stats figure")
            plt.show()
        if savefig:
            logger.debug("Saving swipes monthly stats figure")
            fig.savefig("plots/swipes_monthly_stats.png", format="png", dpi=500)
            logger.success("Saved swipes monthly stats plot as 'plots/swipes_monthly_stats.png'")

    def plot_swipes_monthly_relative_stats(
        self, figsize: tuple = (20, 12), showfig: bool = False, savefig: bool = True
    ):
        """
        Plot percentage of the total number of swipes that were likes, passes and those that
        resulted in matches, on a monthly basis.

        Args:
            figsize: figure size
            showfig: if this is set to True, the figure will be shown. Defaults to False.
            savefig: if this is set to True, the figure will be saved. Defaults to True.

        Returns:
            Nothing, just plots.
        """
        logger.debug("Plotting swipes monthly relative insights")

        with timeit(
            lambda spanned: logger.debug(
                f"Gathered monthly relative swipe statistics in {spanned:.4f} seconds"
            )
        ):
            vals_monthly = self.usage_df.groupby(pd.Grouper(freq="M")).sum()
            vals_monthly["total_swipes"] = vals_monthly.swipes_likes + vals_monthly.swipes_passes
            vals_monthly["likes_ratio"] = (
                100 * vals_monthly.swipes_likes / vals_monthly.total_swipes
            )
            vals_monthly["matches_ratio"] = 100 * vals_monthly.matches / vals_monthly.total_swipes
            vals_monthly["passes_ratio"] = (
                100 * vals_monthly.swipes_passes / vals_monthly.total_swipes
            )
            vals_monthly.fillna(0, inplace=True)

        fig, axis1 = plt.subplots(figsize=figsize)

        axis1.plot(
            vals_monthly.index,
            vals_monthly.likes_ratio,
            color="blue",
            label="'Like' Swipes",
            lw=1.5,
        )
        axis1.plot(
            vals_monthly.index,
            vals_monthly.passes_ratio,
            color="red",
            label="'Pass' Swipes",
            lw=1.5,
        )
        axis1.plot(
            vals_monthly.index, vals_monthly.matches_ratio, color="green", label="Matches", lw=1.5
        )

        axis1.set_xlabel("Date")
        axis1.set_ylabel("Percentage of Total Swipes [%]")
        axis1.set_title("Monthly Ratio of Likes, Passes and Matches to Total Swipes")
        axis1.tick_params(axis="x", rotation=75)
        axis1.legend()
        fig.tight_layout()

        if showfig:
            logger.debug("Showing swipes monthly relative stats figure")
            plt.show()
        if savefig:
            logger.debug("Saving swipes monthly relative stats figure")
            fig.savefig("plots/swipes_monthly_relative_stats.png", format="png", dpi=500)
            logger.success(
                "Saved swipes monthly relative stats plot as "
                "'plots/swipes_monthly_relative_stats.png'"
            )

    def plot_swipes_weekday_stats(
        self, figsize: tuple = (20, 12), showfig: bool = False, savefig: bool = True
    ) -> None:
        """
        Compute the  number of right and left swipes sent for each day of the week, then output
        it as a stacked barplot. Also plot the number of matches for each weekday.

        Args:
            figsize: figure size
            showfig: if this is set to True, the figure will be shown. Defaults to False.
            savefig: if this is set to True, the figure will be saved. Defaults to True.

        Returns:
            Nothing, just plots.
        """
        logger.debug("Plotting swipes weekday insights")

        with timeit(
            lambda spanned: logger.debug(
                f"Gathered weekday swipe statistics in {spanned:.4f} seconds"
            )
        ):
            # Careful, index sorts alphabetically for now)
            vals_weekday = self.usage_df.groupby(self.usage_df.index.weekday_name).sum()
            vals_weekday.fillna(0, inplace=True)

            # Getting index as categorical properly ordered weekdays
            weekday_categories = pd.api.types.CategoricalDtype(categories=WEEK_DAYS, ordered=True)
            vals_weekday.index = vals_weekday.index.astype(weekday_categories)
            vals_weekday.sort_index(inplace=True)

        fig, axis1 = plt.subplots(figsize=figsize)
        axis2 = axis1.twinx()

        axis1.bar(
            vals_weekday.index,
            vals_weekday.swipes_likes,
            label="'Like' Swipes",
            color="blue",
            alpha=0.4,
        )
        axis1.bar(
            vals_weekday.index,
            vals_weekday.swipes_passes,
            bottom=vals_weekday.swipes_likes,
            label="'Pass' Swipes",
            color="red",
            alpha=0.4,
        )
        axis2.plot(vals_weekday.index, vals_weekday.matches, color="grey", lw=1.5)

        axis1.set_xlabel("Date")
        axis1.set_ylabel("Number of Swipes")
        axis1.set_title("Swipes per Weekday")
        axis1.tick_params(axis="x", rotation=75)
        axis1.legend()
        axis2.set_ylabel("Number of Matches", color="grey")
        axis2.tick_params(axis="y", labelcolor="grey")
        axis2.grid(False)
        fig.tight_layout()

        if showfig:
            logger.debug("Showing swipes weekday stats figure")
            plt.show()
        if savefig:
            logger.debug("Saving swipes weekday stats figure")
            fig.savefig("plots/swipes_weekdays_stats.png", format="png", dpi=500)
            logger.success("Saved swipes weekdays stats plot as 'plots/swipes_weekdays_stats.png'")

    def plot_swipes_weekday_relative_stats(
        self, figsize: tuple = (20, 12), showfig: bool = False, savefig: bool = True
    ):
        """
        Plot percentage of the total number of swipes that were likes, passes and those that
        resulted in matches, on a monthly basis.

        Args:
            figsize: figure size
            showfig: if this is set to True, the figure will be shown. Defaults to False.
            savefig: if this is set to True, the figure will be saved. Defaults to True.

        Returns:
            Nothing, just plots.
        """
        logger.debug("Plotting swipes weekday relative insights")

        with timeit(
            lambda spanned: logger.debug(
                f"Gathered relative weekday swipe statistics in {spanned:.4f} seconds"
            )
        ):
            # Careful, index sorts alphabetically for now)
            vals_weekday = self.usage_df.groupby(self.usage_df.index.weekday_name).sum()
            vals_weekday.fillna(0, inplace=True)

            # Getting index as categorical properly ordered weekdays
            weekday_categories = pd.api.types.CategoricalDtype(categories=WEEK_DAYS, ordered=True)
            vals_weekday.index = vals_weekday.index.astype(weekday_categories)

            vals_weekday["total_swipes"] = vals_weekday.swipes_likes + vals_weekday.swipes_passes
            vals_weekday["likes_ratio"] = (
                100 * vals_weekday.swipes_likes / vals_weekday.total_swipes
            )
            vals_weekday["matches_ratio"] = 100 * vals_weekday.matches / vals_weekday.total_swipes
            vals_weekday["passes_ratio"] = (
                100 * vals_weekday.swipes_passes / vals_weekday.total_swipes
            )
            vals_weekday.fillna(0, inplace=True)

        fig, axis1 = plt.subplots(figsize=figsize)

        axis1.plot(
            vals_weekday.index,
            vals_weekday.likes_ratio,
            color="blue",
            label="'Like' Swipes",
            lw=1.5,
        )
        axis1.plot(
            vals_weekday.index,
            vals_weekday.passes_ratio,
            color="red",
            label="'Pass' Swipes",
            lw=1.5,
        )
        axis1.plot(
            vals_weekday.index, vals_weekday.matches_ratio, color="green", label="Matches", lw=1.5
        )

        axis1.set_xlabel("Date")
        axis1.set_ylabel("Percentage of Total Swipes [%]")
        axis1.set_title("Monthly Ratio of Likes, Passes and Matches to Total Swipes")
        axis1.tick_params(axis="x", rotation=75)
        axis1.legend()
        fig.tight_layout()

        if showfig:
            logger.debug("Showing swipes weekday relative stats figure")
            plt.show()
        if savefig:
            logger.debug("Saving swipes weekday relative stats figure")
            fig.savefig("plots/swipes_weekdays_relative_stats.png", format="png", dpi=500)
            logger.success(
                "Saved swipes weekdays relative stats plot as "
                "'plots/swipes_weekdays_relative_stats.png'"
            )


# ---------------------- Runtime Function ---------------------- #


def main() -> None:
    """
    Ran when calling the file from the command line, gather data and show / saves plots
    according to parsed arguments.

    Returns:
        Nothing.
    """
    command_line_args = _parse_arguments()
    _set_logger_level(command_line_args.log_level)

    show_figures = command_line_args.show
    save_figures = command_line_args.save
    tinder = TinderData(command_line_args.path)
    tinder.check_plot_dir()

    logger.info("Getting usage statistics")
    tinder.output_usage_statistics()
    tinder.output_swipes_statistics()
    tinder.output_success_statistics()
    tinder.output_message_statistics()
    tinder.output_sankey_string()

    logger.info("Plotting insights on messages")
    tinder.plot_messages_loyalty(showfig=show_figures, savefig=save_figures)
    tinder.plot_messages_monthly_stats(showfig=show_figures, savefig=save_figures)
    tinder.plot_messages_weekday_stats(showfig=show_figures, savefig=save_figures)

    logger.info("Plotting insights on swipes")
    tinder.plot_swipes_monthly_stats(showfig=show_figures, savefig=save_figures)
    tinder.plot_swipes_monthly_relative_stats(showfig=show_figures, savefig=save_figures)
    tinder.plot_swipes_weekday_stats(showfig=show_figures, savefig=save_figures)
    tinder.plot_swipes_weekday_relative_stats(showfig=show_figures, savefig=save_figures)


# ---------------------- Private Utilities ---------------------- #


def _parse_arguments():
    """Simple argument parser to make life easier in the command-line."""
    parser = argparse.ArgumentParser(description="Getting insight on your Tinder usage.")
    parser.add_argument(
        "-p",
        "--path-to-data",
        dest="path",
        default=None,
        required=True,
        type=str,
        help="Absolute path to the json file of your tinder data. Can be absolute or relative.",
    )
    parser.add_argument(
        "--show-figures",
        dest="show",
        default=False,
        type=bool,
        help="Whether or not to show figures when plotting insights. Defaults to False.",
    )
    parser.add_argument(
        "--save-figures",
        dest="save",
        default=False,
        type=bool,
        help="Whether or not to save figures when plotting insights. Defaults to False.",
    )
    parser.add_argument(
        "-l",
        "--logs",
        dest="log_level",
        default="info",
        type=str,
        help="The base console logging level. Can be 'debug', 'info', 'warning' and 'error'. "
        "Defaults to 'info'.",
    )
    return parser.parse_args()
    # options = parser.parse_args()
    # return options.path, options.show, options.save, options.log_level


def _set_logger_level(log_level: str = "info") -> None:
    """
    Sets the logger level to the one provided at the commandline.

    Default loguru handler will have DEBUG level and ID 0.
    We need to first remove this default handler and add ours with the wanted level.

    Args:
        log_level: string, the default logging level to print out.

    Returns:
        Nothing, acts in place.
    """
    logger.remove(0)
    logger.add(sys.stderr, level=log_level.upper())


# ---------------------- Private Utilities ---------------------- #

if __name__ == "__main__":
    main()
