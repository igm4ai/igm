cpus = {{ sys.cpu.num }}
mem_size = {{ sys.memory.total | str | potc }}
os = {{ sys.os.type | str | potc }}
python = {{ sys.python | str | potc }}
{% if sys.cuda %}
cuda_version = {{ sys.cuda.version | str | potc }}
gpu_num = {{ sys.gpu.num | potc }}
{% endif %}

print('This is your first try!')
print(f'UR running {python} on {os}, with a {cpus} core {mem_size} device.')
{% if sys.cuda %}
print(f'CUDA {cuda_version} is also detected, with {gpu_num} gpu(s).')
{% endif %}
