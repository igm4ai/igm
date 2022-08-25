import json


def _load_from_file(file) -> dict:
    with open(file, 'r') as rf:
        return json.load(rf)


ONE_GPU_1_DATA = _load_from_file('test/testfile/nvidia-smi_1gpu_1.json')
ONE_GPU_2_DATA = _load_from_file('test/testfile/nvidia-smi_1gpu_2.json')
TWO_GPU_DATA = _load_from_file('test/testfile/nvidia-smi_2gpus.json')
