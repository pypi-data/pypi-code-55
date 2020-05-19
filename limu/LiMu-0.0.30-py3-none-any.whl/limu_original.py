#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# std imports
import sys, os, glob, random

# numpy
import numpy
import numpy.random

#scipy
import scipy.linalg

#pandas
import pandas

# skimage
import skimage.measure
import skimage.segmentation
import skimage.feature
import skimage.filters
import skimage.filters.rank
import skimage.io

# hdbscan
import hdbscan

# sklearn
import sklearn.cluster

# matplotlib
import matplotlib.pyplot

# read raw images
import rawkit.raw

def rgb2pol(arr):
  #print arr.max(0).max(0)
  r = ((arr**2).sum(2))**0.5
  theta = numpy.arccos(arr[:,:,2]/r) / numpy.pi
  phi = numpy.arctan2(arr[:,:,1],arr[:,:,0]) / numpy.pi
  #print theta.min(), phi.min(), r.max()
  return numpy.dstack((2*phi,2*theta , r/(3**.5)))
  
def guess_image( arr, mask, use_border=True ):
  # make an educated guess about the image
  # use data where mask is true
  # useful for white balancing... 
  array = arr.copy()
  bwidth = 5
  array[~mask,:] = 0
  disk = skimage.morphology.disk(bwidth)
  bleaf = scipy.ndimage.binary_dilation(~mask,disk)
  border = numpy.logical_xor(bleaf, ~mask)
  q=numpy.array(numpy.where(border)).T  
  q = q[numpy.random.choice(q.shape[0], 1000),:].reshape(1000,1,2)
  t=numpy.array(numpy.where(~mask)).T 
  t = t[numpy.random.choice(t.shape[0], 1100),:].reshape(1,1100,2)
  dst= 1./((q-t)**2).sum(2)**2
  dst /= dst.sum(0).reshape(1,-1)
  vals = array[q[:,0,0],q[:,0,1]]
  nw = (numpy.atleast_3d(dst)*vals.reshape(-1,1,3)).sum(0)
  array[t[0,:,0],t[0,:,1],:] = nw
  nmask = ~bleaf
  nmask[q[:,0,0],q[:,0,1]] = True
  nmask[t[0,:,0],t[0,:,1]] = True
  idx_r, idx_c = numpy.where(nmask)
  xi_idx_r, xi_idx_c = numpy.where(~nmask)
  #linear interpolated
  intp= scipy.interpolate.griddata((idx_r,idx_c), 
            array[idx_r,idx_c],
            (xi_idx_r, xi_idx_c),
            method='linear')
  # nearest interpolation to fill where linear fails
  up = scipy.interpolate.griddata((idx_r,idx_c),
           array[idx_r,idx_c],
           (xi_idx_r, xi_idx_c),
           method='nearest')        
  nonfinite = ~numpy.isfinite(intp)
  intp[nonfinite] = up[nonfinite]
  array[xi_idx_r, xi_idx_c] = intp  

  return array
    
def demosaic_mean( array, bits ):
  arr = array.astype(float) / float(2**bits)
  out = numpy.zeros((arr.shape[0]-2, arr.shape[1]-2,3), dtype=float)
  
  p1 = arr[:-2,:-2]
  p2 = arr[:-2,2:]
  p3 = arr[2:,2:]
  p4 = arr[2:,:-2]
  p5 = arr[1:-1,1:-1]

  # red 
  c = 0
  out[::2,::2,c ] =  ( p1[::2,::2] + p2[::2,::2] + p3[::2,::2] + p4[::2,::2] ) /4.
  out[::2,1:-1:2,c ] = ( p2[::2,:-2:2] + p3[::2,:-2:2] ) /2.
  out[1:-1:2,::2,c ] = ( p4[:-2:2,::2] + p3[:-2:2,::2] ) /2.
  out[1:-1:2,1:-1:2,c ] = p3[:-2:2,:-2:2]
 
  # green
  c = 1
  q =  ( p1[::2,1::2]+ p1[1::2,::2]+p2[1::2,::2]+ p4[::2,1::2] ) / 4.
  out[::2,::2,c ] = q 
  out[::2,1:-1:2,c ] = p2[1::2,:-2:2]    
  out[1:-1:2,::2,c ] =  p4[:-2:2, 1::2]  
  q =  ( p3[::2,1::2]+ p3[1::2,::2]+p2[1::2,::2]+ p4[::2,1::2] ) / 4.  
  out[1:-1:2,1:-1:2,c ] = q[:-1,:-1]  

  # blue 
  c = 2
  out[::2,::2,c ] =  p1[1::2,1::2]  
  out[::2,1:-1:2,c ] =  ( p1[1::2,1:-1:2] + p2[1::2,1:-1:2]  ) /2.
  out[1:-1:2,::2,c ] =  ( p1[1:-1:2,1::2] + p4[1:-1:2,1::2]  ) /2.  
  out[1:-1:2,1:-1:2,c ] = ( p1[1:-1:2,1:-1:2]+p2[1:-1:2,1:-1:2]+p3[1:-1:2,1:-1:2]+p4[1:-1:2,1:-1:2] ) /4.

  white = out[1:-1,1:-1,:].max(0).max(0)*1.2
  return out[1:-1,1:-1,:]/ white.reshape(1,1,3)

