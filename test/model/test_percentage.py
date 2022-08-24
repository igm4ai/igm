import pytest

from igm.model.percentage import Percentage


@pytest.fixture()
def per_142857():
    return Percentage('  14.2857  % ')


class _PercentagePlus(Percentage):
    pass


@pytest.fixture()
def per_plus_142857():
    return _PercentagePlus('  14.2857  % ')


@pytest.mark.unittest
class TestModelPercentage:
    def test_init(self):
        assert Percentage(1.0).ratio == pytest.approx(1.0)
        assert Percentage(0.9).ratio == pytest.approx(0.9)
        assert Percentage('99%').ratio == pytest.approx(0.99)
        assert Percentage('+99.0%').ratio == pytest.approx(0.99)
        assert Percentage('-99%').ratio == pytest.approx(-0.99)
        assert Percentage('0.888%').ratio == pytest.approx(0.00888)
        assert Percentage(Percentage('99%')).ratio == pytest.approx(0.99)
        assert Percentage(Percentage('+99%')).ratio == pytest.approx(0.99)
        assert Percentage(Percentage('-99%')).ratio == pytest.approx(-0.99)

        with pytest.raises(ValueError):
            _ = Percentage('hjadfslks')
        with pytest.raises(TypeError):
            _ = Percentage([1, 2, 3])

    def test_basic(self, per_142857):
        assert per_142857.ratio == pytest.approx(0.142857)
        assert per_142857.percentage == pytest.approx(14.2857)

    def test_int_float(self, per_142857):
        assert float(per_142857) == pytest.approx(0.142857)
        assert int(per_142857) == pytest.approx(0)

    def test_str_repr(self, per_142857, per_plus_142857):
        assert str(per_142857) == '14.29%'
        assert repr(per_142857) == '<Percentage 14.29%>'

        assert str(per_plus_142857) == '14.29%'
        assert repr(per_plus_142857) == '<_PercentagePlus 14.29%>'

    def test_cmp(self, per_142857):
        assert per_142857 > 0.1
        assert per_142857 >= 0.1
        assert per_142857 >= '10%'
        assert per_142857 < 0.2
        assert per_142857 <= 0.2
        assert per_142857 <= '20%'
        assert per_142857 != None
        assert per_142857 != 'sdfjk'
