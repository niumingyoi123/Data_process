import numpy as np
from result_plot.basic_geographical import *
class tradition_al:

    @staticmethod
    def g_spd(t1, t2):
        """
        Usage
        -----
        The spd-distance of trajectory t2 from trajectory t1
        The spd-distance is the sum of the all the point-to-path distance of points of t1 from trajectory t2

        Parameters
        ----------
        param t1 :  len(t1)x2 numpy_array
        param t2 :  len(t2)x2 numpy_array

        Returns
        -------
        spd : float
               spd-distance of trajectory t2 from trajectory t1
        """
        n0 = len(t1)
        n1 = len(t2)
        lats0 = t1[:, 1]
        lons0 = t1[:, 0]
        lats1 = t2[:, 1]
        lons1 = t2[:, 0]
        dist = 0
        for j in range(n1):
            dist_j0 = 9e100
            for i in range(n0 - 1):
                dist_j0 = np.min((dist_j0, point_to_path(lons0[i], lats0[i], lons0[i + 1], lats0[i + 1], lons1[j],
                                                         lats1[j])))
            dist = dist + dist_j0
        dist = float(dist) / n1
        return dist

    @staticmethod
    def g_sspd(t1, t2):
        """
        Usage
        -----
        The sspd-distance between trajectories t1 and t2.
        The sspd-distance is the mean of the spd-distance between of t1 from t2 and the spd-distance of t2 from t1.

        Parameters
        ----------
        param t1 :  len(t1)x2 numpy_array
        param t2 :  len(t2)x2 numpy_array

        Returns
        -------
        sspd : float
                sspd-distance of trajectory t2 from trajectory t1
        """
        dist = tradition_al.g_spd(t1, t2) + tradition_al.g_spd(t2, t1)
        return dist

    @staticmethod
    def g_dtw(t0, t1):
        """
        Usage
        -----
        The Dynamic-Time Warping distance between trajectory t0 and t1.

        Parameters
        ----------
        param t0 : len(t0)x2 numpy_array
        param t1 : len(t1)x2 numpy_array

        Returns
        -------
        dtw : float
              The Dynamic-Time Warping distance between trajectory t0 and t1
        """
        n0 = len(t0)
        n1 = len(t1)
        C = np.zeros((n0 + 1, n1 + 1))
        C[1:, 0] = float('inf')
        C[0, 1:] = float('inf')
        for i in np.arange(n0) + 1:
            for j in np.arange(n1) + 1:
                C[i, j] = great_circle_distance(t0[i - 1][0], t0[i - 1][1], t1[j - 1][0], t1[j - 1][1]) + min(
                    C[i, j - 1], C[i - 1, j - 1], C[i - 1, j])
        dtw = C[n0, n1]
        return dtw

    @staticmethod
    def g_lcss(t0, t1, eps):
        """
        Usage
        -----
        The Longuest-Common-Subsequence distance between trajectory t0 and t1.

        Parameters
        ----------
        param t0 : len(t0)x2 numpy_array
        param t1 : len(t1)x2 numpy_array
        eps : float

        Returns
        -------
        lcss : float
               The Longuest-Common-Subsequence distance between trajectory t0 and t1
        """
        n0 = len(t0)
        n1 = len(t1)
        # An (m+1) times (n+1) matrix
        C = [[0] * (n1 + 1) for _ in range(n0 + 1)]
        for i in range(1, n0 + 1):
            for j in range(1, n1 + 1):
                if great_circle_distance(t0[i - 1, 0], t0[i - 1, 1], t1[j - 1, 0], t1[j - 1, 1]) < eps:
                    C[i][j] = C[i - 1][j - 1] + 1
                else:
                    C[i][j] = max(C[i][j - 1], C[i - 1][j])
        lcss = 1 - float(C[n0][n1]) / min([n0, n1])
        return lcss

    @staticmethod
    def g_directed_hausdorff(t1, t2):
        """
        Usage
        -----
        directed hausdorff distance from trajectory t1 to trajectory t2.

        Parameters
        ----------
        param t1 :  len(t1)x2 numpy_array
        param t2 :  len(t2)x2 numpy_array

        Returns
        -------
        dh : float, directed hausdorff from trajectory t1 to trajectory t2
        """
        n0 = len(t1)
        n1 = len(t2)
        dh = 0
        for j in range(n1):
            dist_j0 = 9e100
            for i in range(n0 - 1):
                dist_j0 = min(dist_j0,
                              point_to_path(t1[i][0], t1[i][1], t1[i + 1][0], t1[i + 1][1], t2[j][0], t2[j][1]))
            dh = max(dh, dist_j0)
        return dh

    @staticmethod
    def g_hausdorff(t1, t2):
        """
        Usage
        -----
        hausdorff distance between trajectories t1 and t2.

        Parameters
        ----------
        param t1 :  len(t1)x2 numpy_array
        param t2 :  len(t2)x2 numpy_array

        Returns
        -------
        h : float, hausdorff from trajectories t1 and t2
        """
        h = max(tradition_al.g_directed_hausdorff(t1, t2), tradition_al.g_directed_hausdorff(t2, t1))
        return h

    @staticmethod
    def g_erp(t0, t1, g):
        """
        Usage
        -----
        The Edit distance with Real Penalty between trajectory t0 and t1.

        Parameters
        ----------
        param t0 : len(t0)x2 numpy_array
        param t1 : len(t1)x2 numpy_array

        Returns
        -------
        dtw : float
              The Dynamic-Time Warping distance between trajectory t0 and t1
        """
        n0 = len(t0)
        n1 = len(t1)
        C = np.zeros((n0 + 1, n1 + 1))

        C[1:, 0] = sum(map(lambda x: abs(great_circle_distance(g[0], g[1], x[0], x[1])), t0))
        C[0, 1:] = sum(map(lambda y: abs(great_circle_distance(g[0], g[1], y[0], y[1])), t1))
        for i in np.arange(n0) + 1:
            for j in np.arange(n1) + 1:
                derp0 = C[i - 1, j] + great_circle_distance(t0[i - 1][0], t0[i - 1][1], g[0], g[1])
                derp1 = C[i, j - 1] + great_circle_distance(g[0], g[1], t1[j - 1][0], t1[j - 1][1])
                derp01 = C[i - 1, j - 1] + great_circle_distance(t0[i - 1][0], t0[i - 1][1], t1[j - 1][0], t1[j - 1][1])
                C[i, j] = min(derp0, derp1, derp01)
        erp = C[n0, n1]
        return erp

    @staticmethod
    def g_edr(t0, t1, eps):
        """
        Usage
        -----
        The Edit Distance on Real sequence between trajectory t0 and t1.

        Parameters
        ----------
        param t0 : len(t0)x2 numpy_array
        param t1 : len(t1)x2 numpy_array
        eps : float

        Returns
        -------
        edr : float
               The Longuest-Common-Subsequence distance between trajectory t0 and t1
        """
        n0 = len(t0)
        n1 = len(t1)
        # An (m+1) times (n+1) matrix
        C = [[0] * (n1 + 1) for _ in range(n0 + 1)]
        for i in range(1, n0 + 1):
            for j in range(1, n1 + 1):
                if great_circle_distance(t0[i - 1][0], t0[i - 1][1], t1[j - 1][0], t1[j - 1][1]) < eps:
                    subcost = 0
                else:
                    subcost = 1
                C[i][j] = min(C[i][j - 1] + 1, C[i - 1][j] + 1, C[i - 1][j - 1] + subcost)
        edr = float(C[n0][n1]) / max([n0, n1])
        return edr
