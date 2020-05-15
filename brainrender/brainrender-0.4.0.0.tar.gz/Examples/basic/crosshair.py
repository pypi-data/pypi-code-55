"""
    This tutorial shows how to render a cross hair at a specific location in the scene
"""

from brainrender.scene import Scene

scene  = Scene()
scene.add_brain_regions('TH', use_original_color=False, alpha=.4)

# Add a point in the right hemisphere
point = scene.get_region_CenterOfMass('TH')
scene.add_crosshair_at_point(point, 
                        ap=False,  # show only lines on the medio-lateral and dorso-ventral axes
                        point_kwargs={'color':'salmon'} # specify how the point at the center of the crosshair looks like
                        )

# Add a point in the left hemisphere
point = scene.get_region_CenterOfMass('TH', hemisphere='left')
scene.add_crosshair_at_point(point, 
                        ap=False,  # show only lines on the medio-lateral and dorso-ventral axes
                        point_kwargs={'color':'darkseagreen'} # specify how the point at the center of the crosshair looks like
                        )

scene.render()