import unittest
from lark import Tree, Token
from interpreter.SPFInterpreter import SPFInterpreter
from interpreter.SPFException import *
from interpreter.type import Type

class TestSPFInterpreter(unittest.TestCase):

    def setUp(self):
        self.interpreter = SPFInterpreter()

    def test_declaration_without_value(self):

        tree = Tree('declaration', [
            Token('TYPE', 'booléen'),
            Token('VARIABLE', 'test')
        ])

        self.interpreter.declaration(tree)

        declaration_var = self.interpreter.symbol_table.vars[1].get('test')

        self.assertTrue(declaration_var.is_declared)
        self.assertFalse(declaration_var.is_initialized)
        self.assertEqual(declaration_var.var_value, None)
        self.assertEqual(declaration_var.var_type, Type.booleen)

        with self.assertRaises(SPFUninitializedVariable):
            self.interpreter.symbol_table.get('test')

        tree = Tree('assignation', [
            Token('VARIABLE', 'test'),
            Tree(
                Token('RULE', 'booleen'),
                [Token('BOOLEAN', 'faux')
            ])
        ])

        self.interpreter.assignation(tree)
        value = self.interpreter.symbol_table.get('test')

        self.assertFalse(value.var_value)
        self.assertTrue(declaration_var.is_declared)
        self.assertTrue(declaration_var.is_initialized)
        self.assertEqual(declaration_var.var_type, Type.booleen)