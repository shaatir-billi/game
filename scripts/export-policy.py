"""Export the fixed PPO actor tensors with Python's standard library."""
import collections
import hashlib
import io
import json
import math
from pathlib import Path
import pickle
import struct
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def rebuild(storage, offset, shape, stride, *_):
    def read(axis, index):
        if axis == len(shape):
            return storage[index]
        return [read(axis + 1, index + i * stride[axis]) for i in range(shape[axis])]
    return read(0, offset)


class TensorReader(pickle.Unpickler):
    def find_class(self, module, name):
        allowed = {
            ('collections', 'OrderedDict'): collections.OrderedDict,
            ('torch', 'FloatStorage'): 'float32',
            ('torch._utils', '_rebuild_tensor_v2'): rebuild,
        }
        if (module, name) not in allowed:
            raise ValueError(f'Unsupported tensor class: {module}.{name}')
        return allowed[module, name]

    def persistent_load(self, identifier):
        kind, dtype, key, device, size = identifier
        if kind != 'storage' or dtype != 'float32' or device != 'cpu':
            raise ValueError('Expected a CPU float32 storage')
        return struct.unpack(f'<{size}f', self.archive.read(f'archive/data/{key}'))


source = ROOT / 'marl_model.zip'
with zipfile.ZipFile(source) as model:
    with zipfile.ZipFile(io.BytesIO(model.read('policy.pth'))) as archive:
        reader = TensorReader(io.BytesIO(archive.read('archive/data.pkl')))
        reader.archive = archive
        tensors = reader.load()

layers = []
for prefix in ['mlp_extractor.policy_net.0', 'mlp_extractor.policy_net.2', 'action_net']:
    layers.append({'weight': tensors[prefix + '.weight'], 'bias': tensors[prefix + '.bias']})
assert [(len(l['bias']), len(l['weight'][0])) for l in layers] == [(64, 8), (64, 64), (7, 64)]
policy = {'sourceSha256': hashlib.sha256(source.read_bytes()).hexdigest(), 'layers': layers}
(ROOT / 'web/policy.json').write_text(json.dumps(policy, separators=(',', ':')) + '\n')

# Reference logits for observations in both halves of the map.
fixtures = []
for observation in [[100, 690, 2710, 706, 1350, 436, 2900, 506],
                    [3200, 690, 3000, 706, 1700, 436, 3200, 506],
                    [750, 50, 1000, 100, 2000, 436, 3400, 506]]:
    values = observation
    for index, layer in enumerate(layers):
        values = [sum(w * x for w, x in zip(row, values)) + bias
                  for row, bias in zip(layer['weight'], layer['bias'])]
        if index < 2:
            values = [math.tanh(value) for value in values]
    fixtures.append({'observation': observation, 'logits': values})
(ROOT / 'tests/policy-fixtures.json').write_text(json.dumps(fixtures, indent=2) + '\n')
print('Exported PPO actor: 8 inputs, 64 + 64 hidden units, 7 action logits')
