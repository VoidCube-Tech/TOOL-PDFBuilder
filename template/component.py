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
                        "AUDITORIA DIGITAL DE PRESENÇA ONLINE",
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

def _draw_cube(c, cx, cy, scale, theme):
    primary = _hex(theme["primary"])
    primary_container = _hex(theme["primaryContainer"])
    on_primary_container = _hex(theme["onPrimaryContainer"])
    tertiary_container = _hex(theme["tertiaryContainer"])

    p = lambda ix, iy, iz: _iso_point(cx, cy, ix, iy, iz, scale)

    top = [p(0, 1, 0), p(1, 1, 0), p(1, 1, 1), p(0, 1, 1)]
    left = [p(0, 0, 0), p(0, 1, 0), p(0, 1, 1), p(0, 0, 1)]
    right = [p(1, 0, 0), p(1, 1, 0), p(1, 1, 1), p(1, 0, 1)]

    def face(points, fill_color, alpha):
        c.saveState()
        c.setFillColorRGB(*fill_color, alpha=alpha)
        path = c.beginPath()
        path.moveTo(*points[0])
        for pt in points[1:]:
            path.lineTo(*pt)
        path.close()
        c.drawPath(path, stroke=0, fill=1)
        c.restoreState()

    def edge(points, color, alpha, width):
        c.saveState()
        c.setStrokeColorRGB(*color, alpha=alpha)
        c.setLineWidth(width)
        path = c.beginPath()
        path.moveTo(*points[0])
        for pt in points[1:]:
            path.lineTo(*pt)
        path.close()
        c.drawPath(path, stroke=1, fill=0)
        c.restoreState()

    # Sombra de contato, suave, abaixo do cubo.
    shadow_x, shadow_y = p(0.5, 0, 0.5)
    _glow(c, shadow_x, shadow_y - scale * 0.05, scale * 0.85, (0, 0, 0), 0.28)

    face(left, primary_container, 0.55)
    face(right, tertiary_container, 0.55)
    face(top, primary, 0.85)

    edge(top, on_primary_container, 0.9, 1.1)
    edge(left, primary, 0.35, 0.8)
    edge(right, primary, 0.35, 0.8)

    # Núcleo luminoso saindo da face superior, sugerindo conexão /
    # profundidade de dados dentro do cubo.
    core_x, core_y = p(0.5, 1, 0.5)
    _glow(c, core_x, core_y, scale * 0.55, primary, 0.16)
    _glow(c, core_x, core_y, scale * 0.22, primary, 0.30)

    # Pequenos nós conectados, saindo das arestas do topo, reforçando
    # a ideia de rede / conexão entre pontos.
    nodes = [p(0.15, 1, 0.85), p(0.85, 1, 0.15), p(0.5, 1, -0.05)]
    c.saveState()
    c.setStrokeColorRGB(*primary, alpha=0.35)
    c.setLineWidth(0.7)
    for nx, ny in nodes:
        c.line(core_x, core_y, nx, ny)
    c.restoreState()
    for nx, ny in nodes:
        c.saveState()
        c.setFillColorRGB(*primary, alpha=0.75)
        c.circle(nx, ny, 1.6, stroke=0, fill=1)
        c.restoreState()