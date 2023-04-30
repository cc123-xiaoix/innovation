#! /usr/bin/env python
# -*- coding: utf-8 -*_
# Author: Yunlong Feng <ylfeng@ir.hit.edu.cn>

import torch

_TORCH_MAJOR, _TORCH_MINOR = map(int, torch.__version__.split('.')[0:2])

if _TORCH_MAJOR < 1 or (_TORCH_MAJOR == 1 and _TORCH_MINOR < 8):
    from torch._six import container_abcs
else:
    import collections.abc as container_abcs


def map2device(batch, device=torch.device('cpu')):
    batch_type = type(batch)
    if isinstance(batch, torch.Tensor):
        return batch.to(device)
    elif isinstance(batch, container_abcs.Mapping):
        return {key: map2device(batch[key], device=device) for key in batch}
    elif isinstance(batch, tuple) and hasattr(batch, '_fields'):  # namedtuple
        return batch_type(*(map2device(samples, device=device) for samples in zip(*batch)))
    elif isinstance(batch, container_abcs.Sequence):
        return [map2device(it, device=device) for it in batch]
    else:
        return batch


def convert2npy(batch):
    batch_type = type(batch)
    if isinstance(batch, torch.Tensor):
        return map2device(batch).numpy()
    elif isinstance(batch, container_abcs.Mapping):
        return {key: convert2npy(batch[key]) for key in batch}
    elif isinstance(batch, tuple) and hasattr(batch, '_fields'):  # namedtuple
        return batch_type(*(convert2npy(samples) for samples in zip(*batch)))
    elif isinstance(batch, container_abcs.Sequence):
        return [convert2npy(it) for it in batch]
    else:
        return batch
