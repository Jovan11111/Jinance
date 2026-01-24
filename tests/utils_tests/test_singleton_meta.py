from utils.singleton_meta import SingletonMeta


class TestSingleton:
    """Test class for SingletonMeta metaclass."""

    def test__create_2_singeltons__they_are_the_same(self):
        """Test that only one instance is created."""

        class TestClass(metaclass=SingletonMeta):
            def __init__(self, value):
                self.value = value

        instance1 = TestClass(67)
        assert instance1.value == 67

        instance2 = TestClass(69)
        assert instance2 is instance1
        assert instance2.value == 67

    def test__create_2_singeltons_get_instance__they_are_the_same(self):
        """Test the get_instance class method."""

        class TestClass(metaclass=SingletonMeta):
            def __init__(self, value):
                self.value = value

        TestClass.clear()

        instance1 = TestClass.get_instance(67)
        assert instance1.value == 67

        instance2 = TestClass.get_instance(69)
        assert instance2 is instance1
        assert instance2.value == 67

    def test__create_singleton_after_clear__different_class_then_before_clear(self):
        """Test the clear method resets the instance."""

        class TestClass(metaclass=SingletonMeta):
            def __init__(self, value):
                self.value = value

        instance1 = TestClass(67)
        instance2 = TestClass(69)
        assert instance1 is instance2

        TestClass.clear()

        instance3 = TestClass(68)
        assert instance3 is not instance1
        assert instance3.value == 68
