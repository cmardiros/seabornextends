import logging
import re
import numpy as np
import seaborn as sns

from seabornextends.retouch.ax import AxRetoucher
from seabornextends.retouch.fig import FigRetoucher


class GridRetoucher(object):
    """
    Adds refinements to a Seaborn grid with one or more facets (Ax objects).
    """

    def __init__(self, grid):

        if not isinstance(grid, sns.FacetGrid):
            msg = "grid must be sns.FacetGrid but is {}".format(type(grid))
            logging.error(msg)
            raise ValueError(msg)

        self.grid = grid

        self._fig = self.grid.fig
        self.fig = FigRetoucher(self._fig)

        self.axes = [ax for ax in grid.axes.ravel()]
        self.ax_retouchers = [AxRetoucher(ax) for ax in self.axes]

    def set_point_sizes(self,
                        sizes=None,
                        list_of_sizes=None):
        """
        If list of sizes, then one size list per ax
        """
        for idx, ax_retoucher in enumerate(self.ax_retouchers):
            if isinstance(list_of_sizes, (list, np.ndarray)):
                ax_retoucher.set_point_sizes(sizes=list_of_sizes[idx])
            elif sizes is not None:
                ax_retoucher.set_point_sizes(sizes=sizes)
            else:
                pass

    def set_point_colors(self,
                         colors=None,
                         list_of_colors=None):
        """
        If list of colors, then one size list per ax
        """
        for idx, ax_retoucher in enumerate(self.ax_retouchers):
            if isinstance(list_of_colors, (list, np.ndarray)):
                ax_retoucher.set_point_colors(colors=list_of_colors[idx])
            elif colors is not None:
                ax_retoucher.set_point_colors(colors=colors)
            else:
                pass

    def set_lines_colors(self,
                         colors=None,
                         list_of_colors=None):
        # TODO: len(colors) must match number of lines AND capsizes x2
        for idx, ax_retoucher in enumerate(self.ax_retouchers):
            if isinstance(list_of_colors, (list, np.ndarray)):
                ax_retoucher.set_lines_colors(colors=list_of_colors[idx])
            elif colors is not None:
                ax_retoucher.set_lines_colors(colors=colors)
            else:
                pass

    def set_lines_width(self,
                        width=1):
        for idx, ax_retoucher in enumerate(self.ax_retouchers):
            ax_retoucher.set_lines_width(width=width)

    def set_lim(self, **kwargs):
        for ax_retoucher in self.ax_retouchers:
            ax_retoucher.set_lim(**kwargs)

    def hide_axis_label(self, **kwargs):
        for ax_retoucher in self.ax_retouchers:
            ax_retoucher.hide_axis_label(**kwargs)

    def set_visible(self, **kwargs):
        for ax_retoucher in self.ax_retouchers:
            ax_retoucher.set_visible(**kwargs)

    def set_ticklabel_rotation(self, **kwargs):
        for ax_retoucher in self.ax_retouchers:
            ax_retoucher.set_ticklabel_rotation(**kwargs)

    def touch_dates_axis(self, **kwargs):
        for ax_retoucher in self.ax_retouchers:
            ax_retoucher.touch_dates_axis(**kwargs)

    def set_tick_params(self, **kwargs):
        for ax_retoucher in self.ax_retouchers:
            ax_retoucher.set_tick_params(**kwargs)

    def set_label_size(self, **kwargs):
        for ax_retoucher in self.ax_retouchers:
            ax_retoucher.set_label_size(**kwargs)

    def add_legend(self, **kwargs):
        """
        Set using grid method but can't pass override loc
        """
        def_legend_kws = {
            'bbox_to_anchor': (1.05, 1),
            'borderaxespad': 0.0
        }
        kwargs = kwargs or dict()
        legend_kws = dict(def_legend_kws, **kwargs)
        self.grid.add_legend(**legend_kws)

    def set_annot(self, annot, **kwargs):
        """
        NOTE: set to first axis only
        """
        def_annot_kws = {
            'x': 0.5,
            'y': -0.3,
            'verticalalignment': 'top',
            'horizontalalignment': 'left',
            'color': 'black',
            'wrap': True
        }
        kwargs = dict(def_annot_kws, **kwargs)
        ax = self.ax_retouchers[0].ax
        ax.text(s=annot, transform=ax.transAxes, **kwargs)

    def highlight_lines(self,
                        values,
                        axis='yaxis',
                        styles_kws=None):

        styles_kws = styles_kws or list()

        if len(values) == 1:
            values = values * len(self.axes)

        if not styles_kws:
            styles_kws = [None] * len(self.axes)

        if len(styles_kws) == 1:
            styles_kws = styles_kws * len(self.axes)

        for idx, ax_retoucher in enumerate(self.ax_retouchers):
            ax_retoucher.highlight_line(axis=axis,
                                        value=values[idx],
                                        style_kws=styles_kws[idx])

    def highlight_levels(self, df, category, highlights, axis='xaxis'):
        """
        Draw h or v lines to highlight levels in a category
        """

        if axis == 'xaxis':
            draw_aline_f = 'axvline'
        if axis == 'yaxis':
            draw_aline_f = 'axhline'

        for highlight in highlights:
            # TODO do we need except for level patterns
            level_pattern = highlight.get('level_pattern')
            color = highlight.get('color') or 'r'
            alpha = highlight.get('alpha') or 0.6
            style = highlight.get('style') or 'solid'
            width = highlight.get('width') or 1.5

            # get all levels for the plotted category
            # TODO: what if not category
            levels = df[category].cat.categories.tolist()

            # see which levels match the ones we want to highlight
            # and get their index
            level_pattern = re.compile(re.escape(level_pattern))
            matching_levels = [l for l in levels if level_pattern.search(l)]
            matching_levels_idx = [i for i, l in
                                   enumerate(levels) if l in matching_levels]

            for idx, ax_retoucher in enumerate(self.ax_retouchers):
                ax = ax_retoucher.ax
                for level_idx in matching_levels_idx:
                    getattr(ax, draw_aline_f)(level_idx,
                                              linestyle=style,
                                              linewidth=width,
                                              color=color,
                                              alpha=alpha)
