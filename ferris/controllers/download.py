from google.appengine.ext.webapp.blobstore_handlers import BlobstoreDownloadHandler
from google.appengine.ext import blobstore

from ferris import Controller, route_with


class Download(Controller):
    """
    Implements the basic functionality to download a blob from the blobstore.
    To use either manually route it in routes.py::

        from ferris.controllers.download import Download
        routing.route_controller(Download)

    Or just create ``/app/controllers/download.py`` and import this::

        from ferris.controllers.download import Download

    You can then generate URLs to download files::

        self.uri("download", blob=blobkey)
        self.uri("download", blob=blobkey, save=True)
        self.uri("download-with-filename", blob=blobkey, filename="whatever.jpg")

    """
    _BlobstoreDownloadHandler__use_range_unset = object()
    get_range = BlobstoreDownloadHandler.get_range.im_func
    send_blob = BlobstoreDownloadHandler.send_blob.im_func

    @route_with(template='/download/<blob>', name='download')
    @route_with(template='/download/<blob>/<filename>', name='download-with-filename')
    def download(self, blob, filename=None):
        blob = blobstore.get(blob)

        if not blob:
            return 404

        if not filename:
            filename = blob.filename

        if 'save' in self.request.params:
            self.send_blob(blob, save_as=blob.filename)
        else:
            self.send_blob(blob)
            self.response.headers['Content-Disposition'] = (u"inline;filename=%s" % filename).encode('utf-8')

        self.response.cache_control.no_cache = None
        self.response.cache_control.max_age = 3200000
        self.response.cache_control.public = True

        return self.response
