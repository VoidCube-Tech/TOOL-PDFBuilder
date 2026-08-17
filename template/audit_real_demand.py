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
from .audit_analysis_result import _draw_footer

SECTION_TITLE_SIZE = 22
SECTION_TITLE_LEADING = 27
BODY_SIZE = 10.6
BODY_LEADING = 16

CHART_LABEL_SIZE = 8.2
CHART_PAD_TOP = 26
CHART_PAD_BOTTOM = 22

STAT_LABEL_SIZE = 8.2
STAT_LABEL_TRACKING = 1.8
STAT_VALUE_SIZE = 15.5

INTERPRETATION_SIZE = 11
INTERPRETATION_LEADING = 16.5


def _draw_trend_chart(c, x, y, w, h, data):
    surface = _hex(THEME["surfaceContainer"])
    outline = _hex(THEME["outlineVariant"])
    primary = _hex(THEME["primary"])
    muted = _hex(THEME["onSurfaceVariant"])

    c.saveState()
    c.setFillColorRGB(*surface, alpha=0.4)
    c.setStrokeColorRGB(*outline, alpha=0.4)
    c.setLineWidth(0.7)
    c.roundRect(x, y, w, h, 8, stroke=1, fill=1)
    c.restoreState()

    values = [d["value"] for d in data]
    max_v = max(values)
    min_v = min(values)
    range_v = max(max_v - min_v, 1)

    plot_x = x + 24
    plot_w = w - 48
    plot_y = y + CHART_PAD_BOTTOM
    plot_h = h - CHART_PAD_TOP - CHART_PAD_BOTTOM

    c.saveState()
    c.setStrokeColorRGB(*outline, alpha=0.18)
    c.setLineWidth(0.5)
    for fraction in (0.33, 0.66):
        gy = plot_y + plot_h * fraction
        c.line(plot_x, gy, plot_x + plot_w, gy)
    c.restoreState()

    n = len(data)
    step = plot_w / (n - 1) if n > 1 else 0
    points = []
    for i, item in enumerate(data):
        px = plot_x + i * step
        py = plot_y + (item["value"] - min_v) / range_v * plot_h
        points.append((px, py))

    c.saveState()
    c.setFillColorRGB(*primary, alpha=0.12)
    path = c.beginPath()
    path.moveTo(points[0][0], plot_y)
    for px, py in points:
        path.lineTo(px, py)
    path.lineTo(points[-1][0], plot_y)
    path.close()
    c.drawPath(path, stroke=0, fill=1)
    c.restoreState()

    c.saveState()
    c.setStrokeColorRGB(*primary, alpha=0.9)
    c.setLineWidth(1.6)
    c.setLineJoin(1)
    c.setLineCap(1)
    path = c.beginPath()
    path.moveTo(*points[0])
    for px, py in points[1:]:
        path.lineTo(px, py)
    c.drawPath(path, stroke=1, fill=0)
    c.restoreState()

    for i, (px, py) in enumerate(points):
        is_last = i == len(points) - 1
        c.saveState()
        c.setFillColorRGB(*primary, alpha=1 if is_last else 0.6)
        c.circle(px, py, 3.2 if is_last else 2, stroke=0, fill=1)
        c.restoreState()
        if is_last:
            _radial_glow(c, px, py, 20, primary, 0.05, steps=10)

    c.setFont(FONT_REGULAR, CHART_LABEL_SIZE)
    c.setFillColorRGB(*muted)
    for i, item in enumerate(data):
        px = plot_x + i * step
        label = item.get("label", "")
        lw = stringWidth(label, FONT_REGULAR, CHART_LABEL_SIZE)
        c.drawString(px - lw / 2, y + 6, label)


