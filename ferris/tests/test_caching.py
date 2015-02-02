import time
from ferrisnose import AppEngineTest
import google
print google.__path__
from google.appengine.api import memcache
from ferris.core.caching import cache, none_sentinel_string, LocalBackend, MemcacheBackend, MemcacheChunkedBackend, DatastoreBackend, DatastoreChunkedBackend, MemcacheCompareAndSetBackend, LayeredBackend


class CacheTest(AppEngineTest):
    
    def test_cache(self):
        for backend in [LocalBackend, MemcacheBackend, MemcacheChunkedBackend, MemcacheCompareAndSetBackend, DatastoreBackend, DatastoreChunkedBackend, LayeredBackend(LocalBackend, MemcacheBackend)]:
            memcache.flush_all()
            LocalBackend.reset()

            mutators = [0, 0, 0]
            t0 = time.time()
            print 'testing %s' % backend,

            @cache('cache-test-key', backend=backend)
            def test_cached():
                mutators[0] += 1
                return mutators[0]

            # to see output of print statements, run with '--nocapture', e.g.
            #   nosetests --with-ferris --nocapture ferris/tests/test_caching.py
            print "storage overhead ~", time.time()-t0
             
            assert test_cached() == 1
            assert test_cached() == 1
            assert mutators[0] == 1
            assert backend.get('cache-test-key') == 1
            assert test_cached.uncached() == 2
            assert test_cached.cached() == 1

            test_cached.clear_cache()
            assert test_cached() == 3

            @cache('cache-test-key-none', backend=backend)
            def test_cached_with_none():
                mutators[1] += 1
                return None

            assert test_cached_with_none() is None
            assert test_cached_with_none() is None
            assert mutators[1] == 1
            assert backend.get('cache-test-key-none') == none_sentinel_string

        from random import choice
        from string import ascii_lowercase

        for backend in [MemcacheChunkedBackend, DatastoreChunkedBackend]:
            memcache.flush_all()
            print 'testing %s' % backend,
            lis=list(ascii_lowercase)
            bigobj = ''.join(choice(lis) for _ in xrange(backend.chunksize*2))
            t0 = time.time()
            
            @cache('cache-test-key-2', backend=backend)
            def test_cached():
                return bigobj
            print "big obj. storage overhead ~", time.time()-t0
            
            assert test_cached() == bigobj, "%s != %s" % (test_cached()[0:10], bigobj[0:10])
            assert test_cached() == bigobj
            assert backend.get('cache-test-key-2') == bigobj