def demosaic( array, method='mean' ):
  bits = 14
  if (numpy.array( array.shape ) % 2).any():
    print 'WRONG size of bayer array'
    return None

  if method=='mean':
    return demosaic_mean( array, bits ) 
  

def get_barcodes( path ):
  barcodes={}  
  with open( path) as bf:
    for l in bf.read().split('\n'):
        try:
          key, val=l.split('\t')
          barcodes[key] = val
        except:
          print l
    return barcodes


def findfile( path, suffix='CR2'):
  # finds files recursively with supplied file suffix
  l = []
  if os.path.isdir(path):
    for fname in  glob.glob(path+'/*'):
      print 'found file {}'.format(fname)
      l.extend( findfile( fname ,suffix) )
  else:
    if os.path.basename( path ).split( '.' )[-1] == suffix:
      l.append(path)
    else:
      print 'wrong suffix', os.path.basename( path ).split( '.' )[-1], suffix
  return( l )    

class LimuImage:
  def __init__(self):
    self._data = {}
    self.npz_obj = {}
    self._produce = { # prod lookup
      #'label':self._p_label,
      'barcode':self.prod_barcode,
      'imageraw':self.prod_imageraw,
      'labels':self.prod_labels,
      'leafprops':self.prod_leafprops,
      'leafraw':self.prod_leafraw,
      'leafrgb':self.prod_leafrgb,
      'lesions':self.prod_lesions,
      'mask':self.prod_mask,
      'norm':self.prod_norm,
      'norminv':self.prod_norminvert,
      'sampleprops':self.prod_sampleprops,
      #'separation':self.prod_separation,
      'segmentation':self.prod_segmentation,
      'stain':self.prod_stain,
      'white':self.prod_white,
      'white_small':self.prod_whitesmall,
      }
    self._keeps = [ 
      'leafraw',
      'mask',
      'white_small',
      'labels',
      'leafprops',
      'lesions',
      'sampleprops',  
       ]
    self.name = 'name not set'
    self.kwargs = {}

  def clean(self):
    del self._data
    del self.npz_obj

  @staticmethod
  def get_biggest_label(labels):
    # return the label with biggest area
    # zero label is excluded
    # labels must be non-negative int
    counts = numpy.bincount(labels.ravel())
    score = list(numpy.argsort(counts))
    candidate = score.pop()
    if candidate > 0:
      return candidate
    return score.pop()
    

  @staticmethod
  def get_disk(r):
    d= skimage.morphology.disk(r)
    pw = (2*numpy.pi* r**2)**.5 - r
    d=skimage.util.pad( d,int(numpy.round(pw,0)),mode='constant')*1.0
    d /= d.sum()
    d =  d-d.mean()
    return d

  def has_data(self, key):
    if key in self._data.keys():
      return True
    if key in self.npz_obj.keys():
      return True
    return False

  def get_data(self, key, remake=False):
    if remake:
      self._produce[key](key)
    if key in self._data.keys():
      return self._data[key]
    if key in self.npz_obj.keys():
      self._data[key] = self.npz_obj[key]
      return self._data[key]
    print key,
    self._produce[key](key)
    return self._data[key] 

  @staticmethod
  def get_mask_adv(array):
    # returns a more advanced mask from boolean mask    
    # regular mask
    adv = array.astype(numpy.uint8) | 128 # bit 1, 128 just for convinient printing
    # with holes filled
    adv = adv | scipy.ndimage.morphology.binary_fill_holes(
        array).astype(numpy.uint8) << 1 # bit 2
    # outer background
    adv =  adv | ( 0b10 & ~adv) << 5  # bit 7 
    # holes 
    adv += ( ( adv >> 1) & ( ~adv & 0b1 ) ) <<  5 # bit 6
    # outer edge
    adv += skimage.segmentation.find_boundaries(0b10 & adv, mode='inner').astype(numpy.uint8) << 3 # bit 4
    # "center line" # very innacurate but anyway...
    idxs =  scipy.ndimage.morphology.distance_transform_edt(0b10 & adv).argmax(1)
    rs = numpy.arange(idxs.shape[0])
    adv[rs , idxs] += (adv[rs , idxs] & 1) << 4 # bit 5
    return( adv )

  def process(self,remake=[]):
    change = False
    for layer in remake:
      void = self.get_data(layer,remake=True)
      change = True 
    for layer in self._keeps:
      if self.has_data(layer):
        continue
      void = self.get_data(layer)
      change = True 
    if change:
      self.savez()  
    return change

  def prod_barcode(self, key):
    try:
      out = self.kwargs['barcodes'][self.name]
    except:
      out = "2018 SLU EM EX 00"
    self._data[key] = out

  def prod_imageraw(self, key):
    raw = self._load_raw() 
    self._data[key] = raw

  def prod_labels(self, key):
    seg=self.get_data('segmentation')
    out = skimage.measure.label(seg)
    self._data[key] = out

  def prod_leafraw(self, key):
    dscale = float(16)
    imgraw = self.get_data('imageraw')
    ds = skimage.transform.rescale(imgraw , 1/dscale)
    ds -= ds.min()
    ds /= ds.max()
    dk = numpy.hstack((numpy.argwhere(ds>-1)*0.001, 2**ds.reshape(-1,1)))
    clusterer = hdbscan.HDBSCAN(min_cluster_size=100)  
    pred = clusterer.fit_predict(dk).reshape(ds.shape)
    label_sum = 0
    for label in numpy.unique(pred):
      lsum = ds[pred==label].sum()
      if lsum > label_sum:
         bg_label = label
         label_sum = lsum 

    # relabel and find biggest
    bg = skimage.measure.label(pred==bg_label)
    bg_label = self.get_biggest_label(bg)

    # get objets inside background
    bg = bg == bg_label
    holes = numpy.logical_xor(scipy.ndimage.binary_fill_holes(bg),bg)
    objects = skimage.measure.label(holes)
    
    props = skimage.measure.regionprops(objects)
    
    # the best guess is bigger than 1000
    # if smaller than 6000
      # pick upper object
    candidate = [None, None]
    
    for prop in props:
      #print prop.label, prop.area
      if prop.area < 1000:
        #print 'area < 1000'
        continue

      if candidate[0] is None:
        #print 'no prop.. setting'
        candidate = [prop.label, prop]
        continue
      
      if prop.area > 5000:
          candidate = [prop.label, prop]
          continue

      if candidate[1].bbox[0] > prop.bbox[2]:        
        candidate = [prop.label, prop]
        continue
    bbox = (numpy.array(candidate[1].bbox)*dscale).astype(int)
    pad = 128
    self._data[key] = imgraw[bbox[0]-pad:bbox[2]+pad,bbox[1]-pad:bbox[3]+pad]

  def prod_leafrgb(self, key):
    rawleaf = self.get_data('leafraw')
    leafrgb = demosaic(rawleaf)
    self._data[key] = leafrgb 

  def prod_leafprops(self, key):
    props = {} 
    mask = self.get_data('mask')
    labels = self.get_data('labels')
    stain = self.get_data('stain')
    skprops = skimage.measure.regionprops(
          mask.astype(int), intensity_image=stain)[0]
    useprops = ['area','bbox','centroid','eccentricity','euler_number','extent','equivalent_diameter','perimeter','orientation']
    for prpkey in useprops:    
      props['rp_'+prpkey] = skprops[prpkey]
    props['b_height'], props['b_width'] = numpy.diff(
          numpy.array(props['rp_bbox']).reshape(2,2).T)[:,0]
    props['b_lesions_no'] = numpy.unique(labels).shape[0]-1
    props['b_lesions_area'] = (labels>0).sum()
    props['c_stain_max'] = stain.max()
    props['c_stain_min'] = stain.min()
    props['c_stain_mean'] = stain.mean()
    self._data[key] = numpy.array(props)

  def prod_lesions(self, key):
    lesions = {}
    labels = self.get_data('labels')    
    stain = self.get_data('stain')
    # 

    polar = rgb2pol(self.get_data('norminv'))
    # polar[~mask] = [0,0,0]
    blue = polar[:,:,1]
    dark = polar[:,:,2]
    mask = self.get_data('mask')
    advmask = self.get_mask_adv(mask)
    leafprops = self.get_data('leafprops')[()]
    leafbox = leafprops['rp_bbox']
    leafbase = leafbox[2]

    # distance from outer edge
    dst_oedge = scipy.ndimage.morphology.distance_transform_edt(advmask & 0b10)    
    
    # distance from any edge
    dst_edge = scipy.ndimage.morphology.distance_transform_edt(advmask & 0b1)

    # distance from center line
    dst_cline = scipy.ndimage.morphology.distance_transform_edt(~advmask & 0b10000)
    
    dst = numpy.dstack((dst_oedge,dst_edge,dst_cline ))
    regprops = skimage.measure.regionprops(
          labels, intensity_image=blue)
    for prop in regprops:
      pd = {}
      if prop.label < 1:
        continue
      pmask = labels == prop.label
      
      useprops = ['label','area','bbox','centroid','eccentricity','euler_number','extent','equivalent_diameter','perimeter','orientation']
      for prpkey in useprops:    
        pd['rp_'+prpkey] = prop[prpkey]
      f = dst[pmask].astype(int)
      fs= blue[pmask]
      fs2= dark[pmask]
      pd['dst_oedge_max'], pd['dst_edge_max'], pd['dst_cline_max'] = f.max(0)
      pd['dst_oedge_min'], pd['dst_edge_min'], pd['dst_cline_min'] = f.min(0)
      pd['dst_oedge_mean'], pd['dst_edge_mean'], pd['dst_cline_mean'] = f.mean(0).astype(int)
      pd['c_blue_max'],pd['c_blue_min'], pd['c_blue_mean'] = fs.max(), fs.min(), fs.mean()
      pd['c_dark_max'],pd['c_dark_min'], pd['c_dark_mean'] = fs2.max(), fs2.min(), fs2.mean()
      pd['d_class_log10'] =  int(numpy.log10(pd['rp_area']))
      pd['b_ypos'] =  leafbase- pd['rp_centroid'][0]
      pd['b_height'], pd['b_width'] = numpy.diff(
          numpy.array(pd['rp_bbox']).reshape(2,2).T)[:,0]   
      for k, v in pd.items():
        if not k in lesions.keys():
          lesions[k] = []
        lesions[k].append(v)
    self._data[key] = numpy.array(lesions)  

  def prod_mask(self, key):
    norminv = self.get_data('norminv')
    pol = rgb2pol(norminv)
    d= skimage.morphology.disk(5)
    blue = pol[:,:,1]
    bmax = skimage.filters.rank.maximum(blue,d )
    lum = pol[:,:,2]
    thresh = skimage.filters.threshold_otsu(lum)
    objects = skimage.measure.label(lum>thresh)
    leaf = self.get_biggest_label(objects)==objects
    holes = numpy.logical_xor(leaf, scipy.ndimage.binary_fill_holes(leaf))
    labels = skimage.measure.label(holes)
    nokeep = numpy.unique(labels[bmax < 180])
    for label in nokeep:
      if label:
        leaf[labels==label]= True
    self._data[key] = leaf

  def prod_norminvert(self,key):
    norm = self.get_data('norm')  
    ds = -numpy.log10(norm)
    ds -= ds.min() 
    ds += .0001
    ds /= ds.max()
    self._data[key] = ds

  def prod_white(self, key):
    white_small = self.get_data('white_small')
    self._data[key] = skimage.transform.rescale(white_small , 4)

  def prod_whitesmall(self, key):
    rgb = self.get_data('leafrgb')
    rgb_ds = skimage.transform.rescale(rgb , 1/4.)
    ds = rgb_ds - rgb_ds.min()
    ds /= ds.max()
    dk = numpy.hstack((numpy.argwhere(ds[:,:,0]>-1)*0.01, 2**ds.reshape(-1,3)))
    clusterer = hdbscan.HDBSCAN(min_cluster_size=100)  
    pred = clusterer.fit_predict(dk).reshape(ds.shape[0],ds.shape[1])
    areas = []
    pred += 1 # donbt exclude label 0 (background... likely)
    for prop in skimage.measure.regionprops(pred):
      areas.append([prop.bbox_area, prop.label])
    bg = sorted(areas)[-1][1]
    objects = skimage.measure.label(~(pred==bg))
    leaf = self.get_biggest_label(objects)
    bg = ~scipy.ndimage.binary_dilation(objects==leaf,skimage.morphology.disk(3))
    guess_image( rgb_ds, bg)
    self._data[key] = guess_image( rgb_ds, bg)

  def prod_norm(self, key):
    rgb = self.get_data('leafrgb')
    white = self.get_data('white')
    norm = ( rgb * 0.999) / white
    norm[norm > 1] = 1
    self._data[key] = norm 

  def prod_sampleprops(self, key):
    sample_dic={}
    bc = self.get_data('barcode')
    #print bc
    bc=str(bc).split() 
    #print '-------',bc
    try:
      sample_dic['species']=bc[3]
      if sample_dic['species'] == 'NC':
        treat = 'NC'
        rep= 0
      elif sample_dic['species'] == 'PT':
        treat = 'PC'
        rep = 0
      else:  
        treat = bc[5]
        rep = bc[6]
      nr = bc[-1]
      sample_dic['name'] = self.name
      sample_dic['treatment'] = treat
      sample_dic['repetition'] = rep
      sample_dic['img_no'] = nr
    except:
      sample_dic['name'] = self.name
      sample_dic['species'] ='Unknown'
      sample_dic['treatment'] = 'special'
      sample_dic['repetition'] = 0
      sample_dic['img_no'] = 0
    sd = {}
    for k, val in sample_dic.items():
      sd['a_'+k] = val
    self._data[key] = numpy.array(sd)


  def prod_segmentation(self, key):
    stain = self.get_data('stain').copy()
    mask = self.get_data('mask')
    rads = [13,10,9,7,6,5,4,3,2,1]
    out = numpy.zeros(stain.shape, dtype=bool)
    stain[~mask] = stain[mask].min() # set outside to min
    for i in rads:
      print 'c',
      cc= numpy.zeros(out.shape, dtype=int)
      disk = self.get_disk(i)
      
      tmp = scipy.ndimage.filters.convolve(stain,disk) 
      mp = tmp > (tmp.max()*0.1)
      mp = scipy.ndimage.morphology.binary_dilation(mp)
      mp = scipy.ndimage.morphology.binary_fill_holes(mp)
      mp = numpy.logical_or(mp, out)
      labels = skimage.measure.label(mp)
      labelnumbers = numpy.unique(labels)
     
      for label in labelnumbers:
        selection = labels==label
        selection[~mask] = False
        q = stain[selection]
        z = numpy.linspace(q.min(),q.max(),11)
        if (z[6]-z[0])<(0.001*selection.sum()**.5):
          #print 'weak leasion'
          continue
        ar = stain[selection]>z[6]
        cc[selection] += ar
      out = numpy.logical_or(out,cc)
    self._data[key] = out

  def prod_stain(self, key):
    nip = rgb2pol(self.get_data('norminv'))
    mask = self.get_data('mask')
    nip[~mask] = 0
    q = nip[:,:,1:].prod(2)
    self._data[key] = q
   
  @classmethod
  def load_raw(self, fname, **kwargs):
    abspath = os.path.abspath(fname)
    assert os.path.isfile(abspath)
    basename = os.path.basename(abspath)
    name = basename.split('.')[0].split('_')[-1]
    datadir = kwargs['dpath']
    datadir = os.path.abspath(datadir)
    assert os.path.isdir(datadir)
    obj = self()    
    obj.name = name
    obj.kwargs = kwargs
    obj._data['px_per_cm2'] = kwargs['px_per_cm2']
    obj.file_raw = abspath
    obj.file_npz = "{}/{}.npz".format(datadir, name)    
    if os.path.isfile(obj.file_npz):
      print 'found npz!!!!!!'
      obj._load_npz()
    else:
      print '***. ', obj.file_npz
    return( obj )

  @classmethod  
  def load_npz(self, fname, **kwargs):
    abspath = os.path.abspath(fname)
    basename = os.path.basename(abspath)
    name = basename.split('.')[0]
    obj = self()    
    obj.name = name
    obj.kwargs = kwargs
    obj.file_raw = None
    obj.file_npz = abspath
    if os.path.isfile(obj.file_npz):
      obj._load_npz()
    return( obj )
 
  def _load_npz(self):
    self.npz_obj = numpy.load(self.file_npz)

  def _load_raw(self):
    with rawkit.raw.Raw(filename=self.file_raw) as rawy:
      return numpy.array(rawy.raw_image(include_margin=True)) 

  def _save_npz(self):
    dout = {}
     
    fname = self.file_npz #'data6/{}.npz'.format(self.name)
    for key, val in self._data.items():
      if key in self._keeps:
        dout[key]  = val
    numpy.savez_compressed(fname, **dout)   
 

  def savez(self):
    for layer in self._keeps:
      if self.has_data(layer):
        void = self.get_data(layer)
    self._save_npz()


