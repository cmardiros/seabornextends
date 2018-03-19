def save_to_s3(aws_creds,
               bucket_name,
               filename,
               fig=None,
               save_kws=None,
               return_public_url=None,
               return_public_url_expires=None,
               clear=False):
    """
    Save current figure to S3 and return public URL
    """
    def_save_kws = {
        'format': 'png',
        'bbox_inches': 'tight',
        'dpi': 300,
    }
    save_kws = save_kws or dict()
    save_kws = dict(def_save_kws, **save_kws)

    if not fig:
        fig = plt.gcf()

    # fig.tight_layout()

    # 5 yrs
    return_public_url_expires = return_public_url_expires or 3600 * 43800
    return_public_url = return_public_url or True

    img_data = io.BytesIO()

    fig.savefig(img_data, **save_kws)
    img_data.seek(0)

    chart_url = s3u.upload_fileobj(
        aws_creds=aws_creds,
        bucket_name=bucket_name,
        file_data=img_data,
        filename="{f}.png".format(f=filename.replace('.png', '')),
        return_public_url=return_public_url,
        return_public_url_expires=return_public_url_expires)  # 5 yrs

    if clear:
        fig.clf()
        plt.close(fig)

    return chart_url
