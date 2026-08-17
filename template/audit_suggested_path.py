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
)
from .audit_evaluation import _draw_header, _wrap
from .audit_analysis_result import _draw_footer

SECTION_TITLE_SIZE = 22
SECTION_TITLE_LEADING = 27
BODY_SIZE = 10.6
BODY_LEADING = 16

RAIL_X_OFFSET = 12
CONTENT_X_OFFSET = 50

TIER_LABEL_SIZE = 9.5
TIER_LABEL_TRACKING = 2.0
TIER_DESC_SIZE = 9.6
TIER_DESC_LEADING = 13.6

ITEM_TITLE_SIZE = 11
ITEM_TITLE_LEADING = 15
ITEM_DESC_SIZE = 9.4
ITEM_DESC_LEADING = 13.2
ITEM_TAG_SIZE = 8

TIER_GAP = 30
ITEM_GAP = 0

TIERS = [
    ("now", "01", "RESOLVER AGORA",
     "Ações de impacto rápido que não deveriam esperar."),
    ("next", "02", "PRÓXIMA ETAPA",
     "Melhorias que valem entrar no planejamento."),
    ("future", "03", "SEGUNDA ETAPA",
     "Oportunidades para depois que o essencial estiver resolvido."),
]


def _tier_accent(index):
    if index == 0:
        return _hex(THEME["primary"])
    if index == 1:
        return _hex(THEME["tertiary"])
    return _hex(THEME["secondary"])


def _draw_priority_item(c, x, y_top, w, item, accent):
    surface = _hex(THEME["surfaceContainer"])
    outline = _hex(THEME["outlineVariant"])
    on_bg = _hex(THEME["onBackground"])
    muted = _hex(THEME["onSurfaceVariant"])

    pad = 14
    inner_w = w - pad * 2

    title = item.get("title", "")
    description = item.get("description", "")

    title_lines = _wrap(title, FONT_BOLD, ITEM_TITLE_SIZE, inner_w)
    desc_lines = _wrap(description, FONT_REGULAR, ITEM_DESC_SIZE, inner_w) if description else []

    tags = []
    if item.get("impact"):
        tags.append(f"Impacto {item['impact']}")
    if item.get("effort"):
        tags.append(f"Esforço {item['effort']}")

    h = pad * 2
    h += len(title_lines) * ITEM_TITLE_LEADING
    if desc_lines:
        h += 6 + len(desc_lines) * ITEM_DESC_LEADING
    if tags:
        h += 18

    c.saveState()
    c.setFillColorRGB(*surface, alpha=0.4)
    c.setStrokeColorRGB(*outline, alpha=0.4)
    c.setLineWidth(0.6)
    c.roundRect(x, y_top - h, w, h, 6, stroke=1, fill=1)
    c.restoreState()

    c.saveState()
    c.setStrokeColorRGB(*accent, alpha=0.8)
    c.setLineWidth(2)
    c.line(x, y_top - h + 6, x, y_top - 6)
    c.restoreState()

    ty = y_top - pad - ITEM_TITLE_SIZE
    c.setFont(FONT_BOLD, ITEM_TITLE_SIZE)
    for line in title_lines:
        c.setFillColorRGB(*on_bg)
        c.drawString(x + pad, ty, line)
        ty -= ITEM_TITLE_LEADING

    if desc_lines:
        ty -= 6
        c.setFont(FONT_REGULAR, ITEM_DESC_SIZE)
        for line in desc_lines:
            c.setFillColorRGB(*muted)
            c.drawString(x + pad, ty, line)
            ty -= ITEM_DESC_LEADING

    if tags:
        ty -= 4
        tag_text = "   ·   ".join(tags)
        _draw_tracked_text(c, x + pad, ty, tag_text.upper(), FONT_REGULAR,
                            ITEM_TAG_SIZE, accent, 1.0)

    return y_top - h