def _draw_stat_card(c, x, y, w, h, label, value, accent):
    surface = _hex(THEME["surfaceContainer"])
    outline = _hex(THEME["outlineVariant"])
    on_bg = _hex(THEME["onBackground"])

    c.saveState()
    c.setFillColorRGB(*surface, alpha=0.45)
    c.setStrokeColorRGB(*outline, alpha=0.5)
    c.setLineWidth(0.7)
    c.roundRect(x, y, w, h, 7, stroke=1, fill=1)
    c.restoreState()

    pad = 16
    _draw_tracked_text(c, x + pad, y + h - pad - 4, label, FONT_REGULAR,
                        STAT_LABEL_SIZE, accent, STAT_LABEL_TRACKING)

    c.setFont(FONT_BOLD, STAT_VALUE_SIZE)
    c.setFillColorRGB(*on_bg)
    c.drawString(x + pad, y + pad + 2, value)


def render_real_demand(
    c,
    service_name: str,
    location: str,
    trend_label: str,
    trend_data: list,
    demand_highlight: str = "",
    interpretation: str = "",
    company_name: str = "",
    page_number: int = 5,
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

    c.setFillColorRGB(*_hex(THEME["background"]))
    c.rect(0, 0, width, height, stroke=0, fill=1)

    _radial_glow(c, width * 1.05, height * 0.9, width * 0.35, primary, 0.011, steps=22)
    _radial_glow(c, width * -0.05, height * 0.1, width * 0.3, container, 0.013, steps=20)

    _draw_header(c, width, height, page_number)

    top_y = height - m - 30
    section_y = top_y - 46

    _draw_tracked_text(c, m, section_y, "DEMANDA REAL", FONT_REGULAR,
                        KICKER_SIZE, primary, KICKER_TRACKING)

    title_lines = [
        f'Gente está procurando por "{service_name}"',
        f"em {location}.",
    ]
    ty = section_y - 34
    c.setFont(FONT_BOLD, SECTION_TITLE_SIZE)
    for line in title_lines:
        c.setFillColorRGB(*on_bg)
        c.drawString(m, ty, line)
        ty -= SECTION_TITLE_LEADING

    intro = (
        "O gráfico abaixo mostra como essa procura se comportou no período "
        "analisado. A questão que importa é quanto dessa demanda chega até você."
    )
    intro_lines = _wrap(intro, FONT_REGULAR, BODY_SIZE, width - 2 * m - 40)
    by = ty - 20
    c.setFont(FONT_REGULAR, BODY_SIZE)
    for line in intro_lines:
        c.setFillColorRGB(*muted)
        c.drawString(m, by, line)
        by -= BODY_LEADING

    chart_top = by - 24
    chart_h = 190
    chart_w = width - 2 * m
    chart_y = chart_top - chart_h

    _draw_trend_chart(c, m, chart_y, chart_w, chart_h, trend_data)

    cube_scale = width * 0.04
    c.saveState()
    c.setFillAlpha(0.3)
    _draw_cube(c, width - m - cube_scale, chart_top + 10, cube_scale, THEME)
    c.restoreState()

    cards_top = chart_y - 26
    card_h = 62
    card_gap = 16
    card_w = (chart_w - card_gap) / 2

    _draw_stat_card(c, m, cards_top - card_h, card_w, card_h,
                     "TENDÊNCIA", trend_label, primary)

    demand_value = demand_highlight if demand_highlight else "Sem volume estimado"
    _draw_stat_card(c, m + card_w + card_gap, cards_top - card_h, card_w, card_h,
                     "DEMANDA ESTIMADA", demand_value, tertiary)

    interp_top = cards_top - card_h - 30
    if interpretation:
        interp_lines = _wrap(interpretation, FONT_REGULAR, INTERPRETATION_SIZE,
                              chart_w - 40)
        iy = interp_top
        c.setFont(FONT_REGULAR, INTERPRETATION_SIZE)
        for line in interp_lines:
            c.setFillColorRGB(*on_bg)
            c.drawString(m, iy, line)
            iy -= INTERPRETATION_LEADING

    _draw_footer(c, width, company_name, page_number, total_pages)

    c.showPage()