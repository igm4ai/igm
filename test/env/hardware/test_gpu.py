import pytest


@pytest.mark.unittest
class TestEnvHardwareGpu:
    def test_gpu_collection_len(self, cuda_1gpu_1, cuda_1gpu_2, cuda_2gpus):
        assert len(cuda_1gpu_1.gpus) == 1
        assert len(cuda_1gpu_2.gpus) == 1
        assert len(cuda_2gpus.gpus) == 2

        assert cuda_1gpu_1.gpus.num == 1
        assert cuda_1gpu_2.gpus.num == 1
        assert cuda_2gpus.gpus.num == 2

    def test_gpu_collection_str_repr(self, cuda_1gpu_1, cuda_1gpu_2, cuda_2gpus):
        assert str(cuda_1gpu_1.gpus) == '<GPUCollection 1 gpu>'
        assert str(cuda_1gpu_2.gpus) == '<GPUCollection 1 gpu>'
        assert str(cuda_2gpus.gpus) == '<GPUCollection 2 gpus>'

    def test_gpu_info(self, cuda_1gpu_1, cuda_1gpu_2, cuda_2gpus):
        assert cuda_1gpu_1.gpus[0].id == '00000000:2B:00.0'
        assert cuda_1gpu_2.gpus[0].id == '00000000:01:00.0'
        assert cuda_2gpus.gpus[0].id == '00000000:25:00.0'
        assert cuda_2gpus.gpus[1].id == '00000000:50:00.0'

        assert cuda_1gpu_1.gpus[0].uuid == 'GPU-cbfd8a17-9022-e1b9-ec1b-3286614c287e'
        assert cuda_1gpu_2.gpus[0].uuid == 'GPU-dea351ca-cb1a-5263-51c0-e73ff2f4ad1c'
        assert cuda_2gpus.gpus[0].uuid == 'GPU-6c7fbd63-1ece-3d5a-cb2e-e554469f949b'
        assert cuda_2gpus.gpus[1].uuid == 'GPU-d1824ae0-d312-b822-c6f5-be822f9eecc6'

        assert cuda_1gpu_1.gpus[0].name == 'NVIDIA GeForce RTX 2060'
        assert cuda_1gpu_2.gpus[0].name == 'Quadro P620'
        assert cuda_2gpus.gpus[0].name == 'A100-SXM-80GB'
        assert cuda_2gpus.gpus[1].name == 'A100-SXM-80GB'

        assert cuda_1gpu_1.gpus[0].brand == 'GeForce'
        assert cuda_1gpu_2.gpus[0].brand == 'Quadro'
        assert cuda_2gpus.gpus[0].brand == 'Tesla'
        assert cuda_2gpus.gpus[1].brand == 'Tesla'

    def test_gpu_memory(self, cuda_1gpu_1, cuda_1gpu_2, cuda_2gpus):
        assert cuda_1gpu_1.gpus[0].memory.total == 12604932096
        assert cuda_1gpu_1.gpus[0].memory.used == 146800640
        assert cuda_1gpu_1.gpus[0].memory.free == 12458131456

        assert cuda_1gpu_2.gpus[0].memory.total == 4294967296
        assert cuda_1gpu_2.gpus[0].memory.used == 62914560
        assert cuda_1gpu_2.gpus[0].memory.free == 4153409536

        assert cuda_2gpus.gpus[0].memory.total == 85197848576
        assert cuda_2gpus.gpus[0].memory.used == 3145728
        assert cuda_2gpus.gpus[0].memory.free == 85194702848

        assert cuda_2gpus.gpus[1].memory.total == 85197848576
        assert cuda_2gpus.gpus[1].memory.used == 3145728
        assert cuda_2gpus.gpus[1].memory.free == 85194702848

    def test_gpu_str(self, cuda_1gpu_1, cuda_1gpu_2, cuda_2gpus):
        assert str(cuda_1gpu_1.gpus[0]) == '<GPU NVIDIA GeForce RTX 2060, ' \
                                           'GPU-cbfd8a17-9022-e1b9-ec1b-3286614c287e, 11.74 GiB>'
        assert str(cuda_1gpu_2.gpus[0]) == '<GPU Quadro P620, GPU-dea351ca-cb1a-5263-51c0-e73ff2f4ad1c, 4.00 GiB>'
        assert str(cuda_2gpus.gpus[0]) == '<GPU Tesla A100-SXM-80GB, ' \
                                          'GPU-6c7fbd63-1ece-3d5a-cb2e-e554469f949b, 79.35 GiB>'
        assert str(cuda_2gpus.gpus[1]) == '<GPU Tesla A100-SXM-80GB, ' \
                                          'GPU-d1824ae0-d312-b822-c6f5-be822f9eecc6, 79.35 GiB>'

    def test_gpu_repr(self, cuda_1gpu_1, cuda_1gpu_2, cuda_2gpus):
        assert repr(cuda_1gpu_1.gpus[0]) == '<GPU NVIDIA GeForce RTX 2060, ' \
                                            'GPU-cbfd8a17-9022-e1b9-ec1b-3286614c287e, 11.74 GiB>'
        assert repr(cuda_1gpu_2.gpus[0]) == '<GPU Quadro P620, GPU-dea351ca-cb1a-5263-51c0-e73ff2f4ad1c, 4.00 GiB>'
        assert repr(cuda_2gpus.gpus[0]) == '<GPU Tesla A100-SXM-80GB, ' \
                                           'GPU-6c7fbd63-1ece-3d5a-cb2e-e554469f949b, 79.35 GiB>'
        assert repr(cuda_2gpus.gpus[1]) == '<GPU Tesla A100-SXM-80GB, ' \
                                           'GPU-d1824ae0-d312-b822-c6f5-be822f9eecc6, 79.35 GiB>'
