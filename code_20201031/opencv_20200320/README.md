# OpenCV - Python

```python
         width ~ columns
        |-------------|
        |             |
 height |    image    |
~ rows  |             | 
        |-------------|
```

Image's Shape is: Height - Width - Deep(Channel)

OpenCV use **BGR** odering instead of RGB. So, for example, if you want to use the image read by OpenCV in *Matplotlib*, we should *convert BGR to RGB*.

**ROIs => “Regions of Interest”**: important skill in image processing

## Rotating image
1. Compute the image center
2. Construct the **rotation matrix**
3. Apply the **affine warp** on image

**Note**
- **positive** angles are **counterclockwise**
- **negative** angles are **clockwise**
- the image **rotated** by OpenCV is **clipped** (in fact, OpenCV *doesn't care* that, check [this doc](https://www.pyimagesearch.com/2017/01/02/rotate-images-correctly-with-opencv-and-python/) to solve that problem)

```python
center = w // 2, h // 2
rotation_matrix = cv2.getRotationMatrix2D(center, -45, 1.0)
rotated = cv2.warpAffine(img, rotation_matrix, (w, h))
```

## Blurring image
**Note**
- **Larger kernels** would yield a **more blurry** image
- **Smaller kernels** will create **less blurry** image

## Drawing on image
With OpenCV, **drawing** operations on images are **performed in-place**
- rectangle
- circle
- text
- etc

## Detection
### Edge
**Canny** algorithm, developed by John F.Canny
- Apply algo on the entire image
- Apply algo on each channel of image

### Color
Basic steps
1. Define lower and upper limits
2. Create **mask** with ```cv2.inRange()```
3. Apply mask on image

### Shape
- Find contours + Color detection or Thresholding
- Calculate moment -> *centroid*

## Thresholding
Help us to remove lighter or darker regions and contours of images

## Dilations and Erosions
### Dilation
Dilation **expands** the connected sets of 1s of a binary image.<br>
It can be used for:
- Growing features
- Filling holes and gaps

### Erosion
Erosion **shrinks** the connected sets of 1s of a binary image.<br>
It can be used for:
- Shrinking features
- Removing bridges, branches, protrusions

### Conclu
Erosions and dilations are typically used to **reduce noise in binary images** (a side effect of thresholding).

## Masking
Masks allow us to *mask out regions* of an image we are *uninterested* in. We call them **masks** because they will **hide** regions of images we do not care about.

## L*a*b* color space
- L*: lightness from black (0) to white (100)
- a*: color channel, from green (−) to red (+)
- b*: color channel, from blue (−) to yellow (+)

## Splitting and Merging Image Channels
The **channels** of an image can be **split** into their individual planes when needed. Then, the individual channels can be **merged back** together to form a image again. 

## Optical Mark Recognition 
OMR for short, is the process of automatically analyzing human-marked documents and interpreting their results.