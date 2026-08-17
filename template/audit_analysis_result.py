from reportlab.pdfbase.pdfmetrics import stringWidth

from .audit_home import (
    THEME,
    PAGE_MARGIN,
    FONT_REGULAR,
    FONT_BOLD,
    KICKER_SIZE,
    KICKER_TRACKING,
    LABEL_SIZE,
    LABEL_TRACKING,
    _hex,
    _draw_tracked_text,
    _radial_glow,
    _draw_cube,
)
from .audit_evaluation import _draw_header, _wrap

SECTION_TITLE_SIZE = 22
SECTION_TITLE_LEADING = 27
BODY_SIZE = 10.6
BODY_LEADING = 16

SCORE_SIZE = 52
SCORE_UNIT_SIZE = 12.5

CATEGORY_NAME_SIZE = 10.2
CATEGORY_VALUE_SIZE = 9.6
CATEGORY_ROW_H = 30
CATEGORY_BAR_H = 7


def _draw_gauge(c, cx, cy, radius, score, max_score=100):
    track = _hex(THEME["surfaceContainerHigh"])
    fill = _hex(THEME["primary"])

    c.saveState()
    c.setLineCap(1)

    c.setStrokeColorRGB(*track, alpha=0.9)
    c.setLineWidth(14)
    c.arc(cx - radius, cy - radius, cx + radius, cy + radius, 180, -180)

    ratio = max(0.0, min(1.0, score / max_score))
    c.setStrokeColorRGB(*fill, alpha=0.95)
    c.setLineWidth(14)
    c.arc(cx - radius, cy - radius, cx + radius, cy + radius, 180, -180 * ratio)
    c.restoreState()

    c.saveState()
    c.setStrokeColorRGB(*fill, alpha=0.4)
    c.setLineWidth(0.8)
    c.circle(cx, cy, radius - 24, stroke=1, fill=0)
    c.restoreState()

    on_bg = _hex(THEME["onBackground"])
    muted = _hex(THEME["onSurfaceVariant"])

    c.setFont(FONT_BOLD, SCORE_SIZE)
    c.setFillColorRGB(*on_bg)
    score_text = str(int(score))
    score_w = stringWidth(score_text, FONT_BOLD, SCORE_SIZE)
    c.drawString(cx - score_w / 2, cy - radius * 0.42 + 25, score_text)

    unit_text = f"de {int(max_score)} pontos"
    c.setFont(FONT_REGULAR, SCORE_UNIT_SIZE)
    c.setFillColorRGB(*muted)
    unit_w = stringWidth(unit_text, FONT_REGULAR, SCORE_UNIT_SIZE)
    c.drawString(cx - unit_w / 2, cy - radius * 0.42 + 5, unit_text)


def _draw_category_row(c, x, y, w, name, score, max_score=10):
    on_bg = _hex(THEME["onBackground"])
    muted = _hex(THEME["onSurfaceVariant"])
    track = _hex(THEME["surfaceContainerHigh"])
    fill = _hex(THEME["primary"])
    outline = _hex(THEME["outlineVariant"])

    c.setFont(FONT_REGULAR, CATEGORY_NAME_SIZE)
    c.setFillColorRGB(*on_bg)
    c.drawString(x, y, name)

    value_text = f"{score}/{max_score}"
    c.setFont(FONT_REGULAR, CATEGORY_VALUE_SIZE)
    c.setFillColorRGB(*muted)
    c.drawRightString(x + w, y, value_text)

    bar_x = x + 175
    bar_w = w - 175 - 46
    bar_y = y - 1.5

    c.saveState()
    c.setFillColorRGB(*track, alpha=0.8)
    c.roundRect(bar_x, bar_y, bar_w, CATEGORY_BAR_H, CATEGORY_BAR_H / 2, stroke=0, fill=1)
    c.restoreState()

    ratio = max(0.0, min(1.0, score / max_score))
    fill_w = max(bar_w * ratio, CATEGORY_BAR_H)
    c.saveState()
    c.setFillColorRGB(*fill, alpha=0.9)
    c.roundRect(bar_x, bar_y, fill_w, CATEGORY_BAR_H, CATEGORY_BAR_H / 2, stroke=0, fill=1)
    c.restoreState()

    c.saveState()
    c.setStrokeColorRGB(*outline, alpha=0.35)
    c.setLineWidth(0.5)
    c.line(x, y - CATEGORY_ROW_H + 10, x + w, y - CATEGORY_ROW_H + 10)
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


