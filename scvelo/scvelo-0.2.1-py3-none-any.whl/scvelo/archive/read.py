from .logg import print_logg
import os

import loompy

try: import scanpy as sc
except: import scanpy.api as sc
import numpy as np


def check_loom_attributes(loom_filepath, backup_url=None):
    if not os.path.exists(loom_filepath):
        try:
            from urllib.request import urlretrieve
            urlretrieve(backup_url, loom_filepath)
            print_logg('Downloaded loom file')
        except OSError:
            print("OS error: {0}".format(OSError))

    ds = loompy.connect(loom_filepath)

    print('Layer keys: ', *ds.layer.keys())
    print('Column attributes: ', *ds.col_attrs.keys())
    print('Row attributes: ', *ds.row_attrs.keys())

    keys = [ds.col_attrs[str_tsne] for str_tsne in ds.col_attrs if 'tsne' in str_tsne.lower()]
    keys.extend([str_clusters for str_clusters in ds.col_attrs if 'cluster' in str_clusters.lower()])
    print('Automatically read: CellID, Gene, ', *keys)

    ds.close()
    return None


def read_loom(loom_filepath, backup_url=None, keys=None, all_loom_layers=False):
    """Read loom file and return AnnData object

    Arguments
    ---------
    loom_filepath: str
        directory of loom file

    backup_url: str

    all_loom_layers: bool, default=False
        whether to load loom layers 'loom_obs' and 'loom_var' into AnnData object

    Returns
    -------
    Updates the attributes .X, .var, .obsm['Xs'], .obsm['Xs']
    """
    if not os.path.exists(loom_filepath):
        try:
            from urllib.request import urlretrieve
            urlretrieve(backup_url, loom_filepath)
            print_logg('Downloaded loom file')
        except OSError:
            print("OS error: {0}".format(OSError))

    ds = loompy.connect(loom_filepath)

    adata = sc.AnnData(ds.layer['spliced'][:, :].T)

    adata.obsm['Xs'] = ds.layer["spliced"][:, :].T
    adata.obsm['Xu'] = ds.layer["unspliced"][:, :].T
    X_ambiguous = ds.layer["ambiguous"][:, :].T

    adata.var_names = list(ds.row_attrs['Gene'])

    # import tsne if available in the loom file
    tsne_list = [ds.col_attrs[str_tsne] for str_tsne in ds.col_attrs if 'tsne' in str_tsne.lower()]
    if len(tsne_list) > 0:
        adata.obsm['X_tsne'] = np.vstack(tsne_list).T

    # import clusters if available in the loom file
    clusters = [str_clusters for str_clusters in ds.col_attrs if 'cluster' in str_clusters.lower()]
    if len(clusters) > 0:
        adata.obs['clusters'] = ds.col_attrs[clusters[0]]
        adata.obs['clusters'] = adata.obs['clusters'].astype('category')

    # import all layers if required
    if all_loom_layers:
        adata.uns['loom_obs'] = dict(ds.col_attrs.items())
        adata.uns['loom_var'] = dict(ds.row_attrs.items())

    # planaria dataset requires a special conversion
    if loom_filepath.endswith('4GU75.loom'):
        adata.obs_names = np.array([x[16:29] for x in ds.col_attrs['CellID']])
    else:
        adata.obs_names = list(ds.col_attrs['CellID'])

    if keys is not None:
        for key in keys:
            if key in ds.col_attrs:
                adata.obs[key] = ds.col_attrs[key]
            elif key in ds.row_attrs:
                adata.var[key] = ds.row_attrs[key]

    ds.close()

    tot_mol_cell_submatrixes = [X.sum(1) for X in [adata.obsm['Xs'], adata.obsm['Xu'], X_ambiguous]]
    mean_abundances = np.round([np.mean(j / np.sum(tot_mol_cell_submatrixes, 0)) for j in tot_mol_cell_submatrixes], 2)

    print_logg('Read loom file (' + str(adata.obsm['Xs'].shape[0]) + ' cells x ' + str(adata.obsm['Xs'].shape[1]) +
               ' genes): abundance of [spliced|unspliced|ambiguous]: ' + str(mean_abundances))

    return adata


def initial_setup(adata, loom_filepath, match_cells=False, match_genes=False, all_loom_layers=False, copy=False):
    """Read loom file and match with existing AnnData object

    Arguments
    ---------
    loom_filepath: string
        directory of loom file

    match_cells: bool, default=False
        whether to match cells of loom file with AnnData object

    match_cells: bool, default=False
        whether to match genes of loom file with AnnData object

    all_loom_layers: bool, default=False
        whether to load loom layers 'loom_obs' and 'loom_var' into AnnData object

    Returns
    -------
    Updates the attributes .X, .var, .obs
    Creates the attributes .obsm['Xs'], .obsm['Xs']
    """
    ds = loompy.connect(loom_filepath)

    print_logg('Read loom file')

    loom_cells_filter = np.ones(len(ds.col_attrs['CellID']), dtype=bool)
    loom_genes_filter = np.ones(len(ds.row_attrs['Gene']), dtype=bool)
    adata_cells_filter = np.ones(len(adata.obs_names), dtype=bool)
    adata_genes_filter = np.ones(len(adata.var_names), dtype=bool)

    if match_cells:
        if loom_filepath.endswith('4GU75.loom'):
            loom_cells = np.array([x[16:29] for x in ds.col_attrs['CellID']])
        else:
            loom_cells = list(ds.col_attrs['CellID'])
        loom_cells_filter = np.array([(x in adata.obs_names) for x in loom_cells])
        adata_cells_filter = np.array([(x in loom_cells) for x in adata.obs_names])

    if match_genes:
        loom_genes = ds.row_attrs['Gene']
        loom_genes_filter = np.array([(x in adata.var_names) for x in loom_genes])
        adata_genes_filter = np.array([(x in loom_genes) for x in adata.var_names])

    if adata_cells_filter.sum() == 0:
        raise ValueError(
            'Cell names in loom file do not match cell names in AnnData.')

    adata._inplace_subset_obs(adata_cells_filter)
    adata._inplace_subset_var(adata_genes_filter)

    adata.obsm['Xs'] = ds.layer["spliced"][:, :][loom_genes_filter, :][:, loom_cells_filter].T
    adata.obsm['Xu'] = ds.layer["unspliced"][:, :][loom_genes_filter, :][:, loom_cells_filter].T
    adata.obsm['Xa'] = ds.layer["ambiguous"][:, :][loom_genes_filter, :][:, loom_cells_filter].T

    if all_loom_layers:
        adata.uns['loom_obs'] = dict(ds.col_attrs.items())
        adata.uns['loom_var'] = dict(ds.row_attrs.items())

        adata.uns['loom_obs'] = {k: v[loom_cells_filter] for k, v in adata.uns['loom_obs'].items()}
        adata.uns['loom_var'] = {k: v[loom_genes_filter] for k, v in adata.uns['loom_var'].items()}

    ds.close()
    print_logg('Read loom items into anndata object')

    return adata if copy else None
