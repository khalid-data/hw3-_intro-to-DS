import pandas
from sample import Sample

TYPE_KEY = 'type'
SAMPLES_KEY = 'samples'


class Data:

    def __init__(self, path):
        """
        takes dataset file and makes a dictionary from thw data
        :param path: the data set path
        """
        df = pandas.read_csv(path)
        self.data = df.to_dict(orient="list")

    def create_samples(self):
        """
        makes a list of samples from the data set
        :return: list of samples
        """
        list_length = len(self.data[TYPE_KEY])
        list_of_samples = []
        for i in range(list_length):
            sample_label = self.data[TYPE_KEY][i]
            sample_id = self.data[SAMPLES_KEY][i]
            gene_list = []
            for key in self.data:
                if (key != TYPE_KEY) and (key != SAMPLES_KEY):
                    gene_list.append(self.data[key][i])
            list_of_samples.append(Sample(sample_id, gene_list, sample_label))
        return list_of_samples
