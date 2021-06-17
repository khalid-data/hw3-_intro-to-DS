import sys
from data import Data
from agglomerativeclustering import AgglomerativeClustering
from link import SingleLink, CompletedLink

MAX_CLUSTERS = 7


def main(argv):
    """
    the main method
    it calls for all the other method and prints the requested details
    :param argv: the path to the dataset file
    :return: none
    """
    path = argv[1]
    data = Data(path)
    list_of_samples = data.create_samples()
    print("Single Link: ")
    single_link = SingleLink()
    clustering = AgglomerativeClustering(single_link, list_of_samples)
    clustering.run(MAX_CLUSTERS)
    print("")
    print("complete Link: ")
    completed_link = CompletedLink
    clustering2 = AgglomerativeClustering(completed_link, list_of_samples)
    clustering2.run(MAX_CLUSTERS)


if __name__ == '__main__':
    main(sys.argv)
