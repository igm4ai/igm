from typing import Union, List

from hbutils.string import plural_word

from ...model import MappingBasedModel, MemoryStatus, GenericCollection


class GPUCollection(GenericCollection):
    def __getitem__(self, item) -> Union[List['GPU'], 'GPU']:
        return GenericCollection.__getitem__(self, item)

    def __str__(self):
        return GenericCollection.__str__(self)

    def __repr__(self):
        return f'<{type(self).__name__} {plural_word(len(self), "gpu")}>'


class NvidiaMemoryStatus(MemoryStatus):
    def __init__(self, data):
        MemoryStatus.__init__(self, data['total'], data['used'], data['free'])


class FBMemoryUsage(NvidiaMemoryStatus):
    pass


class GPU(MappingBasedModel):
    def __init__(self, data):
        MappingBasedModel.__init__(self, data)

    @property
    def id(self) -> str:
        return self['@id']

    @property
    def product_name(self) -> str:
        return self['product_name']

    @property
    def memory(self) -> FBMemoryUsage:
        return FBMemoryUsage(self["fb_memory_usage"])

    def __repr__(self):
        return f'<{type(self).__name__} {self.product_name}, {self.memory.total}>'
