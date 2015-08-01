__author__ = 'lucassilva'
# -*- coding: utf-8 -*-                                                                                                                                                   
import sys
import re
from scipy.stats import zscore


def main():
    '''Main Function'''
    words = []
    arquivo = open('/home/lucasfsilva/PycharmProjects/trade_ea/game_graph/wiki_to_parser.txt', 'r').read().split('\n')
    for line in arquivo:
        if line and not re.search('\d', line.split(')')[0]):
            #print line
            source, target, value = line.replace(')',',').replace(' ','').replace('\'','').replace('(','').split(',')

            value = int(float(value))

            if value > 0 :
                words.append([source, target, value])



    arquivo = ''  # Emptying memory
    hash_all_words = {}

    for s, t, v in words:
        if s in hash_all_words:
             hash_all_words[s][t] = v
        else:
            hash_all_words[s] = {}
            hash_all_words[s][t] = v


    end_out = []

    for key, value in hash_all_words.iteritems():
        norm = zscore([target for target in value.itervalues()])
        for x,z_value in zip(value, norm):
            if z_value > 1:
                end_out.append("\t".join([key, x, str(int(z_value))]))



    saida = open('saida_write_z_maior_que_1.txt', 'w')
    saida.write('\n'.join(end_out))
    saida.close()
    print len(hash_all_words)
    print len(end_out)


if __name__ == '__main__':
    sys.exit(main())

