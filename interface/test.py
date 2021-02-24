import unittest
import json
from cerberus import Validator
from schema import load_schema

v = Validator()

tests = [
    {
        'file': 'simple_validation',
        'passing': [
            [[1]],
            [[], []],
        ],
        'failing': [
            [1, 1],
            [1.0, 2.0],
            ['a', 'a'],
            [{}, {}],
            [[[1]]],
            [[[[1]]]],
            [{"b64": "a"}],
            [{"tag": "a", "image": "a"}],
            [{"b64": "a", "tag": "a", "image": "a"}],
            [[[[[1]]]]],
            ['a', 1],
        ],
    },
    {
        'file': 'tf_validation',
        'passing': [
            [[1]],
            [1, 1],
            [1.0, 2.0],
            ['a', 'a'],
            [{}, {}],
            [[], []],
            [[[1]]],
            [[[[1]]]],
            [{"b64": "a"}],
            [{"tag": "a", "image": "a"}],
        ],
        'failing': [
            [{"b64": "a", "tag": "a", "image": "a"}],
            [[[[[1]]]]],
            ['a', 1],
        ],
    },
    {
        'file': 'custom_validation',
        'passing': [
            [{}, {}],
            [{"b64": "a"}],
            [{"tag": "a", "image": "a"}],
            [{"b64": "a", "tag": "a", "image": "a"}],
        ],
        'failing': [
            [[1]],
            [1, 1],
            [1.0, 2.0],
            ['a', 'a'],
            [[], []],
            [[[1]]],
            [[[[1]]]],
            [[[[[1]]]]],
            ['a', 1],
        ],
    },
]

def test_array(array, schema, value):
    for item in array:
        instances = {'instances': item}
        validation = v.validate(instances, schema)
        print('test {} -> {}'.format(json.dumps(item), validation))
        if validation != value:
            return False
    return True

class Test(unittest.TestCase):
    def test(self):
        for test in tests:
            file = test['file']
            schema = load_schema(file)
            print(schema)
            self.assertTrue(test_array(test['passing'], schema, True))
            self.assertTrue(test_array(test['failing'], schema, False))

if __name__ == '__main__':
    unittest.main()
