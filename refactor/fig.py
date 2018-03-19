class FigRetoucher(object):

    def save_to_s3(self, **kwargs):
        return mpl_utils.save_to_s3(fig=self.fig, **kwargs)
