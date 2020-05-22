import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageOps
import string
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from scipy.signal import savgol_filter as sgf
from sklearn.feature_selection import SelectKBest, chi2, f_classif

class KLDivergence():
    def __init__(self, k=10):
        self.k = k

    def fit(self, X, y=None):
        """Compute the mean and std to be used for later scaling.
        Parameters
        ----------
        X : {array-like, sparse matrix}, shape [n_samples, n_features]
            The data used to compute the mean and standard deviation
            used for later scaling along the features axis.
        y
            Ignored
        """

        # Reset internal state before fitting

        return self.kl_fit(X, y)

    def kl_fit(self, X, y):

        y_unique = list(np.unique(y))
        features_list = np.linspace(0, X.shape[1] - 1, X.shape[1]).astype("int")
        X_1 = X[y == y_unique[0]]
        X_2 = X[y == y_unique[1]]
        x_1_mean = np.mean(X_1, axis=0)
        x_2_mean = np.mean(X_2, axis=0)

        p = abs(x_1_mean)
        q = abs(x_2_mean)
        sid_p = list(p[i] * np.log2(p[i] / q[i]) for i in range(len(p)))
        sid_q = list(q[i] * np.log2(q[i] / p[i]) for i in range(len(p)))

        mean_KL = list(0.5 * (sid_p[_] + sid_q[_]) for _ in range(len(sid_p)))
        results = pd.DataFrame(features_list, columns=["features_index"])
        results["mean_KL_divregence"] = mean_KL
        self.results_sorted = results.sort_values(by="mean_KL_divregence", ascending=False)

        if self.k == "all":
            self.best_feat = self.results_sorted["features_index"]

        else:
            self.best_feat = self.results_sorted["features_index"].iloc[:self.k]

        return self

    def transform(self, X):
        """Perform standardization by centering and scaling
        Parameters
        ----------
        X : array-like, shape [n_samples, n_features]
            The data used to scale along the features axis.

        """

        X = X[:, self.best_feat.index]

        return X

    def set_params(self, **params):
        """
        Set the parameters of this estimator.
        The method works on simple estimators as well as on nested objects
        (such as pipelines). The latter have parameters of the form
        ``<component>__<parameter>`` so that it's possible to update each
        component of a nested object.
        Parameters
        ----------
        **params : dict
            Estimator parameters.
        Returns
        -------
        self : object
            Estimator instance.
        """

        return self

    def fit_transform(self, X, y=None, **fit_params):
        """
        Fit to data, then transform it.
        Fits transformer to X and y with optional parameters fit_params
        and returns a transformed version of X.
        Parameters
        ----------
        X : numpy array of shape [n_samples, n_features]
            Training set.
        y : numpy array of shape [n_samples]
            Target values.
        **fit_params : dict
            Additional fit parameters.
        Returns
        -------
        X_new : numpy array of shape [n_samples, n_features_new]
            Transformed array.
        """
        # non-optimized default implementation; override when a better
        # method is possible for a given clustering algorithm
        if y is None:
            # fit method of arity 1 (unsupervised transformation)
            return self.fit(X, **fit_params).transform(X)
        else:
            # fit method of arity 2 (supervised transformation)
            return self.fit(X, y, **fit_params).transform(X)



class SpectraPrapering:

    def __init__(self, X):
        self.X = X

    def spectra_normalization(self, plot=False):
        df = pd.DataFrame(self.X.T)
        df = df.apply(lambda v: v / ((v ** 2).sum()) ** 0.5)
        df = df.apply(lambda v: v / v.max())
        self.X_norm = df.T.values

        if plot:
            fig, (ax1, ax2) = plt.subplots(2)
            ax1.plot(self.X.T)
            ax1.set_title("Original")
            ax2.plot(self.X_norm.T)
            ax2.set_title("Normalized")
            plt.show()
        return self.X_norm



def derivative(X, deriv=2, window_length=13, polyorder=3):
                X_dev = sgf(X,
                 window_length=window_length,
                 polyorder=polyorder,
                 deriv=deriv,
                 delta=1.0,
                 axis=1,
                 mode='nearest')
                return X_dev


