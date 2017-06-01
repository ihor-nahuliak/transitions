try:
    from builtins import object
except ImportError:
    pass
from transitions.extensions import MachineFactory
import sys
if sys.version_info < (2, 7):
    from unittest2 import TestCase
else:
    from unittest import TestCase


class TestFactory(TestCase):

    def setUp(self):
        self.factory = MachineFactory()

    def test_mixins(self):
        machine_cls = self.factory.get_predefined()
        self.assertFalse(hasattr(machine_cls, 'set_edge_state'))

        graph_cls = self.factory.get_predefined(graph=True)
        self.assertTrue(hasattr(graph_cls, 'set_edge_state'))
        nested_cls = self.factory.get_predefined(nested=True)
        self.assertFalse(hasattr(nested_cls, 'set_edge_state'))
        self.assertTrue(hasattr(nested_cls, 'traverse'))

        locked_cls = self.factory.get_predefined(locked=True)
        self.assertFalse(hasattr(locked_cls, 'set_edge_state'))
        self.assertFalse(hasattr(locked_cls, 'traverse'))
        self.assertTrue('__getattribute__' in locked_cls.__dict__)

        locked_nested_cls = self.factory.get_predefined(nested=True, locked=True)
        self.assertFalse(hasattr(locked_nested_cls, 'set_edge_state'))
        self.assertTrue(hasattr(locked_nested_cls, 'traverse'))
        self.assertEqual(locked_nested_cls.__getattribute__, locked_cls.__getattribute__)
        self.assertNotEqual(machine_cls.__getattribute__, locked_cls.__getattribute__)

        graph_locked_cls = self.factory.get_predefined(graph=True, locked=True)
        self.assertTrue(hasattr(graph_locked_cls, 'set_edge_state'))
        self.assertEqual(graph_locked_cls.__getattribute__, locked_cls.__getattribute__)

        graph_nested_cls = self.factory.get_predefined(graph=True, nested=True)
        self.assertNotEqual(nested_cls._create_transition, graph_nested_cls._create_transition)

        locked_nested_graph_cls = self.factory.get_predefined(nested=True, locked=True, graph=True)
        self.assertNotEqual(locked_nested_graph_cls._create_event, graph_cls._create_event)
