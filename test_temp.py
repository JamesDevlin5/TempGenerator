#!/usr/bin/env python3

from temp import *


def test_countname():
    gen = CountNameGen()
    assert "1" == gen.name()
    assert "2" == gen.name()
    assert "3" == gen.name()
    assert "4" == gen.name()
    assert "5" == gen.name()


def test_uuidname():
    gen = UuidNameGen()
    assert 32 == len(gen.name())


def test_unique():
    for gen in (TmpGen(), TmpGen(CountNameGen())):
        for _ in range(100):
            assert not gen._get_unique().exists()
