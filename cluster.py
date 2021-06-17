def get_s_id(sample):
    return sample.s_id


class Cluster:
    def __init__(self, cluster_id, samples):
        """
        takes the clusters id and a sample
        :param cluster_id: the clusters id
        :param samples: a list of sample objects
        """
        self.cluster_id = cluster_id
        self.samples = samples
        self.labels = []

    def merge(self, other):
        """
        this method merges at each step of the algorithem two clusters into one
        points of other will be added to self
        the new clusters id will be the smaller one
        :param other: other cluster
        :return:none
        """
        self.samples += other.samples
        self.samples = sorted(self.samples, key=get_s_id)
        self.cluster_id = min(self.cluster_id, other.cluster_id)
        del other

    def point_dist_to_cluster(self, point):
        """
        this method calculates the distance between a given point and this cluster
        :param point: given point
        :return:distance
        """
        distance_sum = 0
        for other_point in self.samples:
            distance_sum += point.compute_euclidean_distance(other_point)
        return distance_sum / len(self.samples)

    def dominant_label(self):
        """
        find the most popular label in the cluster
        :return: the most popular label
        """
        for sample in set(self.samples):
            self.labels.append((sample.label, 1))
        result = {}
        for label, value in self.labels:
            total = result.get(label, 0) + value
            result[label] = total
        max_ = 0
        label = ""
        for key in result.keys():
            if result[key] > max_:
                label = key
                max_ = result[key]
        return label

    def print_details(self, silhouette):
        sample_id_list = []
        for sample in self.samples:
            sample_id_list.append(sample.s_id)
        print('Cluster {0}: {1}, dominant label = {2}, silhouette = {3:.3f}'
              .format(self.cluster_id, sample_id_list, self.dominant_label(), silhouette))
