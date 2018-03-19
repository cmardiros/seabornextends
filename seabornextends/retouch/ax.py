import logging
from datetime import datetime
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

from seabornextends.retouch.fig import FigRetoucher


class AxRetoucher(object):

    """
    Adds refinements to a Matplotlib ax.
    """

    def __init__(self, ax):

        if not isinstance(ax, mpl.axes.Axes):
            msg = "ax must be mpl.axes.Axes but is {}".format(type(ax))
            logging.error(msg)
            raise ValueError(msg)

        self.ax = ax

        self._fig = self.ax.figure
        self.fig = FigRetoucher(self._fig)

    def _which_axis(self, axis):
        valid_axes = ['xaxis', 'yaxis']
        if axis not in valid_axes:
            msg = "axis must be one of {} but is {}".format(valid_axes, axis)
            logging.error(msg)
            raise ValueError(msg)
        return getattr(self.ax, axis)

    def set_point_sizes(self, sizes=[10]):
        plt.setp(self.ax.collections, sizes=sizes)

    def set_point_colors(self, colors):
        plt.setp(self.ax.collections, color=colors)

    def set_lines_colors(self, colors):
        for idx, line in enumerate(self.ax.get_lines()):
            line.set_color(colors[idx])

    def set_lines_width(self, width=2):
        plt.setp(self.ax.get_lines(), linewidth=width)

    def set_tick_params(self, axis='xaxis', **kwargs):
        """
        Example:
        ax_retoucher.set_tick_params(axis='xaxis',
                                     which='major',
                                     pad=15,
                                     labelsize=8)
        """
        # tick_params takes 'x', 'y' not 'xaxis', 'yaxis'
        axis = axis[0]
        self.ax.tick_params(axis=axis, **kwargs)

    def set_label_size(self, axis='xaxis', size=None):
        axis = self._which_axis(axis)
        if size:
            axis.label.set_size(size)

    def hide_axis_label(self, axis='xaxis'):
        if axis == 'xaxis':
            self.ax.set_xlabel('')
        if axis == 'yaxis':
            self.ax.set_ylabel('')

    def set_lim(self, axis='xaxis', **kwargs):
        if axis == 'xaxis':
            self.ax.set_xlim(**kwargs)
        if axis == 'yaxis':
            self.ax.set_ylim(**kwargs)

    def set_visible(self, axis='xaxis', visible=False):
        axis = self._which_axis(axis)
        axis.set_visible(visible)

    def set_ticklabel_rotation(self, axis='xaxis', rotation=90):
        axis = self._which_axis(axis)
        plt.setp(axis.get_majorticklabels(), rotation=rotation)

    def highlight_line(self, axis='yaxis', value=0, style_kws=None):
        def_style_kws = {
            'alpha': 0.3,
            'color': 'black',
            'linewidth': 2,
            'linestyle': 'solid'
        }
        style_kws = style_kws or dict()
        style_kws = dict(def_style_kws, **style_kws)

        if axis == 'xaxis' and value is not None:
            self.ax.axvline(value, **style_kws)
        if axis == 'yaxis' and value is not None:
            self.ax.axhline(value, **style_kws)

    def touch_dates_axis(self, axis='xaxis', fmt='%Y-%m-%d'):
        """
        Reformats date axis plotted from datetime64[ns]

        fmt examples:
        fmt='%Y-%m-%d'
        fmt='%Y-%b-%d'

        """

        axis = self._which_axis(axis)
        tick_labels = [tick.get_text() for tick in axis.get_majorticklabels()]
        new_ticks = list()
        for tick in tick_labels:
            tick_ = np.datetime64(tick, 's')   # seconds
            tick_ = datetime.utcfromtimestamp(tick_.astype(int))
            tick_ = tick_.strftime(fmt)
            new_ticks.append(tick_)

        self.ax.xaxis.set_major_formatter(ticker.FixedFormatter(new_ticks))

    def add_legend(self, **kwargs):
        def_legend_kws = {
            'bbox_to_anchor': (1.05, 1),
            'loc': 2,
            'borderaxespad': 0.0
        }
        legend_kws = dict(def_legend_kws, **kwargs)
        self.ax.legend(**legend_kws)
