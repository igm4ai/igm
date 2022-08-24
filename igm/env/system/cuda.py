from .gpu import GPU, GPUCollection
from ...model import VersionInfo, MappingBasedModel


class CUDAVersion(VersionInfo):
    pass


class NvidiaDriverVersion(VersionInfo):
    pass


class CUDA(MappingBasedModel):
    def __init__(self, nvidia_data: dict):
        MappingBasedModel.__init__(self, nvidia_data["nvidia_smi_log"])

    @property
    def version(self) -> CUDAVersion:
        return CUDAVersion(self["cuda_version"])

    @property
    def driver_version(self) -> NvidiaDriverVersion:
        return NvidiaDriverVersion(self["driver_version"])

    @property
    def gpus(self) -> GPUCollection:
        gpu_list = self.get('gpu', None)
        if not gpu_list:
            return GPUCollection([])
        elif isinstance(gpu_list, dict):
            assert int(self.get("attached_gpus", 0)) == 1
            return GPUCollection([GPU(gpu_list)])
        else:
            assert int(self.get("attached_gpus", 0)) == len(gpu_list)
            return GPUCollection([GPU(item) for item in gpu_list])

    def _str_format(self):
        return f'<{type(self).__name__} {self.version}>'

    def __str__(self):
        return self._str_format()

    def __repr__(self):
        return self._str_format()
