# FireSpark -- the Data Work
# Copyright 2020 The FireSpark Author. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""FireSpark label processing functions for datasets """

import numpy as np

def prepare_dirtylense_label(annotation):
	label = []
	for c in annotation.dl_cell:
		label.append((
			c.location.min.x,
			c.location.min.y,
			c.location.max.x,
			c.location.max.y,
			c.occlusion_type,
			c.occlusion_percentage,
			c.occlusion_density
		))
	assert len(label) == 36, "Unmatched label data to number of dirtylense cells!"
	return np.array(label)


