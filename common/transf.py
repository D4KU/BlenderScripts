import numpy as np


def normalize(v):
    """
    Normalize a given vector to length one.

    Parameters
    ----------
    v : Iterable
        Vector of arbitrary dimension.

    Returns
    -------
    v : numpy.ndarray
        Input vector rescaled to length one.
    """
    l = np.linalg.norm(v)
    return v if l == 0 else v / l


def homog_vecs(vecs):
    """
    Transform a vector list from Cartesian into homogeneous coordinates
    by adding a coordinate equal to one to every vector.

    Parameters
    ----------
    vecs : Iterable
        Vector list to homogenize.

    Returns
    -------
    hvecs : numpy.ndarray
        Copy of 'vecs' with homogenized coordinates.

    Examples
    --------
    >>> homog_vecs([[0, 1, 2], [3, 4, 5]])
    array([[0, 1, 2, 1], [3, 4, 5, 1]])
    """
    vs = np.asanyarray(vecs)
    hvecs = np.ones(np.add(vs.shape, (0, 1)), dtype=vs.dtype)
    hvecs[:, :-1] = vs
    return hvecs


def transf_vecs(mat, vecs):
    """
    Apply a transformation matrix to every vector in a list.

    Parameters
    ----------
    mat : Iterable
        4x4 transformation matrix to apply to every vector
    vecs : Iterable
        List of 3D vertices

    Returns
    -------
    vecs : numpy.ndarray
        Copy of 'vecs' with transformed coordinates
    """
    return (np.asanyarray(mat) @ homog_vecs(vecs).T).T[:, :3]


def transf_point(mat, point):
    """
    Apply a transformation matrix to a point.

    Parameters
    ----------
    mat : Iterable
        4x4 transformation matrix to apply.
    point : Iterable
        3D point to transform.

    Returns
    -------
    vecs : numpy.ndarray
        Copy of 'point' with transformed coordinates.
    """
    return (np.asanyarray(mat) @ np.append(point, 1))[:3]


def transf_dist(mat, dist):
    """
    Apply a transformation matrix to a distance vector.

    Parameters
    ----------
    mat : Iterable
        4x4 transformation matrix to apply.
    point : Iterable
        3D vector of distance to transform.

    Returns
    -------
    vecs : numpy.ndarray
        Copy of 'dist' with transformed coordinates.
    """
    return np.asanyarray(mat)[:3, :3] @ dist


def complement(a, b):
    """
    Remove all common vectors found in a and b from a.
    a - b in set theory.

    Parameters
    ----------
    a : Iterable
        Iterable to remove vectors from.
    b : Iterable
        Vectors to remove from 'a'. Vectors not found in 'a' will have
        no effect.

    Returns
    -------
    numpy.ndarray
        Copy of 'a' with all vectors also found in 'b' removed.
    """
    a = np.asanyarray(a)
    if len(b) == 0:
        return a
    b = np.asanyarray(b)
    dims = np.maximum(b.max(0), a.max(0)) + 1
    return a[~np.in1d(
        np.ravel_multi_index(a.T, dims),
        np.ravel_multi_index(b.T, dims),
    )]


def lerp(start, end, alpha):
    return start * (1 - alpha) + end * alpha


def invlerp(start, end, alpha):
    return (alpha - start) / (end - start)


def lerpclip(start, end, alpha):
    out = lerp(start, end, alpha)
    np.clip(out, start, end, out=out)
    return out


def invlerpclip(start, end, alpha):
    out = invlerp(start, end, alpha)
    np.clip(out, 0, 1, out=out)
    return out
