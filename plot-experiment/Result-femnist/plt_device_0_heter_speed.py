"""Helper to visualize metrics-2."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import mark_inset
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import numpy as np
import os
import pandas as pd
import sys

from decimal import Decimal

models_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(models_dir)

ACCURACY_KEY = 'accuracy'
NUM_ROUND_KEY = 'round_number'
NUM_SAMPLES_KEY = 'num_samples'
CLIENT_ID_KEY = 'client_id'
SERVER_TIME_KEY = 'server_time'


# def load_data(stat_metrics_file='stat_metrics.csv', sys_metrics_file='sys_metrics.csv'):
def load_data(stat_metrics_file='stat_metrics.csv'):
    """Loads the data from the given stat_metric and sys_metric files."""
    stat_metrics = pd.read_csv(stat_metrics_file) if stat_metrics_file else None

    if stat_metrics is not None:
        stat_metrics.sort_values(by=NUM_ROUND_KEY, inplace=True)

    return stat_metrics


def _set_plot_properties(properties):
    """Sets some plt properties."""
    if 'xlim' in properties:
        plt.xlim(properties['xlim'])
    if 'ylim' in properties:
        plt.ylim(properties['ylim'])
    if 'xlabel' in properties:
        plt.xlabel(properties['xlabel'])
    if 'ylabel' in properties:
        plt.ylabel(properties['ylabel'])


def get_acc(stat_metrics, round_or_time, weighted=False):
    if weighted:
        accuracies = stat_metrics.groupby(round_or_time).apply(_weighted_mean, ACCURACY_KEY, NUM_SAMPLES_KEY)
        accuracies = accuracies.reset_index(name=ACCURACY_KEY)

    else:
        accuracies = stat_metrics.groupby(round_or_time, as_index=False).mean()

    return accuracies


def plot_accuracy_vs_round_number_leaf_lan_aware(weighted=False, plot_stds=False, figsize=(10, 8), title_fontsize=16, **kwargs):
    plt.figure(figsize=figsize)
    title_weighted = 'Weighted' if weighted else 'Unweighted'
    plt.title('Accuracy vs Round Number', fontsize=title_fontsize)

    plt.plot(leaf_epochs_10_acc_round[NUM_ROUND_KEY], leaf_epochs_10_acc_round[ACCURACY_KEY],
             label='leaf_epochs_10')
    plt.plot(speed_2020202020_acc_round[NUM_ROUND_KEY], speed_2020202020_acc_round[ACCURACY_KEY],
             label='speed_2020202020')
    plt.plot(speed_1010101030_acc_round[NUM_ROUND_KEY], speed_1010101030_acc_round[ACCURACY_KEY],
             label='speed_1010101030')
    plt.plot(speed_2020202020_op_acc_round[NUM_ROUND_KEY], speed_2020202020_op_acc_round[ACCURACY_KEY],
             label='speed_2020202020_op')
    # plt.plot(speed_1010101030_op_fu_acc_round[NUM_ROUND_KEY], speed_1010101030_op_fu_acc_round[ACCURACY_KEY],
    #          label='speed_1010101030_op_fu')

    plt.legend(loc='lower right')
    plt.grid(True)

    plt.ylabel('Accuracy')
    plt.xlabel('Round Number')
    _set_plot_properties(kwargs)
    plt.show()


def plot_accuracy_vs_server_time_leaf_lan_aware(weighted=False, plot_stds=False, figsize=(10, 8), title_fontsize=16, **kwargs):
    plt.figure(figsize=figsize)
    # title_weighted = 'Weighted' if weighted else 'Unweighted'
    # plt.title('Weighted Accuracy vs Clock Time', fontsize=title_fontsize)
    # fig, ax = plt.subplots(1, 1, figsize=(6,4))

    # plt.plot(leaf_epochs_5_acc_time[SERVER_TIME_KEY], leaf_epochs_5_acc_time[ACCURACY_KEY],
    #          label='leaf_epochs_5')
    plt.plot([time_second/3600 for time_second in leaf_epochs_10_acc_time[SERVER_TIME_KEY]], leaf_epochs_10_acc_time[ACCURACY_KEY],
             label='WAN-FL',
             linestyle='-', marker='o', color='red', linewidth=1)
    plt.plot([time_second/3600 for time_second in speed_2020202020_acc_time[SERVER_TIME_KEY]], speed_2020202020_acc_time[ACCURACY_KEY],
             label='LanFL homo',
             linestyle=':', marker='v', color='blue', linewidth=1)
    plt.plot([time_second/3600 for time_second in speed_1010101030_acc_time[SERVER_TIME_KEY]], speed_1010101030_acc_time[ACCURACY_KEY],
             label='LanFL w/o opt',
             linestyle='--', marker='*', color='c', linewidth=1)
    plt.plot([time_second/3600 for time_second in speed_2020202020_op_acc_time[SERVER_TIME_KEY]], speed_2020202020_op_acc_time[ACCURACY_KEY],
             label='LanFL',
             linestyle='-.', marker='d', color='m', linewidth=1)
    # plt.plot(speed_1010101030_op_fu_acc_time[SERVER_TIME_KEY], speed_1010101030_op_fu_acc_time[ACCURACY_KEY],
    #          label='speed_1010101030_op_fu')

    plt.legend(loc='lower right', fontsize=38)
    plt.xlim(0, 30)
    # plt.ylim(0.6, 0.9)
    plt.grid(True)

    plt.ylabel('Accuracy (%)', fontsize=28)
    plt.xlabel('Clock Time (Hour)', fontsize=28)
    _set_plot_properties(kwargs)
    plt.xticks(fontsize=26)
    plt.yticks(fontsize=26)
    plt.savefig('pdf/eval-heter-femnist-setting2.pdf', bbox_inches='tight')
    plt.show()


def get_x_y(list_to_simple):
    x = [list_to_simple[i] for i in range(0, len(list_to_simple), 10)]
    return x


def _weighted_mean(df, metric_name, weight_name):
    d = df[metric_name]
    w = df[weight_name]
    try:
        return (w * d).sum() / w.sum()
    except ZeroDivisionError:
        return np.nan


def _weighted_std(df, metric_name, weight_name):
    d = df[metric_name]
    w = df[weight_name]
    try:
        weigthed_mean = (w * d).sum() / w.sum()
        return (w * ((d - weigthed_mean) ** 2)).sum() / w.sum()
    except ZeroDivisionError:
        return np.nan


if __name__ == '__main__':
    # data dir
    leaf_epochs_10_dir = 'lan-vs-leaf/leaf/clients_50/device_2/epochs_10/metrics/metrics_stat.csv'
    speed_2020202020_dir = 'heter_speed/clients_5×10/epochs_2_agg_5/device_2/speed_2020202020/metrics/metrics_stat.csv'
    # heter-1
    # speed_1010101030_dir = 'heter_speed/clients_5×10/epochs_2_agg_5/device_2/speed_1010101030/metrics/metrics_stat.csv'
    # speed_2020202020_op_dir = 'heter_speed/clients_5×10/epochs_2_agg_5/device_2/speed_2020202020_op/metrics/metrics_stat.csv'
    # heter-2
    speed_1010101030_dir = 'heter_speed/clients_5×10/epochs_2_agg_5/device_2/speed_520204040/metrics/metrics_stat.csv'
    speed_2020202020_op_dir = 'heter_speed/clients_5×10/epochs_2_agg_5/device_2/speed_520204040_op/metrics-2/metrics_stat.csv'

    leaf_epochs_10_acc_round = get_acc(load_data(leaf_epochs_10_dir), NUM_ROUND_KEY, weighted=True)
    leaf_epochs_10_acc_time = get_acc(load_data(leaf_epochs_10_dir), SERVER_TIME_KEY, weighted=True)
    speed_2020202020_acc_round = get_acc(load_data(speed_2020202020_dir), NUM_ROUND_KEY, weighted=True)
    speed_2020202020_acc_time = get_acc(load_data(speed_2020202020_dir), SERVER_TIME_KEY, weighted=True)
    speed_1010101030_acc_round = get_acc(load_data(speed_1010101030_dir), NUM_ROUND_KEY, weighted=True)
    speed_1010101030_acc_time = get_acc(load_data(speed_1010101030_dir), SERVER_TIME_KEY, weighted=True)
    speed_2020202020_op_acc_round = get_acc(load_data(speed_2020202020_op_dir), NUM_ROUND_KEY, weighted=True)
    speed_2020202020_op_acc_time = get_acc(load_data(speed_2020202020_op_dir), SERVER_TIME_KEY, weighted=True)
    # plot_accuracy_vs_round_number_leaf_lan_aware(weighted=True)
    plot_accuracy_vs_server_time_leaf_lan_aware(weighted=True)
    print()