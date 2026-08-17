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
from .audit_analysis_result import _draw_footer

SECTION_TITLE_SIZE = 22
SECTION_TITLE_LEADING = 27

COLUMN_KICKER_SIZE = 8.6
COLUMN_KICKER_TRACKING = 1.8
ITEM_SIZE = 9.8
ITEM_LEADING = 13.6
ITEM_GAP = 9

FINDING_CATEGORY_SIZE = 8.2
FINDING_CATEGORY_TRACKING = 2.0
FINDING_TITLE_SIZE = 18
FINDING_TITLE_LEADING = 23
FINDING_BODY_SIZE = 10.4
FINDING_BODY_LEADING = 15.4
FINDING_IMPACT_SIZE = 10.0
FINDING_IMPACT_LEADING = 14.8


def _draw_finding_list(c, x, y_top, w, kicker, items, accent):
    on_bg = _hex(THEME["onBackground"])

    _draw_tracked_text(c, x, y_top, kicker, FONT_REGULAR, COLUMN_KICKER_SIZE,
                        accent, COLUMN_KICKER_TRACKING)

    y = y_top - 26
    c.setFont(FONT_REGULAR, ITEM_SIZE)

    for item in items:
        c.saveState()
        c.setFillColorRGB(*accent, alpha=0.9)
        c.circle(x + 2, y + 2.5, 2.5, stroke=0, fill=1)
        c.restoreState()

        lines = _wrap(item, FONT_REGULAR, ITEM_SIZE, w - 18)
        c.setFillColorRGB(*on_bg)
        for line in lines:
            c.drawString(x + 8, y, line)
            y -= ITEM_LEADING
        y -= ITEM_GAP

    return y


def _draw_badge(c, x, y, text, accent):
    c.setFont(FONT_REGULAR, FINDING_CATEGORY_SIZE)
    pad_x = 8
    text_w = c.stringWidth(text, FONT_REGULAR, FINDING_CATEGORY_SIZE)
    badge_w = text_w + pad_x * 2 + FINDING_CATEGORY_TRACKING * (len(text) - 1)
    badge_h = 16

    c.saveState()
    c.setStrokeColorRGB(*accent, alpha=0.6)
    c.setLineWidth(0.8)
    c.roundRect(x, y, badge_w, badge_h, badge_h / 2, stroke=1, fill=0)
    c.restoreState()

    _draw_tracked_text(c, x + pad_x, y + badge_h / 2 - 3, text, FONT_REGULAR,
                        FINDING_CATEGORY_SIZE, accent, FINDING_CATEGORY_TRACKING)

    return badge_w


