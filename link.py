class Link:
    def compute(self, this_cluster, other_cluster):
        """
        taked the cluster id and the samples
        :param this_cluster: this cluster
        :param other_cluster: another cluster
        :return: none
        """
        pass


class SingleLink(Link):
    """
    this method rides the method on class Link
    it returns the minimal distance between two pionts from the two clusters given
    """
    def compute(self, this_cluster, other_cluster):
        dist_list = []
        for this_sample in this_cluster.samples:
            for other_sample in other_cluster.samples:
                dist_list.append(this_sample.compute_euclidean_distance(other_sample))
        return min(dist_list)


class CompletedLink(Link):

    def compute(self, this_cluster, other_cluster):
        """
        this method rides the method on class Link
        it returns the maximal distance between two points from the two clusters given
        """
        dist_List = []
        for this_sample in this_cluster.samples:
            for other_sample in other_cluster.samples:
                dist_List.append(this_sample.compute_euclidean_distance(other_sample))
        return max(dist_List)