def sticking_imges(imgs_list, sorting="horizontal", show_out_ph=True, resize_tuple="none", save=False, out_name_end_type="out.tif", out_type="tiff",
                   dpi=600):
    """

    :param imgs_list: list contain the location of the images (list of strings)
    :param sorting: defoalt "horizontal" and can change to "vertical" (string)
    :param show_out_ph:  do you want to see the final image? True or False (boolean)
    :param resize_tuple: new size (tuple)
    :param save: do you want to save the final image? True or False (boolean)
    :param out_name_end_type: the name or location of the final image in order to save (string)
    :param out_type: type of tinal image, defoal is "tiff" (string)
    :param dpi: 300, 600, 1200 (integer)
    :return: sticking images
    """
    numpyes = []
    intinal_sizes = np.zeros((len(imgs_list), 2))
    for im in imgs_list:
        if resize_tuple == "none":
            img = Image.open(im)
        else:
            img = Image.open(im).resize(resize_tuple, Image.ANTIALIAS)

        numpyes.append(np.array(img))

    if sorting == "horizontal":
        im_out = Image.fromarray(np.hstack(tuple(numpyes)))



    elif sorting == "vertical":
        im_out = Image.fromarray(np.vstack(tuple(numpyes)))

    if show_out_ph:
        im_out.show()

    if save:
        if out_type == "tiff":
            im_out.save(out_name_end_type,
                        compression='tiff_lzw',
                        dpi=(dpi, dpi),
                        optimize=True,
                        )
        else:
            im_out.save(out_name_end_type,
                        dpi=(dpi, dpi))


def image_resizing_ratio(init_location, final_location, percent, dpi=300):
    """
    Resize image input image and percent | Keep aspect ratio
    :param init_location:
    :param final_location:
    :param percent:
    :return:
    """
    img = Image.open(init_location)
    w, h = img.size
    img_resized = img.resize((int(float(percent*w)/float(100)),int(float(percent*h)/float(100))))
    img_resized.show()
    img_resized.save(final_location, dpi=(dpi, dpi))


def references_comparing_for_papers_edit(text_file_location):
    """
    This function checking if there are duplicate references in papers.
    Copy the refernces from the paper "with the numbers" and paste it in Notepad text file
    then write in a new first row the word "title".
    :param text_file_location:  Notepad text file location
    :return: report (pandas df)
    """
    df = pd.read_fwf(text_file_location).drop("Unnamed: 1", axis=1)
    X = df["title"].values.astype(str)
    df_ = pd.DataFrame(X, columns=["ref"])
    string_list = list(df_["ref"].apply(lambda _: _[_.find("\t") + 1:]))
    vectroized = CountVectorizer().fit_transform(string_list)
    vectors = vectroized.toarray()
    csim = cosine_similarity(vectors)
    similarity = np.around(csim[(csim > .70) & (csim < .95)] * 100, 0).astype(int)
    similarity = similarity[: int(0.5 * len(similarity))]
    v = np.argwhere((csim > .70) & (csim < .95))
    v = v[: int(0.5 * len(v))]
    df_out = pd.DataFrame()
    df_out["references_1_num"] = (v[:, 0] + 1)
    df_out["references_2_num"] = (v[:, 1] + 1)
    df_out["reference_text_1"] = df_out["references_1_num"].apply(lambda _: string_list[_ - 1])
    df_out["reference_text_2"] = df_out["references_2_num"].apply(lambda _: string_list[_ - 1])
    df_out["similarity %"] = similarity

    return df_out


class SqlImportCsv:
    def __init__(self, df, file_location, table_name="table"):
        """
        This class convert CSV files into SQL tables
        :param df: data frame (pandas)
        :param file_location: file location spuse to be inside the major folder that you defined in SQL (string)
        :param table_name: name of the table that you want to create (string)
        """
        self.df = df
        self.file_location = file_location
        self.table_name = table_name

    def praper_sql_table(self):
        qu = "CREATE TABLE public." + self.table_name + "("
        headers = "("
        self.columns = self.df.columns.values.astype(str)
        for ty in (self.columns):
            if (self.df[ty].dtype == "float64") | (self.df[ty].dtype == "int64"):

                typ = "NUMERIC"
            elif self.df[ty].dtype == "object":
                typ = "TEXT"
            else:
                typ = "OBJECT"

            q = "%s %s, \n" % (ty, typ)
            headers = headers + ty + ","
            qu = qu + q

        qu = qu + ");"
        self.qu = qu[:-5] + qu[-4:]
        self.headers = headers[:-1] + ")"
        print(qu)

    def import_file(self):

        import_ = "COPY %s %s\nFROM '%s' DELIMITER ',' CSV HEADER;" % (self.table_name, self.headers, self.file_location)
        self.import_ = import_

        self.praper_import = "%s\n%s" % (self.qu, self.import_)

        print(self.praper_import)


def feature_selection(X, y, k=10, type_of_tech="f_classif", offset=True):
    """

    :param X:numpy array of shape [n_samples, n_features]
            Training set.
    :param y:numpy array of shape [n_samples]
            Target values.
    :param k: number of features after selection (integer)
    :param type_of_tech:
    :param offset: shifted the the data, where the minimum value will be zero (boolean)
    :return: X with the selected values
    """
    if offset:
        X = X + abs(np.min(X))

    if (type_of_tech == "chi2") | (type_of_tech == "f_classif"):
        X_select = SelectKBest(score_func=eval(type_of_tech), k=k).fit_transform(X, y)
    elif (type_of_tech == "KL"):
        X_select = KLDivergence(k=k).fit_transform(X, y)

    return X_select