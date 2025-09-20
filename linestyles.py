from enum import Enum

class LineStyle(Enum):
    SOLID = "solid"
    DOTTED = "dotted"
    DASHED = "dashed"
    DASHDOT = "dashdot"

    LOOSELY_DOTTED = "loosely dotted"
    DENSELY_DOTTED = "densely dotted"

    LONG_DASH_WITH_OFFSET = "long dash with offset"
    LOOSELY_DASHED = "loosely dashed"
    DENSELY_DASHED = "densely dashed"

    LOOSELY_DASHDOTTED = "loosely dashdotted"
    DASHDOTTED = "dashdotted"
    DENSELY_DASHDOTTED = "densely dashdotted"

    DASHDOTDOTTED = "dashdotdotted"
    LOOSELY_DASHDOTDOTTED = "loosely dashdotdotted"
    DENSELY_DASHDOTDOTTED = "densely dashdotdotted"


line_styles_dict = {
    LineStyle.SOLID: 'solid',      # Same as (0, ()) or '-'
    LineStyle.DASHED: 'dashed',    # Same as '--'
    LineStyle.DOTTED: 'dotted',    # Same as ':'
    LineStyle.DASHDOT: 'dashdot',  # Same as '-.'
    
    LineStyle.LONG_DASH_WITH_OFFSET: (5, (10, 3)),
    LineStyle.LOOSELY_DASHED:        (0, (5, 10)),
    LineStyle.DASHED:                (0, (5, 5)),
    LineStyle.DENSELY_DASHED:        (0, (5, 1)),

    LineStyle.LOOSELY_DOTTED:        (0, (1, 10)),
    LineStyle.DOTTED:                (0, (1, 5)),
    LineStyle.DENSELY_DOTTED:        (0, (1, 1)),

    LineStyle.LOOSELY_DASHDOTTED:    (0, (3, 10, 1, 10)),
    LineStyle.DASHDOTTED:            (0, (3, 5, 1, 5)),
    LineStyle.DENSELY_DASHDOTTED:    (0, (3, 1, 1, 1)),

    LineStyle.DASHDOTDOTTED:         (0, (3, 5, 1, 5, 1, 5)),
    LineStyle.LOOSELY_DASHDOTDOTTED: (0, (3, 10, 1, 10, 1, 10)),
    LineStyle.DENSELY_DASHDOTDOTTED: (0, (3, 1, 1, 1, 1, 1)),
}

line_styles_list = list(line_styles_dict.values())