def render_analysis_result(
    c,
    company_name: str,
    score_description: str,
    categories: list,
    max_score: int = 100,
    page_number: int = 3,
    total_pages: int | None = None,
):
    width, height = c._pagesize
    m = PAGE_MARGIN

    score = int(sum(cat["score"] for cat in categories) / len(categories))
    on_bg = _hex(THEME["onBackground"])
    muted = _hex(THEME["onSurfaceVariant"])
    primary = _hex(THEME["primary"])
    outline = _hex(THEME["outlineVariant"])
    container = _hex(THEME["primaryContainer"])
    surface = _hex(THEME["surfaceContainer"])

    c.setFillColorRGB(*_hex(THEME["background"]))
    c.rect(0, 0, width, height, stroke=0, fill=1)

    _radial_glow(c, width * 1.08, height * 0.72, width * 0.4, primary, 0.011, steps=24)
    _radial_glow(c, width * -0.08, height * 0.05, width * 0.35, container, 0.014, steps=20)

    _draw_header(c, width, height, page_number)

    top_y = height - m - 30
    section_y = top_y - 46

    _draw_tracked_text(c, m, section_y, "RESULTADO DA ANÁLISE", FONT_REGULAR,
                        KICKER_SIZE, primary, KICKER_TRACKING)

    title_lines = [
        "Isto é o que sua presença digital",
        "está comunicando agora.",
    ]
    ty = section_y - 34
    c.setFont(FONT_BOLD, SECTION_TITLE_SIZE)
    for line in title_lines:
        c.setFillColorRGB(*on_bg)
        c.drawString(m, ty, line)
        ty -= SECTION_TITLE_LEADING

    panel_top = ty - 30
    panel_h = 208
    panel_w = width - 2 * m

    c.saveState()
    c.setFillColorRGB(*surface, alpha=0.4)
    c.setStrokeColorRGB(*outline, alpha=0.45)
    c.setLineWidth(0.7)
    c.roundRect(m, panel_top - panel_h, panel_w, panel_h, 8, stroke=1, fill=1)
    c.restoreState()

    gauge_cx = m + panel_w * 0.24
    gauge_cy = panel_top - panel_h * 0.42
    gauge_radius = 78

    _draw_gauge(c, gauge_cx, gauge_cy, gauge_radius, score, max_score)

    desc_x = m + panel_w * 0.46
    desc_w = panel_w * 0.46

    _draw_tracked_text(c, desc_x, panel_top - 34, "LEITURA DO RESULTADO",
                        FONT_REGULAR, LABEL_SIZE, muted, LABEL_TRACKING)

    desc_lines = _wrap(score_description, FONT_REGULAR, BODY_SIZE, desc_w)
    dy = panel_top - 56
    c.setFont(FONT_REGULAR, BODY_SIZE)
    for line in desc_lines:
        c.setFillColorRGB(*on_bg)
        c.drawString(desc_x, dy, line)
        dy -= BODY_LEADING

    cube_scale = width * 0.045
    _draw_cube(c, width - m - cube_scale * 1.1, panel_top - panel_h + cube_scale * 0.9,
               cube_scale, THEME)

    cat_top = panel_top - panel_h - 40

    _draw_tracked_text(c, m, cat_top, "ÁREAS AVALIADAS", FONT_REGULAR,
                        KICKER_SIZE, primary, KICKER_TRACKING)

    row_y = cat_top - 30
    for category in categories:
        name = category.get("name", "")
        cat_score = category.get("score", 0)
        cat_max = category.get("max", 10)
        _draw_category_row(c, m, row_y, panel_w, name, cat_score, cat_max)
        row_y -= CATEGORY_ROW_H

    _draw_footer(c, width, company_name, page_number, total_pages)

    c.showPage()