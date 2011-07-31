import random

from django.test import TestCase

from glitchtools.map.models import Hub, Street

class StreetTestCase(TestCase):
    def setUp(self):
        self.hub = Hub.objects.create(id=1, name='hub')

    def street(self):
        return Street.objects.create(hub=self.hub, tsid=''.join(random.choice('abcdef') for i in xrange(20)), name='')

    def test_search_noop(self):
        s1 = self.street()
        def fn(street):
            return True
        self.assertEqual(s1.search(fn), (s1.id,))

    def test_search_two(self):
        s1 = self.street()
        s2 = self.street()
        s1.connections.add(s2)
        self.assertIn(s1, s2.connections.all())
        def fn(street):
            return street.id == s2.id
        self.assertEqual(s1.search(fn), (s1.id, s2.id))

    def test_search_three(self):
        s1 = self.street()
        s2 = self.street()
        s3 = self.street()
        s1.connections.add(s2)
        s2.connections.add(s3)
        def fn(street):
            return street.id == s2.id
        self.assertEqual(s1.search(fn), (s1.id, s2.id))
        def fn2(street):
            return street.id == s3.id
        self.assertEqual(s1.search(fn2), (s1.id, s2.id, s3.id))
