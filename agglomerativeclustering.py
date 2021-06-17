

from cluster import Cluster


def in_x(sample, this_cluster):
    """
    static method that calculates one points distance from all other points that shares the same cluster
    :param sample: a sample
    :param this_cluster: this cluster
    :return: distance/ the clusters points number -1
    """
    dist_sum = 0
    for other_sample in this_cluster.samples:
        if sample == other_sample:
            continue
        dist_sum += sample.compute_euclidean_distance(other_sample)
    return dist_sum / (len(this_cluster.samples) - 1)


class AgglomerativeClustering:

    def __init__(self, link, samples):
        """
        takes link which is either single or completed link
        the constructore initiates cluster list
        :param link: single or completed link
        :param samples: samples
        """
        self.link = link
        self.clusters = []
        for sample in samples:
            temp_list = [sample]
            self.clusters.append(Cluster(sample.s_id, temp_list))

    def out_x(self, sample, this_cluster):
        """
        calculates the points distance from other clusters
        :param sample: sample
        :param this_cluster: the cluster the point is from
        :return: minimal distance from other cluster
        """
        dist_list = []
        for other_cluster in self.clusters:
            if other_cluster == this_cluster:
                continue
            dist_list.append(other_cluster.point_dist_to_cluster(sample))
        return min(dist_list)

    def compute_silhoeutte(self):
        """
        this method computes makes dictionary thats keys are all the samples
        and the values are the sillhoute of sample i
        :return: the dictionary
        """
        sample_silhoeutte_dict = {}
        for cluster in self.clusters:
            cluster_size = len(cluster.samples)
            for sample in cluster.samples:
                if cluster_size <= 1:
                    sample_silhoeutte_dict[sample.s_id] = 0
                    continue
                in_sample = in_x(sample, cluster)
                out_sample = self.out_x(sample, cluster)
                sample_silhoeutte = (out_sample - in_sample) / (max(in_sample, out_sample))
                sample_silhoeutte_dict[sample.s_id] = sample_silhoeutte
            return sample_silhoeutte_dict

    def compute_summery_silhoeutte(self):
        """
        the method returns a dictionary that includes all the silhoutte for the agglomerative algorithm
        :return: the dictionary
        """
        samples_silhoeutte_dict = self.compute_silhoeutte()
        cluster_silhoeutte_dict = {}
        total_data_silhoeutte = 0
        total_data_size = 0
        for cluster in self.clusters:
            cluster_silhoeutte_sum = 0
            cluster_size = len(cluster.samples)
            for sample in cluster.samples:
                if sample.s_id in samples_silhoeutte_dict:
                    temp = samples_silhoeutte_dict[sample.s_id]
                    cluster_silhoeutte_sum += temp
            cluster_silhoeutte_dict[cluster.cluster_id] = cluster_silhoeutte_sum / cluster_size
            total_data_silhoeutte += cluster_silhoeutte_sum
            total_data_size += cluster_size
        cluster_silhoeutte_dict[0] = total_data_silhoeutte / total_data_size
        return cluster_silhoeutte_dict

    def compute_true_possitive(self):
        """
        this method calculates the true possitive and returns it
        :return: true possitive
        """
        TP = 0
        calculated_sample = []
        for cluster in self.clusters:
            for sample in cluster.samples:
                for other_sample in cluster.samples:
                    if (other_sample in calculated_sample) or (sample == other_sample):
                        continue
                    if sample.label == other_sample.label:
                        TP += 1
                calculated_sample.append(sample)
        return TP

    def compute_false_possitive(self):
        """
        this method calculates the FALSE possitive and returns it
        :return: FALSE POSSITIVE
        """
        FP = 0
        calculated_sample = []
        for cluster in self.clusters:
            for sample in cluster.samples:
                for other_sample in cluster.samples:
                    if (other_sample in calculated_sample) or (sample == other_sample):
                        continue
                    if sample.label != other_sample.label:
                        FP += 1
                calculated_sample.append(sample)
        return FP

    def compute_true_negative(self):
        """
        this method calculates the true negative and returns it
        :return: true negative
        """
        TN = 0
        calculated_clusters = []
        for this_cluster in self.clusters:
            for sample in this_cluster.samples:
                for other_cluster in self.clusters:
                    if (other_cluster in calculated_clusters) or (other_cluster == this_cluster):
                        continue
                    for other_sample in other_cluster.samples:
                        if other_sample.label != sample.label:
                            TN += 1
                calculated_clusters.append(this_cluster)
            return TN

    def compute_false_negative(self):
        """
        this method calculates the FALSE negative and returns it
        :return: FALSE negative
        """
        FN = 0
        calculated_clusters = []
        for this_cluster in self.clusters:
            for sample in this_cluster.samples:
                for other_cluster in self.clusters:
                    if (other_cluster in calculated_clusters) or (other_cluster == this_cluster):
                        continue
                    for other_sample in other_cluster.samples:
                        if other_sample.label == sample.label:
                            FN += 1
                calculated_clusters.append(this_cluster)
            return FN

    def rand_index(self):
        """
        this method calculates the rand index for the algorithm
        :return: the rand index
        """
        TP = self.compute_true_possitive()
        TN = self.compute_true_negative()
        FP = self.compute_false_possitive()
        FN = self.compute_false_negative()
        return (TP + TN) / (TP + TN + FP + FN)

    def print_question_details(self):
        """
        this method prints what is supposed to for the question
        int computes the silhoutte and rand index and prints them
        :return: none
        """
        cluster_sil_dict = self.compute_summery_silhoeutte()
        for cluster in self.clusters:
            cluster_silhoeutte = cluster_sil_dict[cluster.cluster_id]
            cluster.print_details(cluster_silhoeutte)
        total_data_silhoeutte = cluster_sil_dict[0]
        rand_index = self.rand_index()
        print("Whole data: silhouette = {0:.3f}, RI = {1:.3f}\n".format(total_data_silhoeutte, rand_index))

    def run(self, max_clusters):
        """
        this method runs the agglomarative clustering algo so the num of clusters as less than MAX CLUSTER
        the method prints whats needed
        :param max_clusters: the maximum number of clusters
        :return: none
        """
        num_of_clusters = len(self.clusters)
        while num_of_clusters > max_clusters:
            min_dist = None
            this_cluster = None
            other_cluster = None
            for i in range(num_of_clusters):
                for j in range(i + 1, num_of_clusters):
                    temp = self.link.compute(self.clusters[i], self.clusters[j])
                    if (min_dist is None) or (temp < min_dist):
                        min_dist = temp
                        this_cluster = i
                        other_cluster = j
            self.clusters[this_cluster].merge(self.clusters[other_cluster])
            self.clusters.pop(other_cluster)
            num_of_clusters -= 1
        self.print_question_details()
