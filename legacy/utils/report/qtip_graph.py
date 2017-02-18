##############################################################################
# Copyright (c) 2017 ZTE Corporation and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

matplotlib.use('Agg')


def plot_indices(a, b, c):
    N = 3
    ind = np.arange(N)
    y_axis = (a, b, c)
    width = 0.35
    f = plt.figure()
    ax = f.gca()
    ax.set_autoscale_on(True)
    my_bars = ax.bar(ind, y_axis, width, color='b')
    ax.set_ylabel('Index Score*')
    ax.set_xlabel('Suite')
    ax.set_title(' QTIP benchmark scores')
    ax.axis('on')
    my_bars = ax.bar(ind, y_axis, width)
    ax.set_xticks(ind + width / 2)
    ax.set_xticklabels(['Compute', 'Storage', 'Network'])
    ax.axis([0, 3, 0, 1.25])
    f.text(0.7, 0.01, '* With Comparison to Refernece POD', fontsize=9)

    for rect in my_bars:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2., 1.05 * height, height, ha='center', va='bottom')
    f.savefig('qtip_graph.jpeg')
