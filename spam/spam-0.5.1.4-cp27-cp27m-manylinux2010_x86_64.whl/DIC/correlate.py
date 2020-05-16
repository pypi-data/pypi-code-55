﻿"""
Library of SPAM image correlation functions.
Copyright (C) 2020 SPAM Contributors

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the Free
Software Foundation, either version 3 of the License, or (at your option)
any later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
more details.

You should have received a copy of the GNU General Public License along with
this program.  If not, see <http://www.gnu.org/licenses/>.
"""

# 2017-05-29 ER and EA
from __future__ import print_function

# This is spam's C++ DIC toolkit, but since we're in the tools/ directory we can import it directly
from . import DICToolkit

import numpy
import tifffile

import spam.DIC
import spam.deformation
import spam.label as ltk  # for im1mask
import progressbar

#numpy.set_printoptions(precision=3, suppress=True)

def register(im1, im2,
             im1mask=None,
             PhiInit=None, PhiInitBinRatio=1.0,
             margin=None,
             maxIterations=25, deltaPhiMin=0.001,
             interpolationOrder=1, interpolator='python',
             verbose=False,
             imShowProgress=None, imShowProgressNewFig=False):
    """
    Perform subpixel image correlation between im1 and im2.

    This function will deform im2 until it best matches im1.
    The matching includes sub-pixel displacements, rotation, and linear straining of the whole image.
    The correlation of im1, im2 will give a deformation function :math:`\Phi` which maps im1 into im2.

    :math:`im1(x) = im2(\Phi.x)`

    If im1 and im2 follow each other in time, then the resulting Phi is im1 -> im2 which makes sense in most cases.
    "Discrete correlation" can be performed by masking im1.

    im1 and im2 do not necessarily have to be the same size (`i.e.`, im2 can be bigger) -- this is good since there
    is a zone to accommodate movement. In the case of a bigger im2, im1 and im2 are centred with respect to each other.

    Parameters
    ----------
        im1 : 3D numpy array
            The greyscale image that will not move -- must not contain NaNs

        im2 : 3D numpy array
            The greyscale image that will be deformed -- must not contain NaNs

        im1mask : 3D boolean numpy array, optional
            A mask for the zone to correlate in im1 with `False` in the zone to not correlate.
            Default = None, `i.e.`, correlate all of im1 minus the margin.
            If this is defined, the Phi returned is in the centre of mass of the mask

        PhiInit : 4x4 numpy array, optional
            Initial deformation to apply to im1.
            Default = numpy.eye(4), `i.e.`, no transformation

        PhiInitBinRatio : float, optional
            Change translations in PhiInit, if it's been calculated on a differently-binned image. Default = 1

        margin : int, optional
            Margin, in pixels, to take in im1.
            Can also be a N-component list of ints, representing the margin in ND.
            If im2 has the same size as im1 this is strictly necessary to allow space for interpolation and movement
            Default = None (`i.e.`, enough margin for a worse-case 45degree rotation with no displacement)

        maxIterations : int, optional
            Maximum number of quasi-Newton iterations to perform before stopping. Default = 25

        deltaPhiMin : float, optional
            Smallest change in the norm of Phi (the transformation operator) before stopping. Default = 0.001

        interpolationOrder : int, optional
            Order of the greylevel interpolation for applying Phi to im1 when correlating. Recommended value is 3, but you can get away with 1 for faster calculations. Default = 3

        interpolator : string, optional
            Which interpolation function to use from `spam`.
            Default = 'python'. 'C' is also an option

        verbose : bool, optional
            Get to know what the function is really thinking, recommended for debugging only. Default = False

        imShowProgress : String, optional (default = None)
            Pop up a window showing a ``imShowProgress`` slice of the image differences (im1-im2) as im1 is progressively deformed.
            Accepted options are "Z", "Y" and "X" -- the slicing direction.

        imShowProgressNewFig : bool, optional (defaul = False)
                Make a new plt.figure for each iteration

    Returns
    -------
        Dictionary:

            'Phi': 4x4 float array
                Deformation function defined at the centre of the image

            'returnStatus': signed int
                Return status from the correlation:

                2 : Achieved desired precision in the norm of delta Phi

                1 : Hit maximum number of iterations while iterating

                -1 : Error is more than 80% of previous error, we're probably diverging

                -2 : Singular matrix M cannot be inverted

                -3 : Displacement > 5*margin

            'error': float
                Error float describing mismatch between images, it's the sum of the squared difference divided by the sum of im1

            'iterations': int
                Number of iterations

    Note
    ----
        This correlation was written in the style of S. Roux (especially "An extension of Digital Image Correlation for intermodality image registration")
        especially equations 12 and 13.

        Since we're using classical DIC (without multimodal registration) there is no need to update the gradient image,
        so this is calculated once at the beginning.

        PhiInit is taken into account, but a clean Phi which starts as the identity matrix is updated in
        the function, and numpy.dot(Phi,PhiInit) is applied and returned.
        This is important because the Taylor expansion is around the identity matrix.
    """
    # History:
    # 2018-03-20 EA: Trying to make margin a list of 3 values as z, y, x margins in order to try
    #   clean-ish 2D compatilibility

    # Explicitly set input images to floats
    im1 = im1.astype('<f4')
    im2 = im2.astype('<f4')

    # initialise exit clause for singular "M" matrices
    singular = False

    # Detect unpadded 2D image first:
    if len(im1.shape) == 2:
        # pad them
        im1 = im1[numpy.newaxis, ...]
        im2 = im2[numpy.newaxis, ...]
        if im1mask is not None:
            im1mask = im1mask[numpy.newaxis, ...]

    # Detect 2D images
    if im1.shape[0] == 1:
        twoD = True

        # Override interpolator for python in 2D
        interpolator = 'python'

        # Define masks for M and A in 2D since we'll ignore the Z components
        # Components of M and A which don't include Z
        twoDmaskA = numpy.zeros((12), dtype=bool)
        for i in [5, 6, 7, 9, 10, 11]:
            twoDmaskA[i] = True

        twoDmaskM = numpy.zeros((12, 12), dtype=bool)
        for y in range(12):
            for x in range(12):
                if twoDmaskA[y] and twoDmaskA[x]:
                    twoDmaskM[y, x] = True

    else:
        twoD = False

    # Automatically calculate margin if none is passed
    # Detect default case and calculate maring necessary for a 45deg rotation with no displacement
    if margin is None:
        # sqrt
        margin = [int((3**0.5 - 1.0) * max(im1.shape) * 0.5)] * 3
    elif type(margin) == list:
        pass
    else:
        # Make sure margin is an int
        margin = int(margin)
        margin = [margin] * 3

    # Make sure im2 is bigger than im1 and check difference in size
    # Get difference in image sizes. This should be positive, since we must always have enough data for im2 interpolation
    im1im2sizeDiff = numpy.array(im2.shape) - numpy.array(im1.shape)

    # Check im2 is bigger or same size
    if (im1im2sizeDiff < 0).any():
        print("\tcorrelate.register(): im2 is smaller than im1 in at least one dimension: im2.shape: {}, im1.shape: {}".format(im2.shape, im1.shape))
        raise ValueError("correlate.register():DimProblem")

    # Make sure margin is at least 1 for the gradient calculation
    if twoD:
        margin[0] = 0
    elif min(margin) < 1 and min(im1im2sizeDiff) == 0:
        margin = [1] * 3

    # Calculate crops -- margin for im2 and more for im1 if it is bigger
    # Margin + half the difference in size for im2 -- im1 will start in the middle.
    crop2 = (slice(int(im1im2sizeDiff[0] / 2 + margin[0]), int(im1im2sizeDiff[0] / 2 + im1.shape[0] - margin[0])),
             slice(int(im1im2sizeDiff[1] / 2 + margin[1]), int(im1im2sizeDiff[1] / 2 + im1.shape[1] - margin[1])),
             slice(int(im1im2sizeDiff[2] / 2 + margin[2]), int(im1im2sizeDiff[2] / 2 + im1.shape[2] - margin[2])))

    # Get subvolume crops from both images -- just the margin for im1
    crop1 = (slice(int(margin[0]), int(im1.shape[0] - margin[0])),
             slice(int(margin[1]), int(im1.shape[1] - margin[1])),
             slice(int(margin[2]), int(im1.shape[2] - margin[2])))

    # Create im1 crop to shift less data
    im1crop = im1[crop1].copy()

    # Calculate effective margin
    # to calculate displacement divergence
    # using max for the margin -- subjective choice
    realMargin = max(margin) + min(im1im2sizeDiff) / 2
    # print( "\tcorrelate.register(): realMargin is:", realMargin)

    # If live plot is asked for, initialise canvas
    if imShowProgress is not None:
        import matplotlib.pyplot as plt
        # Plot ranges for signed residual
        vmin = -im1crop.max() / 2
        vmax = im1crop.max() / 2
        if not imShowProgressNewFig:
            if imShowProgress == "Z" or imShowProgress == "z":
                plt.axis([im1crop.shape[2], 0, im1crop.shape[1], 0])
            if imShowProgress == "Y" or imShowProgress == "y":
                plt.axis([im1crop.shape[2], 0, im1crop.shape[0], 0])
            if imShowProgress == "X" or imShowProgress == "x":
                plt.axis([im1crop.shape[1], 0, im1crop.shape[0], 0])
            plt.ion()

    # Numerical value for normalising the error
    # errorNormalisationTmp = im1[crop1]
    # errorNormalisation = errorNormalisationTmp[numpy.isfinite(errorNormalisationTmp)].sum()
    # del errorNormalisationTmp
    # 2018-07-10 EA and OS: Removing im1 mask, so errorNormalisation is one-shot
    # 2019-01-18 EA putting it back in so error is more meaningful
    if im1mask is not None:
        errorNormalisation = im1crop[numpy.where(im1mask[crop1] == True)].sum()
    else:
        errorNormalisation = im1crop.sum()

    # 2019-09-11 EA: Avoid nans
    if errorNormalisation == 0:
        errorNormalisation = 1

    ###########################################################
    # Important -- since we're moving im2, initial Phis will be
    # pointing the wrong way, they need to be inversed
    ###########################################################
    # If there is no initial Phi, initalise it and im1defCrop to zero.
    Phi = numpy.eye(4)
    if PhiInit is None:
        PhiInitInternal = numpy.eye(4)
        PhiTotal = PhiInitInternal.copy()
        im2defCrop = im2.copy()[crop2]

    else:
        # 2020-03-17 in isolation from COVID-19 EA and OS: Apparently this changes the PhiInit outside this function, 
        #   Copying into different variable
        # Apply binning on displacement
        PhiInitInternal = PhiInit.copy()
        PhiInitInternal[0:3, -1] *= PhiInitBinRatio
        PhiTotal = PhiInitInternal.copy()

        # invert PhiInit to apply it to im2
        try:
            PhiInv = numpy.linalg.inv(PhiInitInternal.copy())
        except numpy.linalg.linalg.LinAlgError:
            PhiInv = numpy.eye(4)

        # Since we are now using Fcentred for iterations, do nothing
        # call decomposePhi to apply PhiInit (calculated on the centre of the image) to the origin (0,0,0)
        if interpolator == 'C':
            im2defCrop = spam.DIC.applyPhi(im2, Phi=PhiInv, interpolationOrder=interpolationOrder)[crop2]

        elif interpolator == 'python':
            im2defCrop = spam.DIC.applyPhiPython(im2, Phi=PhiInv, interpolationOrder=interpolationOrder)[crop2]

        else:
            return

    # Calculate gradient of the non-moving im1
    # 2017-11-06 EA: This is going in a try, since it's possible to have an error like this:
    #   "Shape of array too small to calculate a numerical gradient, "
    #   ValueError: Shape of array too small to calculate a numerical gradient, at least (edge_order + 1) elements are required.
    try:
        # Use gradient of image 2 which does NOT move
        if twoD:
            # If 2D image we have no gradients in the 1st direction
            if verbose:
                print("Calculating gradients...", end="")
            im1gradY, im1gradX = numpy.gradient(im1[0])
            im1gradX = im1gradX[numpy.newaxis, ...]
            im1gradY = im1gradY[numpy.newaxis, ...]
            im1gradZ = numpy.zeros_like(im1gradX)
            if verbose:
                print("done")
        else:
            if verbose:
                print("Calculating gradients...", end="")
            im1gradZ, im1gradY, im1gradX = numpy.gradient(im1)
            if verbose:
                print("done ")
    # If gradient calculation failed, set singular to true, means early exit
    except ValueError:
        # Override max iteration and also set singular
        maxIterations = 0
        singular = True

    # Apply stationary im1 mask
    if im1mask is not None:
        im1crop[im1mask[crop1] == False] = numpy.nan

    # Initialise iteration variables
    iterationNumber = 0
    returnStatus = 0
    # Big value to start with to ensure the first iteration
    deltaPhiNorm = 100.0
    errorTmp = numpy.square(numpy.subtract(im1crop, im2defCrop))
    error = errorTmp[numpy.isfinite(errorTmp)].sum() / errorNormalisation

    if verbose:
        print("Start correlation with Error = {:0.2f}".format(error))

        widgets = ['    Iteration Number:', progressbar.Counter(), ' ', progressbar.FormatLabel(''), ' (', progressbar.Timer(), ')']
        pbar = progressbar.ProgressBar(widgets=widgets, maxval=maxIterations)
        # widgets = [progressbar.FormatLabel(''), ' ', progressbar.Bar(), ' ', progressbar.AdaptiveETA()]
        # pbar = progressbar.ProgressBar(widgets=widgets, maxval=numberOfNodes)
        pbar.start()
        # --- Start Iterations ---
    while iterationNumber < maxIterations and deltaPhiNorm > deltaPhiMin:
        errorPrev = error

        # if verbose:
        # print("\tIteration Number {:02d}".format(iterationNumber)),

        # No recomputation of gradient -- initialise M and A
        M = numpy.zeros((12, 12), dtype='<f8')
        A = numpy.zeros((12), dtype='<f8')

        # Compute DIC operators A and M with C library
        # NOTE: If the image with gradients is not moving, M does not need to be recomputed
        DICToolkit.computeDICoperators(im1crop.astype("<f4"),
                                       im2defCrop.astype("<f4"),
                                       im1gradZ[crop1].astype("<f4"),
                                       im1gradY[crop1].astype("<f4"),
                                       im1gradX[crop1].astype("<f4"),
                                       M, A)

        if twoD:
            # If a twoD image, cut out the bits of the M and A matrices that interest us
            #   This is necessary since the rest is super singular
            A = A[twoDmaskA]
            M = M[twoDmaskM].reshape(6, 6)

        # Solve for delta Phi
        try:
            deltaPhi = numpy.dot(numpy.linalg.inv(M), A)
        except numpy.linalg.linalg.LinAlgError:
            singular = True
            break

        if twoD:
            # ...and now put deltaPhi components back in place for a 3D deltaPhi
            deltaPhinew = numpy.zeros((12), dtype=float)
            deltaPhinew[twoDmaskA] = deltaPhi
            del deltaPhi
            deltaPhi = deltaPhinew

        deltaPhiNorm = numpy.linalg.norm(deltaPhi)

        # Add padding zeros
        deltaPhi = numpy.hstack([deltaPhi, numpy.zeros(4)]).reshape((4, 4))

        # Apply Delta Phi correction to Phi In Roux X-N paper equation number 11
        #Phi = numpy.dot((numpy.eye(4) + deltaPhi), Phi)
        # ...in the end the Newton Raphson is setup as Phi + deltaPhi, which seems to work well here
        #   (saves an iteration or two in large rotations/displacements)
        Phi += deltaPhi

        # Compute Phi including the PhiInit
        # 2019-09-11 EA and OS: This was in the wrong order
        #PhiTotal = numpy.dot(Phi, PhiInitInternal)
        # 2020-04-20 EA and OS: The saga continues, in the case of very large initial guesses, it's better this way around,
        #   We have a first transformation (PhiInitInternal), which moves the coordinate system. Since we want to apply another
        #   local Phi on top of this transformation, this is the right way around in the end (i.e., Phi is not defined in
        #   the global coordinate but a local one).
        #   See: Huamin Wang's notes at: http://web.cse.ohio-state.edu/~wang.3602/courses/cse5542-2013-spring/6-Transformation_II.pdf
        #   (or copied in doc/theory/Wang Real-time Rendering Notes.pdf
        PhiTotal = numpy.dot(PhiInitInternal, Phi)

        # Solve for delta Phi
        try:
            PhiTotalInv = numpy.linalg.inv(PhiTotal.copy())
        except numpy.linalg.linalg.LinAlgError:
            singular = True
            break

        # reset im1def as emtpy matrix for deformed image
        if interpolator == 'C':
            im2defCrop = spam.DIC.applyPhi(im2, Phi=PhiTotalInv, interpolationOrder=interpolationOrder)[crop2]

        elif interpolator == 'python':
            im2defCrop = spam.DIC.applyPhiPython(im2, Phi=PhiTotalInv, interpolationOrder=interpolationOrder)[crop2]

        else:
            return

        # Error calculation
        errorTmp = numpy.square(numpy.subtract(im1crop, im2defCrop))
        error = errorTmp[numpy.isfinite(errorTmp)].sum() / errorNormalisation

        # Keep interested people up to date with what's happening
        # if verbose:
        #print("Error = {:0.2f}".format(error)),
        #print("deltaPhiNorm = {:0.4f}".format(deltaPhiNorm))

        # Catch divergence condition after half of the max iterations
        if errorPrev < error * 0.8 and iterationNumber > maxIterations / 2:
            # undo this bad Phi which has increased the error:
            #Phi = numpy.dot((numpy.eye(4) + deltaPhi), Phi)
            returnStatus = -1
            if verbose:
                print("\t -> diverging on error condition")
            break

        # Second divergence criterion on displacement (Issue #62)
        #   If any displcement is bigger than 5* the margin...
        if (numpy.abs(spam.deformation.decomposePhi(PhiTotal.copy())['t']) > 5 * realMargin).any():
            if verbose:
                print("\t -> diverging on displacement condition")
            returnStatus = -3
            break

        # 2018-10-02 - EA: Add divergence condition on U
        trans = spam.deformation.decomposePhi(PhiTotal.copy())
        try:
            volumeChange = numpy.linalg.det(trans['U'])
            if volumeChange > 3 or volumeChange < 0.2:
                if verbose:
                    print("\t -> diverging on volumetric change condition")
                returnStatus = -3
                break
        except:
            returnStatus = -3
            break

        if imShowProgress is not None:
            if imShowProgress == "Z" or imShowProgress == "z":
                if imShowProgressNewFig:
                    plt.figure()
                else:
                    plt.clf()
                plt.imshow(numpy.subtract(im1crop, im2defCrop)[im1crop.shape[0] // 2, :, :], cmap='coolwarm', vmin=vmin, vmax=vmax)
            if imShowProgress == "Y" or imShowProgress == "y":
                if imShowProgressNewFig:
                    plt.figure()
                else:
                    plt.clf()
                plt.imshow(numpy.subtract(im1crop, im2defCrop)[:, im1crop.shape[1] // 2, :], cmap='coolwarm', vmin=vmin, vmax=vmax)
            if imShowProgress == "X" or imShowProgress == "x":
                if imShowProgressNewFig:
                    plt.figure()
                else:
                    plt.clf()
                plt.imshow(numpy.subtract(im1crop, im2defCrop)[:, :, im1crop.shape[2] // 2], cmap='coolwarm', vmin=vmin, vmax=vmax)
            plt.title('\t\tIteration Number = {}'.format(iterationNumber))
            plt.pause(0.5)

        if verbose:
            r = spam.deformation.decomposePhi(PhiTotal.copy())["r"]
            U = spam.deformation.decomposePhi(PhiTotal.copy())["U"]
            widgets[3] = progressbar.FormatLabel("  dPhiNorm={:0>7.5f}   error={:0>4.2f}   t=[{:0>5.3f} {:0>5.3f} {:0>5.3f}]   r=[{:0>5.3f} {:0>5.3f} {:0>5.3f}]   Udiag=[{:0>5.3f} {:0>5.3f} {:0>5.3f}]".format(
                deltaPhiNorm,
                error,
                PhiTotal[0, -1],
                PhiTotal[1, -1],
                PhiTotal[2, -1],
                r[0],
                r[1],
                r[2],
                U[0, 0],
                U[1, 1],
                U[2, 2]))

        iterationNumber += 1
        if verbose:
            pbar.update(iterationNumber)

    # Positive return status is a healthy end of while loop:
    if iterationNumber >= maxIterations:
        returnStatus = 1
    if deltaPhiNorm <= deltaPhiMin:
        returnStatus = 2
    if singular:
        returnStatus = -2

    if verbose:
        print()
        # pbar.finish()
        if iterationNumber > maxIterations:
            print("\t -> No convergence before max iterations")
        if deltaPhiNorm <= deltaPhiMin:
            print("\t -> Converged")
        if singular:
            print("\t -> Singular")

    # create human readable transformation
    #trans = spam.deformation.decomposePhi(PhiTotal.copy())
    # display transform if verbose
    # if verbose:
    #print("\t --> displacements:  z={:.2f} vox".format(trans['t'][0]))
    #print("\t                     y={:.2f} vox".format(trans['t'][1]))
    #print("\t                     x={:.2f} vox".format(trans['t'][2]))
    #print("\t --> rotations comps:z={:.2f} deg".format(trans['r'][0]))
    #print("\t                     y={:.2f} deg".format(trans['r'][1]))
    #print("\t                     x={:.2f} deg".format(trans['r'][2]))

    # Create Phi appled at the centre of the image for returning
    #PhiZeroOrigin = PhiTotal.copy()
    #PhimaskCentre = PhiTotal.copy()
    #PhiZeroOrigin[0:3, -1] = spam.deformation.decomposePhi(Phi.copy(), PhiPoint=[0, 0, 0])["t"]

    if im1mask is not None:
        # If a mask on im1 is defined, return an Phi at the centre of the mass
        maskCOM = ltk.centresOfMass(im1mask[crop1])[-1]
        #print("Mask COM", maskCOM)
        #print( "\nNormal Phi:\n", Phi)
        PhiTotal[0:3, -1] = spam.deformation.decomposePhi(PhiTotal.copy(), PhiCentre=(numpy.array(im1crop.shape) - 1) / 2.0, PhiPoint=maskCOM)["t"]
        #print( "\nF in mask:\n", F)

    return {'error': error,
            #'transformation': trans,
            'Phi': PhiTotal,
            'returnStatus': returnStatus,
            'iterations': iterationNumber,
            'deltaPhiNorm': deltaPhiNorm}



def registerMultiscale(  im1, im2, binMax,
                            PhiInit=None, PhiInitBinRatio=1.0,
                            margin=None,
                            maxIterations=100, deltaPhiMin=0.0001,
                            interpolationOrder=1, interpolator='C',
                            verbose=False,
                            imShowProgress=None):
    """
    Perform multiscale subpixel image correlation between im1 and im2.

    This means applying a downscale (binning) to the images, performing a Lucas and Kanade at that level,
    and then improving it on a 2* less downscaled image, all the way back to the full scale image.

    If your input images have multiple scales of texture, this should save significant time.

    Please see the documentation for `register` for the rest of the documentation.

    Parameters
    ----------
        im1 : 3D numpy array
            The greyscale image that will not move -- must not contain NaNs

        im2 : 3D numpy array
            The greyscale image that will be deformed -- must not contain NaNs

        binMax : int
            Maximum amount of binning to apply, please input a number which is 2^int

        im1mask : 3D boolean numpy array, optional
            A mask for the zone to correlate in im1 with `False` in the zone to not correlate.
            Default = None, `i.e.`, correlate all of im1 minus the margin.
            If this is defined, the Phi returned is in the centre of mass of the mask

        PhiInit : 4x4 numpy array, optional
            Initial deformation to apply to im1, by default at bin1 scale
            Default = numpy.eye(4), `i.e.`, no transformation

        PhiInitBinRatio : float, optional
            Change translations in PhiInit, if it's been calculated on a differently-binned image. Default = 1

        margin : int, optional
            Margin, in pixels, to take in im1.
            Can also be a N-component list of ints, representing the margin in ND.
            If im2 has the same size as im1 this is strictly necessary to allow space for interpolation and movement
            Default = 0 (`i.e.`, enough margin for a worse-case 45degree rotation with no displacement)

        maxIterations : int, optional
            Maximum number of quasi-Newton iterations to perform before stopping. Default = 25

        deltaPhiMin : float, optional
            Smallest change in the norm of Phi (the transformation operator) before stopping. Default = 0.001

        interpolationOrder : int, optional
            Order of the greylevel interpolation for applying Phi to im1 when correlating. Recommended value is 3, but you can get away with 1 for faster calculations. Default = 3

        interpolator : string, optional
            Which interpolation function to use from `spam`.
            Default = 'python'. 'C' is also an option

        verbose : bool, optional
            Get to know what the function is really thinking, recommended for debugging only. Default = False

        imShowProgress : String, optional (default = None)
            Pop up a window showing a ``imShowProgress`` slice of the image differences (im1-im2) as im1 is progressively deformed.
            Accepted options are "Z", "Y" and "X" -- the slicing direction.

    Returns
    -------
        Dictionary:

            'Phi': 4x4 float array
                Deformation function defined at the centre of the image

            'returnStatus': signed int
                Return status from the correlation:

                2 : Achieved desired precision in the norm of delta Phi

                1 : Hit maximum number of iterations while iterating

                -1 : Error is more than 80% of previous error, we're probably diverging

                -2 : Singular matrix M cannot be inverted

                -3 : Displacement > 5*margin

            'error': float
                Error float describing mismatch between images, it's the sum of the squared difference divided by the sum of im1

            'iterations': int
                Number of iterations
    """
    import math
    l = math.log(binMax, 2)
    if not l.is_integer():
        print("spam.DIC.correlate.registerMultiscale(): You asked for a binning of",binMax,",rounding it to ", end='')
        binMax = 2**numpy.round(l)
        print(binMax)

    # If there is no initial Phi, initalise it and im1defCrop to zero.
    if PhiInit is None:
        PhiInit = numpy.eye(4)
    else:
        # Apply binning on displacement   -- the /2 is to be able to *2 it in the LK call
        PhiInit[0:3, -1] *= PhiInitBinRatio/2.0/float(binMax)
    reg = {'Phi': PhiInit}


    binLevel = int(binMax)
    while binLevel > 0.5:
        print("spam.DIC.correlate.registerMultiscale(): working on binning: ", binLevel)
        if binLevel > 1:
            im1b = spam.DIC.binning(im1, binLevel)
            im2b = spam.DIC.binning(im2, binLevel)
        else:
            im1b = im1
            im2b = im2

        if margin is None:
            marginB = None
        else:
            marginB = margin//binLevel
        reg = spam.DIC.register(im1b, im2b, PhiInit=reg['Phi'], PhiInitBinRatio=2.0,
                                   margin=marginB,
                                   maxIterations=maxIterations, deltaPhiMin=deltaPhiMin,
                                   interpolationOrder=interpolationOrder, interpolator=interpolator,
                                   verbose=verbose,
                                   imShowProgress=imShowProgress)

        binLevel = int(binLevel/2)
    return reg


def pixelSearch(imagette1, imagette2, searchCentre=None, searchRange={'zRange': [-2, 2], 'yRange': [-2, 2], 'xRange': [-2, 2]}):
    """
    Interface to Pixel Search C code.

    Parameters
    ----------
        imagette1 : 3D numpy array of floats
            Image 1 is the smaller reference image

        imagette2 : 3D numpy array of floats
            Image 2 is the bigger image

        searchCentre : 3-component list or numpy array, optional
            The point in im2 around which the search range is defined
            Default is middle of imagette2

        searchRange : dictionary, optional
            This dictionary contains 3 keys: 'zRange', 'yRange', and 'xRange',
            Each of which contains a list with two items.
            Default +-2 pixels in every direction

    Returns
    -------
        Dictionary:

            'transformation': dictionary
                Dictionary containing:

                    't' : 3-component vector

                        Z, Y, X displacements in pixels

            'cc':float
                Normalised correlation coefficient, ~0.5 is random, >0.99 is very good correlation.

    Note
    ----
        It important to remember that the C code runs MUCH faster in its current incarnation when it has
        a cut-out im2 to deal with (this is related to processor optimistaions).
        When the globalCoords flag is true we should search with all of im2 in memory, but (default) we will cut it out.
    """
    if searchCentre is None:
        searchCentre = (numpy.array(imagette2.shape, dtype='<f4') - 1) / 2.0
    else:
        searchCentre = numpy.array(searchCentre, dtype='<f4')

    # If dictionary overwrite with numpy array
    if type(searchRange) is dict:
        searchRange = numpy.array([searchRange['zRange'],
                                   searchRange['yRange'],
                                   searchRange['xRange']], dtype='<f4')
    else:
        print("correlate.pixelSearch(): searchRange should be a dict with 'zRange', 'yRange', and 'xRange' entries. Exiting")
        return

    assert(numpy.all(imagette2.shape >= imagette1.shape)), "spam.DIC.correlate.pixelSearch(): imagette2 should be bigger or equal to imagette1 in all dimensions"

    # Run the actual pixel search
    # print imagette1.shape, imagette2.shape, searchCentre, searchRange
    returns = numpy.zeros(4, dtype='<f4')
    DICToolkit.pixelSearch(imagette1.astype("<f4"),
                           imagette2.astype("<f4"),
                           searchCentre.astype("<f4"),
                           searchRange.astype("<f4"),
                           returns)

    # Collect and pack returns
    return {'transformation': {'t': returns[0:3]},
            'cc': returns[3]}


def globalCorrelation(im1, im2, mesh, convergenceCriterion=0.01, debugFiles=False, maxIterations=20, initialDisplacements=None, boundaryConditions=None, prefix="./"):
    import spam.helpers
    print("gdic: convergenceCriterion = {}".format(convergenceCriterion))
    print("gdic: maxIterations = {}".format(maxIterations))
    print("gdic: converting im1 to 32-bit float")
    im1 = im1.astype('<f4')

    print("\tgdic: Loading mesh...")
    points = numpy.array(mesh["points"]).astype('<f8')
    tetra = numpy.array(mesh["tetra"]).astype('<u2')
    imTetLabel = numpy.array(mesh["lab"]).astype('<u2')
    print("\tgdic: mesh box:")
    maxCoord = numpy.amax(points, axis=0).astype('<u2')
    minCoord = numpy.amin(points, axis=0).astype('<u2')
    print("\t\tmin coords: {}".format(minCoord))
    print("\t\tmax coords: {}".format(maxCoord))
    # meshPadding = numpy.array(mesh["padding"]).astype('<u1')
    # meshPaddingSlice = [slice(meshPadding[0], im1.shape[0]-meshPadding[0]),
    #                     slice(meshPadding[1], im1.shape[1]-meshPadding[1]),
    #                     slice(meshPadding[2], im1.shape[2]-meshPadding[2])]
    meshPaddingSlice = (slice(minCoord[0], maxCoord[0]),
                        slice(minCoord[1], maxCoord[1]),
                        slice(minCoord[2], maxCoord[2]))

    print("\tgdic: Points: ", points.shape)
    print("\tgdic: Cells:", tetra.shape)
    print("\tgdic: Mesh Padding:", meshPaddingSlice)

    ###############################################################
    # Step 2-1 Apply deformation and interpolate pixels
    ###############################################################
    displacements = numpy.zeros((3 * points.shape[0]), dtype='<f8')

    print("\tgdic: Allocating 3D data (deformed image)")
    if initialDisplacements is None:
        im1Def = im1.copy()
    else:
        print("\tgdic: Applying initial deformation to image")
        displacements = numpy.ravel(initialDisplacements)
        im1Def = numpy.zeros_like(im1, dtype="<f4")
        DICToolkit.applyMeshTransformation(im1.astype("<f4"),
                                           imTetLabel.astype("<u4"),
                                           im1Def,
                                           tetra.astype("<u4"),
                                           points.astype("<f8"),
                                           displacements.reshape(3, points.shape[0]).astype("<f8"))

    # if debugFiles:
    #     #tifffile.imsave("{}-def-{:03d}.tif".format(prefix, 0), im1Def[meshPaddingSlice])
    #     #tifffile.imsave("{}-residual-{:03d}.tif".format(prefix, 0), im2[meshPaddingSlice]-im1Def[meshPaddingSlice])
    #     spam.helpers.writeGlyphsVTK(points, pointData={"displacement": displacements.reshape(points.shape[0], 3)}, fileName="{}-displacementFE-{:03d}.vtk".format(prefix, 0))

    print("gdic: Correlating (MF)!")
    print("\tgdic: Calculating gradient...")
    im2Grad = numpy.array(numpy.gradient(im2), dtype='<f4')

    print("\tgdic: Computing global matrix")
    # This generates the globalMatrix (big M matrix) with imGrad as input
    # EnhancedMeshImageToolkitC.globalMatrix_func( imTetLabel, im1Grad, tetra, points, globalMatrix )
    globalMatrix = numpy.zeros((3 * points.shape[0], 3 * points.shape[0]), dtype='<f8')
    DICToolkit.computeDICglobalMatrix(imTetLabel.astype("<u4"),
                                      im2Grad.astype("<f4"),
                                      tetra.astype("<u4"),
                                      points.astype("<f8"),
                                      globalMatrix)

    applyBC = True if boundaryConditions is not None else False

    if applyBC:
        bc = numpy.ravel(boundaryConditions)
        nbc = numpy.logical_not(numpy.ravel(boundaryConditions))
        print("gdic: get boundary conditions")
        print("gdic: global matrix shape: {}".format(globalMatrix.shape))
        K11 = globalMatrix[nbc]
        K11 = K11[:, nbc]
        K22 = globalMatrix[bc]
        K22 = K22[:, bc]
        K12 = globalMatrix[nbc]
        K12 = K12[:, bc]
        K21 = globalMatrix[bc]
        K21 = K21[:, nbc]
        K22i = numpy.linalg.inv(K22)
        print("gdic: K11 shape: {}".format(K11.shape))
        print("gdic: K12 shape: {}".format(K12.shape))
        print("gdic: K22 shape: {}".format(K22.shape))
        print("gdic: K21 shape: {}".format(K21.shape))
    else:
        K11 = globalMatrix.copy()

    print("\tgdic: Inversing global matrix")
    # print globalMatrix, "\n\n\n\n\n"
    # + 0.0*numpy.eye( globalMatrix.shape[0] ) )
    # K11 = globalMatrix.copy()
    if applyBC:
        tmp = K11 - numpy.dot(K12, numpy.dot(K22i, K21))
        globalMatrixInv = numpy.linalg.inv(tmp)
    else:
        globalMatrixInv = numpy.linalg.inv(K11)
    # print globalMatrixInv

    #def errorCalc(im1, im2, im2ref, meshPaddingSlice):
        #errorInitial = numpy.sqrt(numpy.square(im2ref[meshPaddingSlice] - im1[meshPaddingSlice]).sum())
        #errorCurrent = numpy.sqrt(numpy.square(im2[meshPaddingSlice] - im1[meshPaddingSlice]).sum())
        #return errorCurrent / errorInitial

    #error = errorCalc(im2, im1Def, im1, meshPaddingSlice)
    #print("\tgdic: Initial Error (abs) = ", error)
    i = 0

    # We try to solve Md=F
    # while error > 0.1 and error < errorIn:
    # while error > 0.1 and i <= maxIterations and error < errorIn:
    dxNorm = numpy.inf
    while dxNorm > convergenceCriterion and i < maxIterations:
        i += 1
        # This function returns globalVector (F) taking in im1Def and im2 and the gradients
        globalVector = numpy.zeros((3 * points.shape[0]), dtype='<f8')
        DICToolkit.computeDICglobalVector(imTetLabel.astype("<u4"),
                                          im2Grad.astype("<f4"),
                                          im1Def.astype("<f4"),
                                          im2.astype("<f4"),
                                          tetra.astype("<u4"),
                                          points.astype("<f8"),
                                          globalVector)
        if applyBC:
            a1 = globalVector[nbc]
            a2 = globalVector[bc]
            # print("gdic: get reduced global considering boundary conditions")
            # print("gdic: global vector size: {}".format(globalVector.shape))
            dx = numpy.dot(globalMatrixInv, (a1 - numpy.dot(K12, numpy.dot(K22i, a2)))).astype('<f8')
            # dx = numpy.dot(globalMatrixInv, (globalVector[nbc] - numpy.dot(K12, displacements[bc]))).astype('<f8')
            displacements[nbc] += dx

        else:
            dx = numpy.dot(globalMatrixInv, globalVector).astype('<f8')
            displacements += dx

        dxNorm = numpy.linalg.norm(dx)

        # We generate a new im1def by adding the displacements to the nodes
        im1Def = numpy.zeros_like(im1, dtype="<f4")
        DICToolkit.applyMeshTransformation(im1.astype("<f4"),
                                           imTetLabel.astype("<u4"),
                                           im1Def,
                                           tetra.astype("<u4"),
                                           points.astype("<f8"),
                                           displacements.reshape(3, points.shape[0]).astype("<f8"))

        if debugFiles:
            #tifffile.imsave("{}-def-{:03d}.tif".format(prefix, i), im1Def[meshPaddingSlice])
            #tifffile.imsave("{}-residual-{:03d}.tif".format(prefix, i), im2[meshPaddingSlice]-im1Def[meshPaddingSlice])
            #spam.helpers.writeGlyphsVTK(points, pointData={"displacements": displacements.reshape(points.shape[0], 3)}, fileName="{}-displacementGlyph-{:03d}.vtk".format(prefix, i))
            spam.helpers.writeUnstructuredVTK(points.copy(), tetra.copy(), pointData={"displacements": displacements.reshape(points.shape[0], 3)}, fileName="{}-displacementFE-{:03d}.vtk".format(prefix, i), fileFormat='vtk-binary')

        #error = errorCalc(im2, im1Def, im1, meshPaddingSlice)

        # print("\t\tgdic: Error Out = %0.5f%%" % (error))
        reshapedDispl = displacements.reshape(points.shape[0], 3)
        dMin = numpy.min(reshapedDispl, axis=0)
        dMed = numpy.median(reshapedDispl, axis=0)
        dMax = numpy.max(reshapedDispl, axis=0)
        print("\ti={:03d}, displacements min={: .3f} {: .3f} {: .3f}, median={: .3f} {: .3f} {: .3f}, max={: .3f} {: .3f} {: .3f}, dx={:.2f}".format(
            i,
            dMin[0], dMin[1], dMin[2],
            dMed[0], dMed[1], dMed[2],
            dMax[0], dMax[1], dMax[2],
            dxNorm))

    return displacements.reshape(points.shape[0], 3)
