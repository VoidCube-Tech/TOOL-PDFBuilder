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
SECTION_BODY_LEADING
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


def _draw_footer(c, width, page_number):
    outline = _hex(THEME["outlineVariant"])
    on_primary_container = _hex(THEME["onPrimaryContainer"])

    footer_y = PAGE_MARGIN

    c.saveState()
    c.setStrokeColorRGB(*outline, alpha=0.5)
    c.setLineWidth(0.6)
    c.line(PAGE_MARGIN, footer_y + 14, width - PAGE_MARGIN, footer_y + 14)
    c.restoreState()

    _draw_tracked_text(c, PAGE_MARGIN, footer_y, "VOIDCUBE",
                        FONT_REGULAR, LABEL_SIZE, outline, LABEL_TRACKING)
    _draw_tracked_text(c, width - PAGE_MARGIN, footer_y,
                        f"{page_number:02d}", FONT_REGULAR, LABEL_SIZE,
                        on_primary_container, LABEL_TRACKING, anchor="right")

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