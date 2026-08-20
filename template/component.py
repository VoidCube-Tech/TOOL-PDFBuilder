from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import stringWidth

from .theme import THEME

from .const import (
PAGE_MARGIN,
KICKER_SIZE,
KICKER_TRACKING,

BRAND_SIZE,
BRAND_TRACKING,

TITLE_SIZE,
TITLE_LEADING,

SUBTITLE_SIZE,
SUBTITLE_LEADING,

LABEL_SIZE,
LABEL_TRACKING,
VALUE_SIZE,

FONT_REGULAR,
FONT_BOLD,

CARD_TITLE_SIZE,
CARD_LABEL_SIZE,
CARD_LABEL_TRACKING,
CARD_BODY_SIZE,
CARD_BODY_LEADING,

SECTION_TITLE_SIZE,
SECTION_TITLE_LEADING,
SECTION_BODY_SIZE,
SECTION_BODY_LEADING,

SCORE_SIZE,
SCORE_UNIT_SIZE,

CATEGORY_NAME_SIZE,
CATEGORY_VALUE_SIZE,
CATEGORY_ROW_H,
CATEGORY_BAR_H,

COLUMN_KICKER_SIZE,
COLUMN_KICKER_TRACKING,
ITEM_SIZE,
ITEM_LEADING,
ITEM_GAP,

FINDING_CATEGORY_SIZE,
FINDING_CATEGORY_TRACKING,
FINDING_TITLE_SIZE,
FINDING_TITLE_LEADING,
FINDING_BODY_SIZE,
FINDING_BODY_LEADING,
FINDING_IMPACT_SIZE,
FINDING_IMPACT_LEADING,

CTA_TEXT_SIZE,
CTA_NOTE_SIZE,

CONTACT_LABEL_SIZE,
CONTACT_LABEL_TRACKING,
CONTACT_VALUE_SIZE,

TAGLINE_SIZE,

BENEFIT_TITLE_SIZE,
BENEFIT_DESC_SIZE,
BENEFIT_DESC_LEADING,

FLOW_LABEL_SIZE,

CHART_LABEL_SIZE,
CHART_PAD_TOP,
CHART_PAD_BOTTOM,

STAT_LABEL_SIZE,
STAT_LABEL_TRACKING,
STAT_VALUE_SIZE,

INTERPRETATION_SIZE,
INTERPRETATION_LEADING,

RAIL_X_OFFSET,
CONTENT_X_OFFSET,

TIER_LABEL_SIZE,
TIER_LABEL_TRACKING,
TIER_DESC_SIZE,
TIER_DESC_LEADING,

ITEM_TITLE_SIZE,
ITEM_TITLE_LEADING,
ITEM_DESC_SIZE,
ITEM_DESC_LEADING,
ITEM_TAG_SIZE,

TIER_GAP,
ITEM_GAP,

TIERS
)

def _hex(value):
    value = value.lstrip("#")
    return tuple(int(value[i:i + 2], 16) / 255.0 for i in (0, 2, 4))


def _draw_tracked_text(c, x, y, text, font, size, color, tracking=0.0, anchor="left"):
    """Desenha texto com espaçamento entre letras (tracking) manual.

    O ReportLab não tem tracking nativo no canvas, então avançamos
    caractere a caractere. anchor pode ser 'left' ou 'right'.
    """
    c.setFont(font, size)
    c.setFillColorRGB(*color)

    widths = [pdfmetrics.stringWidth(ch, font, size) for ch in text]
    total = sum(widths) + tracking * max(len(text) - 1, 0)

    cursor = x - total if anchor == "right" else x
    for ch, w in zip(text, widths):
        c.drawString(cursor, y, ch)
        cursor += w + tracking

def _draw_header(c, width, height, page_number):
    on_bg = _hex(THEME["onBackground"])
    muted = _hex(THEME["onSurfaceVariant"])
    outline = _hex(THEME["outlineVariant"])

    top_y = height - PAGE_MARGIN

    _draw_tracked_text(c, PAGE_MARGIN, top_y - 12, "VOIDCUBE", FONT_BOLD,
                        BRAND_SIZE * 0.85, on_bg, BRAND_TRACKING)

    _draw_tracked_text(c, width - PAGE_MARGIN, top_y - 9,
                        "AUDITORIA DIGITAL",
                        FONT_REGULAR, KICKER_SIZE, muted, KICKER_TRACKING,
                        anchor="right")
    _draw_tracked_text(c, width - PAGE_MARGIN, top_y - 20,
                        f"PÁGINA {page_number:02d}", FONT_REGULAR,
                        KICKER_SIZE, muted, KICKER_TRACKING, anchor="right")

    c.saveState()
    c.setStrokeColorRGB(*outline, alpha=0.5)
    c.setLineWidth(0.6)
    c.line(PAGE_MARGIN, top_y - 30, width - PAGE_MARGIN, top_y - 30)
    c.restoreState()

