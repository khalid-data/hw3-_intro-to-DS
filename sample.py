import math


class Sample:

    def __init__(self, s_id, genes, label):
        """
        takes the number of sample the genes and label
        :param s_id: number of sample
        :param genes: genes
        :param label: label
        """
        self.s_id = s_id
        self.genes = genes
        self.label = label

    def compute_euclidean_distance(self, other):
        """
        coputes euclidian distance for two given points
        :param other: other samples point
        :return: the euclidian distance
        """
        g = sum([math.pow((i - j), 2) for i, j in zip(self.genes, other.genes)])
        return g ** (1 / 2)
