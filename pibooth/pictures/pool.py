# -*- coding: utf-8 -*-

import multiprocessing


class PicturesMakersPool(object):

    def __init__(self):
        self._pool = None
        self._async_results = []

    def add(self, maker):
        """Add a new picture maker and build it asyncronously.
        """
        if not self._pool:
            self._pool = multiprocessing.Pool(processes=min(multiprocessing.cpu_count(), 4))
        self._async_results.append(self._pool.apply_async(maker.build))

    def get(self):
        """Return all the results.
        """
        return [res.get() for res in self._async_results]

    def clear(self):
        """Cancel all run tasks and drop all makers.
        """
        for res in self._async_results:
            res.get(5)
        self._async_results = []

    def quit(self):
        """Quit and cleanup the pool.
        """
        if self._pool:
            self._pool.terminate()
            self._pool.join()
