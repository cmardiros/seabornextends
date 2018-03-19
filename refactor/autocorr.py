def autocorrplot(data,
                 measure,
                 maxlag=None,
                 discrete=False,
                 **plot_kws):

    fig = plt.figure()

    def_plot_kws = {'color': 'steelblue'}
    plot_kws = plot_kws or dict()
    plot_kws = dict(def_plot_kws, **plot_kws)
    series = data[measure]
    n = series.shape[0]
    maxlag = maxlag if maxlag else n

    ax = plt.gca(xlim=(1, maxlag), ylim=(-1.0, 1.0))

    mean = series.mean()
    c0 = np.sum((series - mean) ** 2) / float(n)

    def r(h):
        return ((series[:n - h] - mean) *
                (series[h:] - mean)).sum() / float(n) / c0

    x = np.arange(n) + 1
    y = pd.compat.lmap(r, x)
    z95 = 1.959963984540054
    z99 = 2.5758293035489004

    # TODO: may need different CI calculation depending on purpose
    # http://www.itl.nist.gov/div898/handbook/eda/section3/autocopl.htm
    ax.axhline(y=z99 / np.sqrt(n), linestyle='--', color='lightgrey')
    ax.axhline(y=z95 / np.sqrt(n), color='lightgrey')
    ax.axhline(y=0.0, color='darkslategrey')
    ax.axhline(y=-z95 / np.sqrt(n), color='lightgrey')
    ax.axhline(y=-z99 / np.sqrt(n), linestyle='--', color='lightgrey')
    ax.set_xlabel("Lag")
    ax.set_ylabel("Autocorrelation")
    ax.plot(x, y, **plot_kws)

    plt.gcf().suptitle(
        t=measure + ' autocorrelation',
        y=0.95)

    if discrete:
        ax.set_xticks(np.arange(1, maxlag + 1))
