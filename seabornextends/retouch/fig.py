import math
import matplotlib as mpl
import matplotlib.pyplot as plt


class FigRetoucher(object):

    def __init__(self, fig):

        if not isinstance(grid, mpl.figure.Figure):
            msg = "fig must be mpl.figure.Figure but is {}".format(type(fig))
            logging.error(msg)
            raise ValueError(msg)

        self.fig = fig

    def set_size(self, w=25, h=4, dpi=300):

        if isinstance(w, str) and 'px' in w:
            wpx = int(math.ceil(float(w.replace('px', ''))))
            w = wpx * 1.0 / dpi

        if isinstance(h, str) and 'px' in h:
            hpx = int(math.ceil(float(h.replace('px', ''))))
            h = hpx * 1.0 / dpi

        self.fig.set_size_inches(w=w, h=h)

    def set_dpi(self, dpi=300):
        self.fig.set_dpi(dpi)

    def set_title(self, title, **kwargs):
        def_title_kws = {
            'y': 1,
            'x': 0.5,
            'fontweight': 'bold',
        }
        kwargs = kwargs or dict()
        kwargs = dict(def_title_kws, **kwargs)

        self.fig.suptitle(t=title,
                          **kwargs)

    def adjust_legend(self, **kwargs):
        def_legend_kws = {
            'bbox_to_anchor': (1.05, 1),
            'loc': 2,
            'borderaxespad': 0.0
        }
        kwargs = dict(def_legend_kws, **kwargs)
        plt.legend(**kwargs)

    def adjust_subplots(self, **kwargs):
        def_subplots_kws = {
            'wspace': 0,
            'hspace': 0
        }
        subplots_kws = dict(def_subplots_kws, **kwargs)
        self.fig.subplots_adjust(**subplots_kws)

    def set_tight_layout(self):
        try:
            self.fig.tight_layout()
        except ValueError:
            # skip set_tight_layout error
            pass

    def set_annot(self, annot, **kwargs):
        def_annot_kws = {
            'x': 0.5,
            'y': -0.3,
            'verticalalignment': 'center',
            'horizontalalignment': 'center',
            'color': 'black',
            'wrap': True
        }
        kwargs = dict(def_annot_kws, **kwargs)
        self.fig.text(s=annot, **kwargs)