def _draw_footer(c, width, company_name, page_number, total_pages=None):
    outline = _hex(THEME["outlineVariant"])
    muted = _hex(THEME["onSurfaceVariant"])
    on_primary_container = _hex(THEME["onPrimaryContainer"])

    footer_y = PAGE_MARGIN

    c.saveState()
    c.setStrokeColorRGB(*outline, alpha=0.5)
    c.setLineWidth(0.6)
    c.line(PAGE_MARGIN, footer_y + 14, width - PAGE_MARGIN, footer_y + 14)
    c.restoreState()

    _draw_tracked_text(c, PAGE_MARGIN, footer_y, "VOIDCUBE",
                        FONT_REGULAR, LABEL_SIZE, muted, LABEL_TRACKING)

    page_text = f"{page_number:02d}"
    if total_pages:
        page_text = f"{page_number:02d} / {total_pages:02d}"

    _draw_tracked_text(c, width - PAGE_MARGIN, footer_y, page_text,
                        FONT_REGULAR, LABEL_SIZE, on_primary_container, LABEL_TRACKING,
                        anchor="right")

    c.setFont(FONT_REGULAR, LABEL_SIZE + 1.5)
    c.setFillColorRGB(*muted)
    c.drawCentredString(width / 2, footer_y, company_name)

def _wrap(text, font, size, max_width):
    words = text.split()
    lines = []
    current = ""
    for word in words:
        trial = f"{current} {word}".strip()
        if stringWidth(trial, font, size) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines

def _glow(c, cx, cy, radius, color, alpha):
    c.saveState()
    c.setFillColorRGB(*color, alpha=alpha)
    c.circle(cx, cy, radius, stroke=0, fill=1)
    c.restoreState()


def _radial_glow(c, cx, cy, max_radius, color, layer_alpha, steps=10):
    """Aproxima um brilho radial suave empilhando círculos concêntricos
    com alpha baixo e constante. Como as camadas se sobrepõem mais perto
    do centro, o resultado é um degradê suave sem borda dura visível.
    """
    c.saveState()
    c.setFillColorRGB(*color, alpha=layer_alpha)
    for i in range(steps, 0, -1):
        r = max_radius * (i / steps)
        c.circle(cx, cy, r, stroke=0, fill=1)
    c.restoreState()


def _iso_point(cx, cy, ix, iy, iz, scale):
    """Projeção isométrica simples de coordenadas (ix, iy, iz) -> (x, y)."""
    x = cx + (ix - iz) * scale * 0.866
    y = cy + (ix + iz) * scale * 0.5 - iy * scale
    return x, y

