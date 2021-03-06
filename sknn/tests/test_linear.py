import unittest
from nose.tools import (assert_is_not_none, assert_false, assert_raises, assert_equal)

import io
import pickle
import numpy

from sknn.mlp import MultiLayerPerceptronRegressor as MLPR


class TestLinearNetwork(unittest.TestCase):

    def setUp(self):
        self.nn = MLPR(layers=[("Linear",)])

    def test_LifeCycle(self):
        del self.nn

    def test_PredictUninitialized(self):
        a_in = numpy.zeros((8,16))
        assert_raises(ValueError, self.nn.predict, a_in)

    def test_FitAutoInitialize(self):
        a_in, a_out = numpy.zeros((8,16)), numpy.zeros((8,4))
        self.nn.fit(a_in, a_out)

    def test_FitWrongSize(self):
        a_in, a_out = numpy.zeros((7,16)), numpy.zeros((9,4))
        assert_raises(AssertionError, self.nn.fit, a_in, a_out)


class TestInputOutputs(unittest.TestCase):

    def setUp(self):
        self.nn = MLPR(layers=[("Linear",)])

    def test_FitOneDimensional(self):
        a_in, a_out = numpy.zeros((8,16)), numpy.zeros((8,))
        self.nn.fit(a_in, a_out)


class TestSerialization(unittest.TestCase):

    def setUp(self):
        self.nn = MLPR(layers=[("Linear",)])

    def test_SerializeFail(self):
        buf = io.BytesIO()
        assert_raises(AssertionError, pickle.dump, self.nn, buf)

    def test_SerializeCorrect(self):
        a_in, a_out = numpy.zeros((8,16)), numpy.zeros((8,4))
        self.nn.fit(a_in, a_out)

        buf = io.BytesIO()
        pickle.dump(self.nn, buf)

        buf.seek(0)
        nn = pickle.load(buf)

        assert_is_not_none(nn.mlp)
        assert_equal(nn.layers, self.nn.layers)


"""
class TestSerializedNetwork(TestLinearNetwork):

    def setUp(self):
        self.original = MLPR(layers=[("Linear",)])
        a_in, a_out = numpy.zeros((8,16)), numpy.zeros((8,4))
        self.original.initialize(a_in, a_out)

        buf = io.BytesIO()
        pickle.dump(self.original, buf)
        buf.seek(0)
        self.nn = pickle.load(buf)

    def test_PredictUninitialized(self):
        # Override base class test, this is not initialized but it
        # should be able to predict without throwing assert.
        assert_false(self.nn.is_initialized)

    def test_PredictAlreadyInitialized(self):
        a_in = numpy.zeros((8,16))
        self.nn.predict(a_in)
"""