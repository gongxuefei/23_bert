#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Han Xiao <artex.xh@gmail.com> <https://hanxiao.github.io>

import argparse
import sys

from bert.extract_features import PoolingStrategy
from service.server import BertServer


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-model_dir', type=str, default='./chinese_L-12_H-768_A-12/',
                        help='directory of a pretrained BERT model')
    parser.add_argument('-max_seq_len', type=int, default=25,
                        help='maximum length of a sequence')
    parser.add_argument('-num_worker', type=int, default=1,
                        help='number of server instances')
    parser.add_argument('-max_batch_size', type=int, default=256,
                        help='maximum number of sequences handled by each worker')
    parser.add_argument('-port', '-port_in', '-port_data', type=int, default=15555,
                        help='server port for receiving data from client')
    parser.add_argument('-port_out', '-port_result', type=int, default=15556,
                        help='server port for outputting result to client')
    parser.add_argument('-pooling_layer', type=int, nargs='+', default=[-2],
                        help='the encoder layer(s) that receives pooling. '
                             'Give a list in order to concatenate several layers into 1.')
    parser.add_argument('-pooling_strategy', type=PoolingStrategy.from_string,
                        default=PoolingStrategy.REDUCE_MEAN, choices=list(PoolingStrategy),
                        help='the pooling strategy for generating encoding vectors')

    args = parser.parse_args()
    param_str = '\n'.join(['%20s = %s' % (k, v) for k, v in sorted(vars(args).items())])
    print('usage: %s\n%20s   %s\n%s\n%s\n' % (' '.join(sys.argv), 'ARG', 'VALUE', '_' * 50, param_str))
    return args


if __name__ == '__main__':
    args = get_args()
    server = BertServer(args)
    server.start()
    server.join()
