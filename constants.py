BANDS = {
    'sub-bass': (10, 60),
    'bass': (60, 250),
    'low-mid': (250, 500),
    'mid': (500, 2000),
    'high-mid': (2000, 4000),
    'presence': (4000, 6000),
    'brilliance': (6000, 10000),
    'ultra': (10000, 20000),
    'super-ultra': (20000, 40000),
}

WEIGHTS = {
    'sub-bass': 0.08,
    'bass': 0.12,
    'low-mid': 0.08,
    'mid': 0.12,
    'high-mid': 0.08,
    'presence': 0.12,
    'brilliance': 0.12,
    'ultra': 0.10,
    'super-ultra': 0.08,
    'flatness': 0.05,
    'centroid': 0.05,
}

TARGETS = {
    'sub-bass': (-20, 6),
    'bass': (-20, 6),
    'low-mid': (-20, 6),
    'mid': (-20, 6),
    'high-mid': (-20, 6),
    'presence': (-20, 6),
    'brilliance': (-20, 6),
    'ultra': (-25, 8),
    'super-ultra': (-30, 10),
    'flatness': (0.4, 0.2),
    'centroid': (5000, 2000),
}