def _draw_tier(c, x, y_top, w, index, key, label, description, items):
    on_bg = _hex(THEME["onBackground"])
    muted = _hex(THEME["onSurfaceVariant"])
    accent = _tier_accent(index)

    rail_x = x - CONTENT_X_OFFSET + RAIL_X_OFFSET
    circle_y = y_top - 6

    c.saveState()
    c.setFillColorRGB(*_hex(THEME["background"]))
    c.setStrokeColorRGB(*accent, alpha=0.9)
    c.setLineWidth(1.2)
    c.circle(rail_x, circle_y, 12, stroke=1, fill=1)
    c.restoreState()

    number = TIERS[index][1]
    c.setFont(FONT_BOLD, 9)
    nw = c.stringWidth(number, FONT_BOLD, 9)
    c.setFillColorRGB(*accent)
    c.drawString(rail_x - nw / 2, circle_y - 3, number)

    _draw_tracked_text(c, x, y_top, label, FONT_REGULAR, TIER_LABEL_SIZE,
                        accent, TIER_LABEL_TRACKING)

    desc_lines = _wrap(description, FONT_REGULAR, TIER_DESC_SIZE, w)
    dy = y_top - 18
    c.setFont(FONT_REGULAR, TIER_DESC_SIZE)
    for line in desc_lines:
        c.setFillColorRGB(*muted)
        c.drawString(x, dy, line)
        dy -= TIER_DESC_LEADING

    items_top = dy - 10

    if not items:
        c.setFont(FONT_REGULAR, ITEM_DESC_SIZE)
        c.setFillColorRGB(*muted)
        c.drawString(x, items_top - 4, "Nenhuma ação necessária nesta etapa.")
        return items_top - 24, circle_y

    y = items_top
    for item in items:
        y = _draw_priority_item(c, x, y, w, item, accent)
        y -= ITEM_GAP

    return y, circle_y


def render_suggested_path(
    c,
    priorities: dict,
    company_name: str = "",
    page_number: int = 6,
    total_pages: int | None = None,
):
    width, height = c._pagesize
    m = PAGE_MARGIN

    on_bg = _hex(THEME["onBackground"])
    muted = _hex(THEME["onSurfaceVariant"])
    primary = _hex(THEME["primary"])
    outline = _hex(THEME["outlineVariant"])
    container = _hex(THEME["primaryContainer"])

    c.setFillColorRGB(*_hex(THEME["background"]))
    c.rect(0, 0, width, height, stroke=0, fill=1)

    _radial_glow(c, width * 1.05, height * 0.1, width * 0.35, primary, 0.011, steps=22)
    _radial_glow(c, width * -0.06, height * 0.9, width * 0.3, container, 0.013, steps=20)

    _draw_header(c, width, height, page_number)

    top_y = height - m - 30
    section_y = top_y - 46

    _draw_tracked_text(c, m, section_y, "CAMINHO SUGERIDO", FONT_REGULAR,
                        KICKER_SIZE, primary, KICKER_TRACKING)

    title_lines = [
        "O que fazer primeiro para colher",
        "resultado mais rápido.",
    ]
    ty = section_y - 34
    c.setFont(FONT_BOLD, SECTION_TITLE_SIZE)
    for line in title_lines:
        c.setFillColorRGB(*on_bg)
        c.drawString(m, ty, line)
        ty -= SECTION_TITLE_LEADING

    intro = (
        "Nem tudo precisa ser resolvido ao mesmo tempo. Organizamos os achados "
        "da auditoria em uma ordem prática, pensada para gerar retorno o quanto antes."
    )
    intro_lines = _wrap(intro, FONT_REGULAR, BODY_SIZE, width - 2 * m - 40)
    by = ty - 18
    c.setFont(FONT_REGULAR, BODY_SIZE)
    for line in intro_lines:
        c.setFillColorRGB(*muted)
        c.drawString(m, by, line)
        by -= BODY_LEADING

    content_x = m + CONTENT_X_OFFSET
    content_w = width - content_x - m

    y = by
    circles = []

    for index, (key, number, label, description) in enumerate(TIERS):
        items = priorities.get(key, [])
        y, circle_y = _draw_tier(c, content_x, y, content_w, index, key,
                                  label, description, items)
        circles.append(circle_y)
        y -= TIER_GAP

    rail_x = content_x - CONTENT_X_OFFSET + RAIL_X_OFFSET
    c.saveState()
    c.setStrokeColorRGB(*outline, alpha=0.5)
    c.setLineWidth(0.8)
    for i in range(len(circles) - 1):
        c.line(rail_x, circles[i] - 12, rail_x, circles[i + 1] + 12)
    c.restoreState()

    _draw_footer(c, width, company_name, page_number, total_pages)

    c.showPage()