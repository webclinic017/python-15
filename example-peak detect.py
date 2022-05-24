#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 17 00:38:08 2022

@author: bronx
"""

import numpy as np
import peakdetect

vector = [
    0, 6, 25, 20, 15, 8, 15, 6, 0, 6, 0, -5, -15, -3, 4, 10, 8, 13, 8, 10, 3,
    1, 20, 7, 3, 0 ]

print('Detect peaks with distance filters.')
peaks = peakdetect.peakdetect(np.array(vector), lookahead=1, delta=2)
# peakdetect returns two lists, respectively positive and negative peaks,
# with for each peak a tuple of (indexes, values).
indexes = []
for posOrNegPeaks in peaks:
    for peak in posOrNegPeaks:
        indexes.append(peak[0])
print('Peaks are: %s' % (indexes))
