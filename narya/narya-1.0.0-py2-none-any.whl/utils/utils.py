from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import six
import os
import numpy    as np
import pandas   as pd
import pickle

from six.moves  import range

SMM_WIDTH = 96
SMM_HEIGHT = 72

channel_dimensions = (SMM_WIDTH, SMM_HEIGHT)
frame = np.zeros((channel_dimensions[1], channel_dimensions[0]))

SMM_LAYERS = ["left_team", "right_team", "ball", "active"]

# Normalized minimap coordinates
MINIMAP_NORM_X_MIN = -1.0
MINIMAP_NORM_X_MAX = 1.0
MINIMAP_NORM_Y_MIN = -1.0 / 2.25
MINIMAP_NORM_Y_MAX = 1.0 / 2.25

_MARKER_VALUE = 255


def load_dump(dump_file):
    dump = []
    with open(dump_file, "rb") as in_fd:
        while True:
            try:
                step = six.moves.cPickle.load(in_fd)
            except EOFError:
                return dump
            dump.append(step)
    return dump


def mark_points(frame, frame_cnt, points):
    """Draw dots corresponding to 'points'.
    Args:
      frame: 2-d matrix representing one SMM channel ([y, x])
      points: a list of (x, y) coordinates to be marked
    """
    for p in range(len(points) // 2):
        x = int(
            (points[p * 2] - MINIMAP_NORM_X_MIN)
            / (MINIMAP_NORM_X_MAX - MINIMAP_NORM_X_MIN)
            * frame.shape[1]
        )
        y = int(
            (points[p * 2 + 1] - MINIMAP_NORM_Y_MIN)
            / (MINIMAP_NORM_Y_MAX - MINIMAP_NORM_Y_MIN)
            * frame.shape[0]
        )
        x = max(0, min(frame.shape[1] - 1, x))
        y = max(0, min(frame.shape[0] - 1, y))
        frame[y, x] = _MARKER_VALUE
        frame_cnt[y, x] += 1


def _left_parser(tab, i):
    """Helper function to build google observations
    """
    coord = []
    tab_ = tab[i]["left_team_positions"]
    for list_ in tab_:
        for value in list_:
            coord.append(value)
    return coord


def _right_parser(tab, i):
    """Helper function to build google observations
    """
    coord = []
    tab_ = tab[i]["right_team_positions"]
    for list_ in tab_:
        for value in list_:
            coord.append(value)
    return coord


def _ball_parser(tab, i):
    """Helper function to build google observations
    """
    tab_ = tab[i]["ball_position"]
    return tab_[:-1]


def _active_parser(tab, i):
    """Helper function to build google observations
    """
    tab_left = tab[i]["left_team_positions"]
    tab_ball = tab[i]["ball_position"][:-1]
    min_dist = 1000000
    for indx, list_ in enumerate(tab_left):
        dist = (list_[0] - tab_ball[0]) ** 2 + (list_[1] - tab_ball[1]) ** 2
        if dist < min_dist:
            min_dist = dist
            select = indx
    return tab_left[select]


def _build_obs_stacked(tab, i):
    """ Computes an observation, readable by an agent, from _save_data output
    Args:
      tab: Output of _save_data : player tracking data in the right coordinates
      i: Index of the frame to create
    Returns:
      frame: Google observations of the tracking data
      frame_count:Google observations count of the tracking data
    """
    frame = np.zeros((channel_dimensions[1], channel_dimensions[0], 16))
    frame_count = np.zeros((channel_dimensions[1], channel_dimensions[0], 16))
    mark_points(frame[:, :, 0], frame_count[:, :, 0], _left_parser(tab, i))
    mark_points(frame[:, :, 1], frame_count[:, :, 0], _right_parser(tab, i))
    mark_points(frame[:, :, 2], frame_count[:, :, 0], _ball_parser(tab, i))
    mark_points(frame[:, :, 3], frame_count[:, :, 0], _active_parser(tab, i))
    to_add = min((i + 1), len(tab) - 1)
    mark_points(frame[:, :, 4], frame_count[:, :, 0], _left_parser(tab, to_add))
    mark_points(frame[:, :, 5], frame_count[:, :, 0], _right_parser(tab, to_add))
    mark_points(frame[:, :, 6], frame_count[:, :, 0], _ball_parser(tab, to_add))
    mark_points(frame[:, :, 7], frame_count[:, :, 0], _active_parser(tab, to_add))
    to_add = min((i + 2), len(tab) - 1)
    mark_points(frame[:, :, 8], frame_count[:, :, 0], _left_parser(tab, to_add))
    mark_points(frame[:, :, 9], frame_count[:, :, 0], _right_parser(tab, to_add))
    mark_points(frame[:, :, 10], frame_count[:, :, 0], _ball_parser(tab, to_add))
    mark_points(frame[:, :, 11], frame_count[:, :, 0], _active_parser(tab, to_add))
    to_add = min((i + 3), len(tab) - 1)
    mark_points(frame[:, :, 12], frame_count[:, :, 0], _left_parser(tab, to_add))
    mark_points(frame[:, :, 13], frame_count[:, :, 0], _right_parser(tab, to_add))
    mark_points(frame[:, :, 14], frame_count[:, :, 0], _ball_parser(tab, to_add))
    mark_points(frame[:, :, 15], frame_count[:, :, 0], _active_parser(tab, to_add))

    return frame, frame_count


# For each play, we add to ball coordinates at each frame and for each player :
def _add_ball_coordinates(dataframe: pd.DataFrame) -> pd.DataFrame:
    """ Adds the ball coordinates at each row
    Args:
      dataframe: pd.DataFrame with player tracking data
    Returns:
      dataframe: pd.DataFrame with player tracking data
    """
    list_of_plays = list(dataframe.index.get_level_values("play").unique())

    # First, a function to compute this for one play at a time :
    def _add_coord(df):
        # Getting the balls infos:
        df_ball = df[df["edgecolor"] == 0]

        df_ball = df_ball[["frame", "x", "y", "z"]]
        df_ball.rename(
            columns={"x": "ball_x", "y": "ball_y", "z": "ball_z"}, inplace=True
        )

        df = df.merge(df_ball, on="frame", how="left")
        df = df.drop(columns=["Unnamed: 0"])
        return df

    for i, play in enumerate(list_of_plays):

        df = dataframe.loc[play]
        df = df.reset_index()

        if i == 0:
            new_dataframe = _add_coord(df)
            new_dataframe["play"] = play
        else:
            df = _add_coord(df)
            df["play"] = play
            new_dataframe = pd.concat([new_dataframe, df])

    return new_dataframe


# We now add a boolean to mark the possession of the ball by a player
def _add_possession(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Add a boolean to mark which player has the ball
    Args:
      dataframe: pd.DataFrame with player tracking data
    Returns:
      dataframe: pd.DataFrame with player tracking data
    """
    dataframe["possession"] = False
    columns = list(dataframe.columns.values)
    tab = dataframe.values

    for line in tab:
        # Not ocmputing for the ball :
        if line[4] != 0:
            if (line[8] - line[11]) ** 2 + (line[9] - line[12]) ** 2 < 1:
                line[-1] = True
                # Test to display later :
                line[4] = "black"

    dataframe = pd.DataFrame(tab, columns=columns)
    return dataframe


def _scale_mapper(x, y):
    """maps LastRow coordinates to google coordinates
    Args:
      x,y: Last Row coordinates
    Returns:
      new_x,new_y: Google env coordinates
    """
    # Takes our x,y and maps it into google's (x,y)
    new_x = (x / 100.0 - 0.5) * 2
    new_y = -(y / 100.0 - 0.5) * 2
    return (new_x, new_y)


def _save_data(df, filename):
    """Saves the LastRow tracking data into a google readable format
    Args:
      df:pd.DataFrame with player tracking data
      filename:a .dump filename to store the informations
    Returns:
      full_info: A list with the tracking data in a google observations format
    """
    df = df.reset_index()
    full_info = []
    for i in list(df["frame"].unique()):
        temp_df = df[df["frame"] == i]
        if (i + 1) in list(df["frame"].unique()):
            next_temp_df = df[df["frame"] == i + 1]
        else:
            next_temp_df = df[df["frame"] == i]

        left_df = temp_df[temp_df["team"] == "attack"]
        right_df = temp_df[temp_df["team"] == "defense"]

        next_left_df = next_temp_df[next_temp_df["team"] == "attack"]
        next_right_df = next_temp_df[next_temp_df["team"] == "defense"]

        left_team_positions = [[-1.0, 0.0]]
        right_team_positions = []
        left_team_velocity = [[0.0, 0.0]]
        right_team_velocity = []
        ball_position = []
        ball_velocity = []
        ball_team_owner = -1
        ball_player_owner = -1

        # Ball Information :

        # Left team informations :

        for indx, line in enumerate(left_df.values):
            new_x, new_y = _scale_mapper(line[8], line[9])
            next_line = next_left_df.values[indx]
            next_new_x, next_new_y = _scale_mapper(next_line[8], next_line[9])
            dx, dy = next_new_x - new_x, next_new_y - new_y

            left_team_positions.append([new_x, new_y])
            left_team_velocity.append([dx, dy])

            if line[-1] == True and ball_team_owner == -1:
                ball_team_owner = 0
                ball_player_owner = indx + 1

            if indx == 0:
                # Ball information :
                ball_x, ball_y = _scale_mapper(line[11], line[12])
                next_ball_x, next_ball_y = _scale_mapper(next_line[11], next_line[12])
                dx, dy = next_ball_x - ball_x, next_ball_y - ball_y
                ball_z = line[13]

                ball_position = [ball_x, ball_y, ball_z]
                ball_velocity = [dx, dy, 0.0]

        for indx, line in enumerate(right_df.values):
            new_x, new_y = _scale_mapper(line[8], line[9])
            next_line = next_right_df.values[indx]
            next_new_x, next_new_y = _scale_mapper(next_line[8], next_line[9])
            dx, dy = next_new_x - new_x, next_new_y - new_y

            right_team_positions.append([new_x, new_y])
            right_team_velocity.append([dx, dy])

        info = {
            "left_team_positions": left_team_positions,
            "right_team_positions": right_team_positions,
            "left_team_velocity": left_team_velocity,
            "right_team_velocity": right_team_velocity,
            "ball_position": ball_position,
            "ball_velocity": ball_velocity,
            "ball_team_owner": ball_team_owner,
            "ball_player_owner": ball_player_owner,
        }

        full_info.append(info)
    with open(filename, "wb") as fh:
        pickle.dump((full_info,), fh, pickle.HIGHEST_PROTOCOL)
    return full_info