def _draw_cube(c, cx, cy, scale, theme, svg_path=None):
    primary = _hex("#00FFFF")
    cyan = _hex("#00CED1")
    dark = _hex("#050708")
    surface = _hex("#0A0A0A")
    surface2 = _hex("#111111")
    grid = _hex("#12383B")

    p = lambda x, y, z: _iso_point(cx, cy, x, y, z, scale)

    def polygon(points, fill=None, stroke=None, alpha=1.0, width=1.0):
        c.saveState()

        if fill is not None:
            c.setFillColorRGB(*fill, alpha=alpha)

        if stroke is not None:
            c.setStrokeColorRGB(*stroke, alpha=alpha)
            c.setLineWidth(width)

        path = c.beginPath()
        path.moveTo(*points[0])

        for pt in points[1:]:
            path.lineTo(*pt)

        path.close()

        c.drawPath(
            path,
            stroke=1 if stroke is not None else 0,
            fill=1 if fill is not None else 0
        )

        c.restoreState()

    def line(points, color, alpha=1.0, width=1.0):
        c.saveState()
        c.setStrokeColorRGB(*color, alpha=alpha)
        c.setLineWidth(width)

        path = c.beginPath()
        path.moveTo(*points[0])

        for pt in points[1:]:
            path.lineTo(*pt)

        c.drawPath(path, stroke=1, fill=0)

        c.restoreState()

    def rounded_quad(points, fill, stroke=None, alpha=1.0, width=1.0, radius=0.12):
        center_x = sum(x for x, _ in points) / 4
        center_y = sum(y for _, y in points) / 4

        inset = radius

        pts = [
            (
                x + (center_x - x) * inset,
                y + (center_y - y) * inset
            )
            for x, y in points
        ]

        a, b, cc, d = pts

        k = 0.22

        ab = (
            a[0] + (b[0] - a[0]) * k,
            a[1] + (b[1] - a[1]) * k
        )

        bc = (
            b[0] + (cc[0] - b[0]) * k,
            b[1] + (cc[1] - b[1]) * k
        )

        cd = (
            cc[0] + (d[0] - cc[0]) * k,
            cc[1] + (d[1] - cc[1]) * k
        )

        da = (
            d[0] + (a[0] - d[0]) * k,
            d[1] + (a[1] - d[1]) * k
        )

        path = c.beginPath()

        path.moveTo(*ab)

        path.curveTo(
            b[0], b[1],
            b[0], b[1],
            *bc
        )

        path.curveTo(
            cc[0], cc[1],
            cc[0], cc[1],
            *cd
        )

        path.curveTo(
            d[0], d[1],
            d[0], d[1],
            *da
        )

        path.curveTo(
            a[0], a[1],
            a[0], a[1],
            *ab
        )

        c.saveState()

        c.setFillColorRGB(*fill, alpha=alpha)

        if stroke is not None:
            c.setStrokeColorRGB(*stroke, alpha=alpha)
            c.setLineWidth(width)

        c.drawPath(
            path,
            stroke=1 if stroke else 0,
            fill=1
        )

        c.restoreState()

    def glow_point(x, y, radius, alpha):
        _glow(
            c,
            x,
            y,
            radius,
            primary,
            alpha
        )

    def glowing_line(points, width):
        # Halo externo
        line(
            points,
            primary,
            alpha=0.07,
            width=width * 4.5
        )

        # Halo próximo
        line(
            points,
            primary,
            alpha=0.15,
            width=width * 2.3
        )

        # Núcleo
        line(
            points,
            cyan,
            alpha=0.95,
            width=width
        )

    def face_cell(face, row, col):
        u0 = col / 3
        u1 = (col + 1) / 3

        v0 = row / 3
        v1 = (row + 1) / 3

        if face == "top":
            return [
                p(u0, 1, v0),
                p(u1, 1, v0),
                p(u1, 1, v1),
                p(u0, 1, v1)
            ]

        if face == "front":
            return [
                p(u0, v0, 1),
                p(u1, v0, 1),
                p(u1, v1, 1),
                p(u0, v1, 1)
            ]

        return [
            p(1, v0, u0),
            p(1, v1, u0),
            p(1, v1, u1),
            p(1, v0, u1)
        ]

    def technical_texture(pts, face, row, col):
        center = (
            sum(x for x, _ in pts) / 4,
            sum(y for _, y in pts) / 4
        )

        cx2, cy2 = center

        glow_point(
            cx2,
            cy2,
            scale * 0.035,
            0.035
        )

        a, b, cc, d = pts

        for t in (0.28, 0.52, 0.76):
            if face == "top":
                x1, y1 = (
                    a[0] + (b[0] - a[0]) * t,
                    a[1] + (b[1] - a[1]) * t
                )

                x2, y2 = (
                    d[0] + (cc[0] - d[0]) * t,
                    d[1] + (cc[1] - d[1]) * t
                )

            elif face == "front":
                x1, y1 = (
                    a[0] + (b[0] - a[0]) * t,
                    a[1] + (b[1] - a[1]) * t
                )

                x2, y2 = (
                    d[0] + (cc[0] - d[0]) * t,
                    d[1] + (cc[1] - d[1]) * t
                )

            else:
                x1, y1 = (
                    a[0] + (d[0] - a[0]) * t,
                    a[1] + (d[1] - a[1]) * t
                )

                x2, y2 = (
                    b[0] + (cc[0] - b[0]) * t,
                    b[1] + (cc[1] - b[1]) * t
                )

            line(
                [(x1, y1), (x2, y2)],
                grid,
                alpha=0.30,
                width=max(0.25, scale * 0.002)
            )

        # pequenos nós de circuito
        node_positions = (
            (0.27, 0.31),
            (0.72, 0.68)
        )

        for u, v in node_positions:
            x = (
                a[0]
                + (b[0] - a[0]) * u
                + (d[0] - a[0]) * v
            )

            y = (
                a[1]
                + (b[1] - a[1]) * u
                + (d[1] - a[1]) * v
            )

            c.saveState()
            c.setFillColorRGB(*grid, alpha=0.65)

            c.circle(
                x,
                y,
                max(0.5, scale * 0.004),
                stroke=0,
                fill=1
            )

            c.restoreState()

    def cavity(pts, depth=0.55):
        center = (
            sum(x for x, _ in pts) / 4,
            sum(y for _, y in pts) / 4
        )

        inner = [
            (
                center[0] + (x - center[0]) * depth,
                center[1] + (y - center[1]) * depth
            )
            for x, y in pts
        ]

        # sombra externa
        rounded_quad(
            pts,
            fill=_hex("#020303"),
            alpha=1.0,
            radius=0.12
        )

        # parede interna
        rounded_quad(
            inner,
            fill=_hex("#000000"),
            stroke=_hex("#06272A"),
            alpha=1.0,
            width=max(0.45, scale * 0.004),
            radius=0.08
        )

        # núcleo absolutamente escuro
        inner2 = [
            (
                center[0] + (x - center[0]) * 0.62,
                center[1] + (y - center[1]) * 0.62
            )
            for x, y in inner
        ]

        rounded_quad(
            inner2,
            fill=_hex("#000000"),
            alpha=1.0,
            radius=0.05
        )

    # ============================================================
    # FUNDO / HALO
    # ============================================================

    shadow_x, shadow_y = p(0.5, 0, 0.5)

    _glow(
        c,
        shadow_x,
        shadow_y + scale * 0.04,
        scale * 0.72,
        _hex("#00FFFF"),
        0.035
    )

    _glow(
        c,
        shadow_x,
        shadow_y + scale * 0.04,
        scale * 0.42,
        _hex("#00FFFF"),
        0.025
    )

    # sombra de contato
    _glow(
        c,
        shadow_x,
        shadow_y - scale * 0.035,
        scale * 0.62,
        _hex("#000000"),
        0.60
    )

    # ============================================================
    # CORPO 3D
    # ============================================================

    top = [
        p(0, 1, 0),
        p(1, 1, 0),
        p(1, 1, 1),
        p(0, 1, 1)
    ]

    front = [
        p(0, 0, 1),
        p(1, 0, 1),
        p(1, 1, 1),
        p(0, 1, 1)
    ]

    right = [
        p(1, 0, 0),
        p(1, 1, 0),
        p(1, 1, 1),
        p(1, 0, 1)
    ]

    polygon(
        top,
        fill=_hex("#0A0A0A"),
        alpha=1.0
    )

    polygon(
        front,
        fill=_hex("#080909"),
        alpha=1.0
    )

    polygon(
        right,
        fill=_hex("#050606"),
        alpha=1.0
    )

    # ============================================================
    # SUBCUBOS
    # ============================================================

    faces = (
        ("top", top),
        ("front", front),
        ("right", right)
    )

    for face_name, _ in faces:
        for row in range(3):
            for col in range(3):

                pts = face_cell(
                    face_name,
                    row,
                    col
                )

                # Cavidade no centro do topo
                if (
                    face_name == "top"
                    and row == 1
                    and col == 1
                ):
                    cavity(pts)
                    continue

                # Cavidade inferior direita da face direita
                if (
                    face_name == "right"
                    and row == 2
                    and col == 2
                ):
                    cavity(pts, depth=0.52)
                    continue

                rounded_quad(
                    pts,
                    fill=_hex("#0A0A0A"),
                    stroke=_hex("#102426"),
                    alpha=1.0,
                    width=max(0.4, scale * 0.003),
                    radius=0.105
                )

                technical_texture(
                    pts,
                    face_name,
                    row,
                    col
                )

    # ============================================================
    # DIVISÕES INTERNAS
    # ============================================================

    structural = [
        # topo
        (p(1 / 3, 1, 0), p(1 / 3, 1, 1)),
        (p(2 / 3, 1, 0), p(2 / 3, 1, 1)),
        (p(0, 1, 1 / 3), p(1, 1, 1 / 3)),
        (p(0, 1, 2 / 3), p(1, 1, 2 / 3)),

        # frente
        (p(1 / 3, 0, 1), p(1 / 3, 1, 1)),
        (p(2 / 3, 0, 1), p(2 / 3, 1, 1)),
        (p(0, 1 / 3, 1), p(1, 1 / 3, 1)),
        (p(0, 2 / 3, 1), p(1, 2 / 3, 1)),

        # direita
        (p(1, 1 / 3, 0), p(1, 1 / 3, 1)),
        (p(1, 2 / 3, 0), p(1, 2 / 3, 1)),
        (p(1, 0, 1 / 3), p(1, 1, 1 / 3)),
        (p(1, 0, 2 / 3), p(1, 1, 2 / 3))
    ]

    for a, b in structural:
        glowing_line(
            [a, b],
            max(0.65, scale * 0.007)
        )

    # ============================================================
    # BORDAS EXTERNAS
    # ============================================================

    external_edges = [
        [p(0, 1, 0), p(1, 1, 0)],
        [p(1, 1, 0), p(1, 1, 1)],
        [p(1, 1, 1), p(0, 1, 1)],
        [p(0, 1, 1), p(0, 1, 0)],

        [p(0, 0, 1), p(1, 0, 1)],
        [p(1, 0, 1), p(1, 1, 1)],
        [p(0, 0, 1), p(0, 1, 1)],

        [p(1, 0, 0), p(1, 1, 0)],
        [p(1, 0, 0), p(1, 0, 1)]
    ]

    for edge in external_edges:
        glowing_line(
            edge,
            max(1.0, scale * 0.011)
        )

    # ============================================================
    # CAVIDADE SUPERIOR
    # ============================================================

    top_hole = face_cell(
        "top",
        1,
        1
    )

    center = (
        sum(x for x, _ in top_hole) / 4,
        sum(y for _, y in top_hole) / 4
    )

    glow_point(
        center[0],
        center[1],
        scale * 0.18,
        0.08
    )

    # ============================================================
    # BROKEN CYAN LIGHT
    # ============================================================

    broken = [
        (
            p(1 / 3, 0, 1)[0],
            p(1 / 3, 0, 1)[1]
        ),
        (
            p(0.43, 0, 1)[0],
            p(0.43, 0, 1)[1]
        ),
        (
            p(0.47, 0, 1)[0],
            p(0.47, 0, 1)[1]
        ),
        (
            p(0.56, 0, 1)[0],
            p(0.56, 0, 1)[1]
        ),
        (
            p(0.61, 0, 1)[0],
            p(0.61, 0, 1)[1]
        ),
        (
            p(2 / 3, 0, 1)[0],
            p(2 / 3, 0, 1)[1]
        )
    ]

    for i in range(len(broken) - 1):
        if i in (1, 3):
            continue

        glowing_line(
            broken[i:i + 2],
            max(0.75, scale * 0.008)
        )

    # ============================================================
    # PEQUENOS REFLEXOS CYAN
    # ============================================================

    highlights = [
        [p(0.03, 0.10, 1), p(0.03, 0.35, 1)],
        [p(0.97, 0.10, 1), p(0.97, 0.32, 1)],
        [p(1, 0.08, 0.08), p(1, 0.28, 0.08)],
        [p(0.08, 1, 0.04), p(0.30, 1, 0.04)]
    ]

    for pts in highlights:
        line(
            pts,
            cyan,
            alpha=0.25,
            width=max(0.35, scale * 0.004)
        )

    # ============================================================
    # NÓS LUMINOSOS DISCRETOS
    # ============================================================

    nodes = [
        p(0.16, 1, 0.84),
        p(0.84, 1, 0.16),
        p(0.16, 0.34, 1),
        p(0.84, 0.67, 1)
    ]

    for nx, ny in nodes:
        glow_point(
            nx,
            ny,
            scale * 0.035,
            0.10
        )

        c.saveState()
        c.setFillColorRGB(*cyan, alpha=0.75)

        c.circle(
            nx,
            ny,
            max(0.8, scale * 0.006),
            stroke=0,
            fill=1
        )

        c.restoreState()