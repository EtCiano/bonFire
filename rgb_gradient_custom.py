import math


def _hex_to_rgb(color):
    """Converte '#rrggbb' para uma tupla (r, g, b)."""
    color = color.lstrip('#')
    return tuple(int(color[i:i + 2], 16) for i in (0, 2, 4))


def _rgb_to_hex(color):
    """Converte (r, g, b) para '#rrggbb'."""
    r, g, b = (max(0, min(255, round(c))) for c in color)
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)


def _normalize_color(color):
    """Aceita tupla RGB ou string hex e sempre retorna tupla (r, g, b)."""
    if isinstance(color, str):
        return _hex_to_rgb(color)
    return tuple(color)


def _distance(c1, c2):
    """Distância euclidiana entre dois pontos no espaço RGB (3D)."""
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(c1, c2)))


def get_linear_gradient(colors, nb_colors, return_format='rgb'):
    """
    Gera um gradiente linear passando pelas cores fornecidas.
    """
    if len(colors) < 2:
        raise ValueError("colors deve conter pelo menos 2 cores")
    if len(colors) > nb_colors:
        raise ValueError("nb_colors deve ser >= len(colors)")
    if nb_colors < 3:
        raise ValueError("nb_colors deve ser >= 3")
    if return_format not in ('rgb', 'hex'):
        raise ValueError("return_format deve ser 'rgb' ou 'hex'")

    points = [_normalize_color(c) for c in colors]

    segment_distances = [
        _distance(points[i], points[i + 1]) for i in range(len(points) - 1)
    ]
    total_distance = sum(segment_distances)

    nb_to_add = nb_colors - len(points)
    step = total_distance / (nb_to_add + 1) if total_distance > 0 else 0

    gradient = [points[0]]
    accumulated = 0.0
    remaining_to_add = nb_to_add

    for i in range(len(points) - 1):
        start, end = points[i], points[i + 1]
        seg_len = segment_distances[i]

        if seg_len == 0:
            continue

        dist_to_next_point = step - accumulated
        traveled = 0.0
        while remaining_to_add > 0 and dist_to_next_point <= seg_len - traveled + 1e-9:
            traveled += dist_to_next_point
            t = traveled / seg_len
            new_point = tuple(
                start[c] + (end[c] - start[c]) * t for c in range(3)
            )
            gradient.append(new_point)
            remaining_to_add -= 1
            dist_to_next_point = step

        accumulated = seg_len - traveled
        gradient.append(end)

    if return_format == 'hex':
        return [_rgb_to_hex(c) for c in gradient]
    return [tuple(round(c) for c in color) for color in gradient]