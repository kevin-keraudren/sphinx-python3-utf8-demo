# -*- coding: utf-8 -*-

"""
Maths look nicer with Greek letters.
"""

import numpy as np

def gaussian( x, μ, σ):
    """Gaussian distribution."""
    π = np.pi
    return 1/(σ*np.sqrt(2*π)) * np.exp(-(x-μ)**2/(2*σ**2))