if __name__ == '__main__':
  rawpics = os.path.abspath('/home/emina/2017Microlesions_experiment_Raw_Images')
  datadir = os.path.abspath('datafiles')
  figures = os.path.abspath('figures')
  outdir  = os.path.abspath('imagesteps')
  dataout= os.path.abspath('out')
  lesionfile = os.path.abspath('data_lesions.csv')
  lesionclasses = os.path.abspath('data_lesions_classes.csv')
    

  flist = findfile(rawpics)
  # resort based on filename not full path
  flist =[b for a,b in sorted([list(row) for row in  zip([fname[-8:-4] for fname in flist],flist)])]
  kwargs = {
      'px_per_cm2': 38628,
      'dpath' :datadir,
       'barcodes': get_barcodes('imagemeta.txt'),
        }

  # images not working for one reason or another
  blacklist = ['2948','2950','2973','1726','2248','2264','2868','2913','2201','2215','1685','2714','2346','2921','2758','2037','2085','2599','2065','2104','2726','2930']

  for process_step in ['finalise']: #['get_lesions', 'cluster_lesions','plotclusters','insert_class','make_images','finalise']:
    if process_step == 'get_lesions':
      print 'Getting lesions'
      try:  
        lesiondata = pandas.read_csv(lesionfile)
        continue
      except:
        pass
      lesiondata = None
      for fname in flist:
        print fname,
        img = LimuImage.load_raw(fname, **kwargs)
        if img.name in blacklist:
          print img.name,'blacklisted, skip'
          continue
        changed = img.process() #   remake=['sampleprops','lesions'])
        if changed:
          print 'changed, ok'
        else:
          print 'unchanged, ok'
        lesions = pandas.DataFrame(img.get_data('lesions')[()])
        nrows = lesions.shape[0]

        for key, val in img.get_data('sampleprops')[()].items():
          lesions.loc[:,key] = pandas.Series([val]*nrows, index=lesions.index)
        for key, val in img.get_data('leafprops')[()].items():
          lesions.loc[:,key] = pandas.Series([val]*nrows, index=lesions.index)
        if lesiondata is None:
          lesiondata = lesions
        else:
          lesiondata= lesiondata.append(lesions, ignore_index=True)
  
      lesiondata= lesiondata.reindex(sorted(lesiondata.columns), axis=1)
      lesiondata.to_csv(lesionfile) 
      continue

    elif process_step == 'cluster_lesions':
      print 'clustering'
      try:  
        print 'loading'
        lesiondata = pandas.read_csv(lesionclasses)
        continue
      except:
        pass
      print 'clustering lesions'
      data = []
      data.append(lesiondata['c_blue_max'])
      data.append(lesiondata['c_blue_max']-lesiondata['c_blue_min'])
      data.append(lesiondata['c_dark_max'])
      data.append(lesiondata['c_dark_max']-lesiondata['c_dark_min'])
      data.append(numpy.log10((lesiondata['rp_area']**.5)+.1))
      data.append(lesiondata['rp_eccentricity'])
      data = numpy.column_stack(data)

      from sklearn.preprocessing import StandardScaler as Scaler
      scaler = Scaler()
      data = scaler.fit_transform(data)

      from sklearn.cluster import MiniBatchKMeans as Clusterer
      clusterer = Clusterer(n_clusters=30,verbose=True)

      classes = clusterer.fit_predict(data)
      lesiondata['z_clusterclass'] = pandas.Series(classes, index=lesiondata.index)
      lesiondata.to_csv(lesionclasses)
    
    elif process_step == 'plotclusters':
      print 'plotting clusters'
      # delete png to rerun
      if os.path.isfile('{}/cluster-00.png'.format(figures)):
        continue
      layout = numpy.array((15, 15)) # cols, rows
      res = 100
      images = {}
      count = layout.prod()
      selection = None
      for classnumber in numpy.unique(lesiondata['z_clusterclass']):
        images[classnumber] = []
        subselection =    lesiondata.loc[lesiondata['z_clusterclass']==classnumber]
        if len(subselection) > count:
          rindex = numpy.random.choice(subselection.index.values, count)
          subselection = subselection.ix[rindex]
        if selection is None:
          selection = subselection
        else:
          selection= selection.append(subselection, ignore_index=True)
      selection = selection.sort_values(['a_name','z_clusterclass','rp_label'])
      for name in numpy.unique(selection['a_name']):
        print name
        subselection = selection.loc[selection['a_name']==name]
        fname = '{}/{:04}.npz'.format(datadir,name)
        img = LimuImage.load_npz(fname, **kwargs)
        for index, row in subselection.iterrows():
          label = row['rp_label']
          labels = img.get_data('labels')
          norm = img.get_data('norm')          
          sel = (labels == label)
          props = skimage.measure.regionprops(sel.astype(int))[0]
          box = numpy.array(props.bbox, dtype=int).reshape(2,2)
          pad = 10
          box += numpy.array([[-pad,-pad],[pad,pad]])
          size = numpy.diff(box,axis=0)
          ddi = size[0,0] - size[0,1]
          corr = numpy.zeros((2,2), dtype=int)
          cf = abs(ddi/2.)
          if ddi > 0:
            corr[:,1] = [-numpy.floor(cf),numpy.ceil(cf)]
          elif ddi < 0:
            corr[:,0] = [-numpy.floor(cf),numpy.ceil(cf)]
          box += corr
          size = numpy.diff(box,axis=0).sum(0)
          im = norm[box[0,0]:box[1,0],box[0,1]:box[1,1],:]
          sbox = sel[box[0,0]:box[1,0],box[0,1]:box[1,1]]
          imb = skimage.segmentation.mark_boundaries(im, sbox,color=(0,1,0))
          im = (imb+im)/2.
          im = skimage.transform.resize(im,output_shape=(res,res))
          images[row['z_clusterclass']].append(im)
           
      for classnumber in images.keys():
        image = None
        row = None
        for idx, im in enumerate(images[classnumber]):
          print idx
          if row is None:
            row = im
          else:
            row = numpy.hstack((row, im))
          if not ((idx+1) % layout[0]):
            if image is None:
              image = row
            else:
              image = numpy.vstack((image, row))
            row = None
        fname = '{}/cluster-{:02}.png'.format(figures, classnumber)  
        skimage.io.imsave(fname, image)  

    elif process_step == 'insert_class':
      for fname in flist:
        print fname,
        img = LimuImage.load_raw(fname, **kwargs)
        if img.name in blacklist:
          print img.name,'blacklisted, skip'
          continue
        
        selection = lesiondata.loc[lesiondata['a_name']==int(img.name)]  
        lesions = img.get_data('lesions')[()]  
        lesions['z_clusterclass']=selection['z_clusterclass'].tolist()      
        img._data['lesions'] = numpy.array(lesions)
        img.savez()


    elif process_step == 'make_images': # and put classification into npz
      manual_assessment = pandas.read_csv('classification.csv')
      real_lesions = manual_assessment.loc[manual_assessment['classification']==1]['cluster'].tolist()      
      colors =  manual_assessment['color'].tolist()
      colors = [color[1:-1].split(',') for color in colors] 
      colors = [(float(color[0]), float(color[1]),float(color[2])) for color in colors]

      for fname in flist:
        print fname,
        img = LimuImage.load_raw(fname, **kwargs)
        if img.name in blacklist:
          print img.name,'blacklisted, skip'
          continue
        oname = '{}/{}/{}-{}.png'.format(outdir,'steps-all',img.name,'full')
        if os.path.isfile(oname):
          continue

        leafrgb = img.get_data('leafrgb')
        oname = '{}/{}/{}-{}.png'.format(outdir,'step1-leafrgb', img.name,'leafrgb')
        skimage.io.imsave(oname,leafrgb )

        norm = img.get_data('norm')
        oname = '{}/{}/{}-{}.png'.format(outdir,'step2-normalised',img.name,'normalised')
        skimage.io.imsave(oname,norm)
      
        mask = img.get_data('mask')
        mask = skimage.color.label2rgb(mask, bg_label=0, bg_color=(1,1,1))
        oname = '{}/{}/{}-{}.png'.format(outdir,'step3-mask',img.name,'mask')
        skimage.io.imsave(oname,mask)

        labels = img.get_data('labels')
        labelsrgb = skimage.color.label2rgb(labels, bg_label=0, bg_color=(1,1,1))
        oname = '{}/{}/{}-{}.png'.format(outdir,'step4-labels',img.name,'labels')
        skimage.io.imsave(oname,labelsrgb)

        lesions_lut = numpy.array([-1] + img.get_data('lesions')[()]['z_clusterclass'])
        labelsclass = lesions_lut[labels]
        
        ld = norm.copy()
        lf = norm.copy()
        for clusterclass in numpy.unique(lesions_lut):
          print clusterclass
          if clusterclass == -1:
            continue #background
          s = labelsclass ==  clusterclass   
          print colors[clusterclass]
          ld = skimage.segmentation.mark_boundaries(ld, s, color=colors[clusterclass], background_label=0)
          if clusterclass in real_lesions:
            lf = skimage.segmentation.mark_boundaries(lf, s, color=colors[clusterclass], background_label=0)
        
        
        oname = '{}/{}/{}-{}.png'.format(outdir,'step5-clusterclass',img.name,'clusterclass')       
        skimage.io.imsave(oname,ld)
        oname = '{}/{}/{}-{}.png'.format(outdir,'step6-real_lesions',img.name,'real_lesions')       
        skimage.io.imsave(oname,lf)

        oname = '{}/{}/{}-{}.png'.format(outdir,'steps-all',img.name,'full')
        fullim = numpy.hstack((leafrgb, norm, mask, labelsrgb,ld,lf ))#leafrgb, norm, mask, labelsrgb))
        skimage.io.imsave(oname,fullim)

    elif process_step == 'finalise':
    
      manual_assessment = pandas.read_csv('classification.csv')
      real_lesions = manual_assessment.loc[manual_assessment['classification']==1]['cluster'].tolist()  
      image_selection =  pandas.read_csv('selection.csv')['Image_number'].tolist()     
      print image_selection
      image_selection = ['{:04}'.format(iid) for iid in image_selection] 
      print image_selection
      leafdata_selection = None
      lesions_selection = None
      summary_lesions_selection = None
      
      leafdata = None
      lesions = None
      summary_lesions = None
      
      leafdata_selection_filtered = None
      lesions_selection_filtered = None
      summary_lesions_selection_filtered = None
      
      leafdata_filtered = None
      lesions_filtered = None
      summary_lesions_filtered = None
          
      #random.shuffle(flist)
      
      for fname in flist:
        print fname,
        img = LimuImage.load_raw(fname, **kwargs)
        if img.name in blacklist:
          print img.name,'blacklisted, skip'
          continue
        #changed = img.process() #   remake=['sampleprops','lesions'])
        try:
          img_lesions = pandas.DataFrame(img.get_data('lesions')[()])
        except:
          print 'weird bug'
          d = img.get_data('lesions')[()] 
          d['z_clusterclass'] = d['z_clusterclass'][:len(d['rp_label'])] # weird bug solution
          print len(d['rp_label']), len(d['z_clusterclass'])
          img_lesions = pandas.DataFrame(d)      
        img_sampledata = img.get_data('sampleprops')[()]     
        img_leafdata = img.get_data('leafprops')[()]
        nrows = img_lesions.shape[0]
        # extend lesions to include sample data
        
        for key, val in img_sampledata.items():
          img_lesions.loc[:,key] = pandas.Series([val]*nrows, index=img_lesions.index)
        img_leafdata.update(img_sampledata)
        img_tmp = {}
        for key, val in img_leafdata.items():
          img_tmp[key] = [val]               
        img_leafdata = pandas.DataFrame(img_tmp)
        img_summary = None
        img_summary_filtered = None
        img_lesions_filtered  = None
        
        for clusterclass in numpy.unique(img_lesions['z_clusterclass']):
          selection = img_lesions.loc[img_lesions['z_clusterclass']==clusterclass]
          count = selection.shape[0]
          area = selection['rp_area'].sum()
          row = img_leafdata.copy()
          row['b_lesions_no'] = pandas.Series([count])
          row['b_lesions_area'] = pandas.Series([area])
          row['z_clusterclass'] = pandas.Series([clusterclass])
          if img_summary is None:    
            img_summary = row
          else:
            img_summary = img_summary.append(row, ignore_index=True)
          if clusterclass in real_lesions:
            if img_summary_filtered is None:
              img_lesions_filtered = selection
              img_summary_filtered = row
            else:
              img_summary_filtered = img_summary_filtered.append(row, ignore_index=True)
              img_lesions_filtered = img_lesions_filtered.append(selection, ignore_index=True)
        img_leafdata_filtered = img_leafdata.copy()
        img_leafdata_filtered['b_lesions_no'] = img_summary_filtered['b_lesions_no'].sum()
        img_leafdata_filtered['b_lesions_area'] = img_summary_filtered['b_lesions_area'].sum()     
        
        if leafdata is None:
          leafdata = img_leafdata
          lesions = img_lesions
          summary_lesions = img_summary
          leafdata_filtered = img_leafdata_filtered
          lesions_filtered = img_lesions_filtered
          summary_lesions_filtered =img_summary_filtered 
        else:
          leafdata = leafdata.append(img_leafdata, ignore_index=True)
          lesions = lesions.append(img_lesions, ignore_index=True)
          summary_lesions = summary_lesions.append(img_summary, ignore_index=True)
          leafdata_filtered = leafdata_filtered.append(img_leafdata_filtered, ignore_index=True)
          lesions_filtered = lesions_filtered.append(img_lesions_filtered, ignore_index=True)
          summary_lesions_filtered = summary_lesions_filtered.append(img_summary_filtered, ignore_index=True)
         
        #)
        
        
      #print leafdata['a_name', image_selection]
      leafdata_selection = leafdata[leafdata['a_name'].isin(image_selection)]
      lesions_selection = lesions[lesions['a_name'].isin(image_selection)]      
      
      summary_lesions_selection = summary_lesions[summary_lesions['a_name'].isin(image_selection)]
      leafdata_selection_filtered = leafdata_filtered[leafdata_filtered['a_name'].isin(image_selection)]
      lesions_selection_filtered = lesions_filtered[lesions_filtered['a_name'].isin(image_selection)]
      summary_lesions_selection_filtered = summary_lesions_filtered[summary_lesions_filtered['a_name'].isin(image_selection)]
     
          
      savelist = [
      (leafdata_selection,'leafdata_selection.csv'),
      (lesions_selection,'lesions_selection.csv'),
      (summary_lesions_selection,'summary_lesions_selection.csv'),
      #(leafdata,'leafdata.csv'),
      #(lesions,'lesions.csv'),
      #(summary_lesions,'summary_lesions.csv'), 

      (leafdata_selection_filtered,'leafdata_selection_filtered.csv'),
      (lesions_selection_filtered,'lesions_selection_filtered.csv'),
      (summary_lesions_selection_filtered,'summary_lesions_selection_filtered.csv'),
      #(leafdata_filtered,'leafdata_filtered.csv'),
      #(lesions_filtered,'lesions_filtered.csv'),
      #(summary_lesions_filtered,'summary_lesions_filtered.csv'),
      ]
      for frame, fname in savelist:
        print fname
        sframe = frame.reindex(sorted(frame.columns), axis=1)   
        sframe.to_csv('{}/{}'.format(dataout,fname)) 