def render_diagnosis(
    c,
    company_name: str,
    strengths: list,
    attention_points: list,
    central_finding: dict,
    page_number: int = 4,
    total_pages: int | None = None,
):
    width, height = c._pagesize
    m = PAGE_MARGIN

    on_bg = _hex(THEME["onBackground"])
    muted = _hex(THEME["onSurfaceVariant"])
    primary = _hex(THEME["primary"])
    tertiary = _hex(THEME["tertiary"])
    outline = _hex(THEME["outlineVariant"])
    container = _hex(THEME["primaryContainer"])
    surface = _hex(THEME["surfaceContainer"])

    c.setFillColorRGB(*_hex(THEME["background"]))
    c.rect(0, 0, width, height, stroke=0, fill=1)

    _radial_glow(c, width * -0.06, height * 0.85, width * 0.35, primary, 0.011, steps=22)
    _radial_glow(c, width * 1.06, height * 0.15, width * 0.32, container, 0.013, steps=20)

    _draw_header(c, width, height, page_number)

    top_y = height - m - 30
    section_y = top_y - 46

    _draw_tracked_text(c, m, section_y, "DIAGNÓSTICO", FONT_REGULAR,
                        KICKER_SIZE, primary, KICKER_TRACKING)

    title_lines = [
        "O que encontramos ao observar",
        "sua empresa por fora.",
    ]
    ty = section_y - 34
    c.setFont(FONT_BOLD, SECTION_TITLE_SIZE)
    for line in title_lines:
        c.setFillColorRGB(*on_bg)
        c.drawString(m, ty, line)
        ty -= SECTION_TITLE_LEADING

    columns_top = ty - 36
    gap = 28
    col_w = (width - 2 * m - gap) / 2
    col_left_x = m
    col_right_x = m + col_w + gap

    y_left = _draw_finding_list(c, col_left_x, columns_top, col_w,
                                 "PONTOS FORTES", strengths, primary)
    y_right = _draw_finding_list(c, col_right_x, columns_top, col_w,
                                  "PONTOS DE ATENÇÃO", attention_points, tertiary)

    divider_y = min(y_left, y_right) - 18

    c.saveState()
    c.setStrokeColorRGB(*outline, alpha=0.5)
    c.setLineWidth(0.6)
    c.line(m, divider_y, width - m, divider_y)
    c.restoreState()

    finding_top = divider_y - 40
    finding_bottom = m + 60
    finding_h = finding_top - finding_bottom
    finding_w = width - 2 * m

    c.saveState()
    c.setFillColorRGB(*surface, alpha=0.4)
    c.setStrokeColorRGB(*outline, alpha=0.4)
    c.setLineWidth(0.7)
    c.roundRect(m, finding_bottom, finding_w, finding_h, 8, stroke=1, fill=1)
    c.restoreState()

    c.saveState()
    c.setStrokeColorRGB(*primary, alpha=0.85)
    c.setLineWidth(2.4)
    c.line(m, finding_bottom + 6, m, finding_bottom + finding_h - 6)
    c.restoreState()

    cube_scale = width * 0.05
    c.saveState()
    c.setFillAlpha(0.35)
    _draw_cube(c, width - m - cube_scale * 1.3, finding_bottom + cube_scale * 0.9,
               cube_scale, THEME)
    c.restoreState()

    inner_x = m + 30
    inner_w = finding_w - 60
    fy = finding_top - 26

    _draw_tracked_text(c, inner_x, fy, "ACHADO CENTRAL", FONT_REGULAR,
                        KICKER_SIZE, muted, KICKER_TRACKING)

    category = central_finding.get("category", "")
    fy -= 26
    if category:
        _draw_badge(c, inner_x, fy - 12, category, primary)
        fy -= 30

    title_text = central_finding.get("title", "")
    title_lines = _wrap(title_text, FONT_BOLD, FINDING_TITLE_SIZE, inner_w)
    c.setFont(FONT_BOLD, FINDING_TITLE_SIZE)
    for line in title_lines:
        fy -= FINDING_TITLE_LEADING
        c.setFillColorRGB(*on_bg)
        c.drawString(inner_x, fy, line)

    description = central_finding.get("description", "")
    desc_lines = _wrap(description, FONT_REGULAR, FINDING_BODY_SIZE, inner_w)
    fy -= 20
    c.setFont(FONT_REGULAR, FINDING_BODY_SIZE)
    for line in desc_lines:
        c.setFillColorRGB(*muted)
        c.drawString(inner_x, fy, line)
        fy -= FINDING_BODY_LEADING

    impact = central_finding.get("impact", "")
    if impact:
        fy -= 16
        _draw_tracked_text(c, inner_x, fy, "POR QUE ISSO IMPORTA", FONT_REGULAR,
                            LABEL_SIZE, primary, LABEL_TRACKING)
        fy -= 18
        impact_lines = _wrap(impact, FONT_REGULAR, FINDING_IMPACT_SIZE, inner_w)
        c.setFont(FONT_REGULAR, FINDING_IMPACT_SIZE)
        for line in impact_lines:
            c.setFillColorRGB(*on_bg)
            c.drawString(inner_x, fy, line)
            fy -= FINDING_IMPACT_LEADING

    _draw_footer(c, width, company_name, page_number, total_pages)

    c.showPage()