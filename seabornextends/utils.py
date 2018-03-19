import scipy


def integrate_line(ax, line_idx=None):
    """
    Get line data from a plot and integrate it using scipy.cumtrapz.
    Useful for shading areas under the curve.

    Parameters
    ----------

        line_idx : int, default None
            Index of line to retrieve from axes, if None the last one
            is retrieved.
    """

    if not line_idx:
        line_idx = len(ax.get_lines()) - 1

    x, y = ax.get_lines()[line_idx].get_data()
    cdf = scipy.integrate.cumtrapz(y, x, initial=0)

    return x, y, cdf
