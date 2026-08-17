from reportlab.lib.utils import ImageReader

from .component import _draw_footer, _wrap, _hex, _radial_glow, _draw_header, _draw_tracked_text
from .theme import THEME
from .const import (
PAGE_MARGIN,
KICKER_SIZE,
KICKER_TRACKING,

FONT_REGULAR,
FONT_BOLD,

SECTION_TITLE_SIZE,
SECTION_TITLE_LEADING,
SECTION_BODY_SIZE,
SECTION_BODY_LEADING,

BENEFIT_TITLE_SIZE,
BENEFIT_DESC_SIZE,
BENEFIT_DESC_LEADING,

FLOW_LABEL_SIZE,
)




def _draw_device_frame(c, x, y, w, h, radius, image_path, show_dots=True):
    surface = _hex(THEME["surfaceContainerHigh"])
    outline = _hex(THEME["outlineVariant"])
    primary = _hex(THEME["primary"])
    tertiary = _hex(THEME["tertiary"])
    secondary = _hex(THEME["secondary"])

    c.saveState()
    c.setFillColorRGB(*surface, alpha=0.92)
    c.setStrokeColorRGB(*outline, alpha=0.55)
    c.setLineWidth(0.8)
    c.roundRect(x, y, w, h, radius, stroke=1, fill=1)
    c.restoreState()

    pad = 10
    content_x = x + pad
    content_w = w - pad * 2
    content_y = y + pad
    content_h = h - pad * 2

    if show_dots:
        dot_y = y + h - pad - 3
        for i, col in enumerate((primary, tertiary, secondary)):
            c.saveState()
            c.setFillColorRGB(*col, alpha=0.85)
            c.circle(content_x + i * 10, dot_y, 2.2, stroke=0, fill=1)
            c.restoreState()
        content_h -= 16

    if image_path:
        try:
            img = ImageReader(image_path)
            c.saveState()
            clip = c.beginPath()
            clip.rect(content_x, content_y, content_w, content_h)
            c.clipPath(clip, stroke=0, fill=0)
            c.drawImage(img, content_x, content_y, width=content_w, height=content_h,
                        mask="auto", preserveAspectRatio=True)
            c.restoreState()
        except Exception:
            image_path = None

    if not image_path:
        bar_color = outline
        by = content_y + content_h - 14
        widths = (0.85, 0.55, 0.7, 0.4)
        for wr in widths:
            c.saveState()
            c.setFillColorRGB(*bar_color, alpha=0.3)
            c.roundRect(content_x, by, content_w * wr, 6, 3, stroke=0, fill=1)
            c.restoreState()
            by -= 15


def _draw_flow(c, x, y, w, h):
    outline = _hex(THEME["outlineVariant"])
    primary = _hex(THEME["primary"])
    muted = _hex(THEME["onSurfaceVariant"])
    on_bg = _hex(THEME["onBackground"])

    steps = ("Procura", "Encontra você", "Chama no WhatsApp", "Você atende")
    n = len(steps)
    node_y = y + h * 0.58
    margin_x = w * 0.08
    usable_w = w - margin_x * 2
    step_gap = usable_w / (n - 1)

    c.saveState()
    c.setStrokeColorRGB(*outline, alpha=0.5)
    c.setLineWidth(0.8)
    c.line(x + margin_x, node_y, x + margin_x + usable_w, node_y)
    c.restoreState()

    for i, label in enumerate(steps):
        nx = x + margin_x + i * step_gap
        c.saveState()
        c.setFillColorRGB(*_hex(THEME["background"]))
        c.setStrokeColorRGB(*primary, alpha=0.85)
        c.setLineWidth(1.1)
        c.circle(nx, node_y, 6, stroke=1, fill=1)
        c.restoreState()
        c.saveState()
        c.setFillColorRGB(*primary, alpha=0.9)
        c.circle(nx, node_y, 2.2, stroke=0, fill=1)
        c.restoreState()

        c.setFont(FONT_REGULAR, FLOW_LABEL_SIZE)
        lw = c.stringWidth(label, FONT_REGULAR, FLOW_LABEL_SIZE)
        c.setFillColorRGB(*on_bg if i in (0, n - 1) else muted)
        c.drawString(nx - lw / 2, node_y - 20, label)


def render_no_complication(
    c,
    title: str,
    description: str,
    benefits: list,
    mockup_desktop_path: str | None = None,
    mockup_mobile_path: str | None = None,
    company_name: str = "",
    page_number: int = 7,
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

    _radial_glow(c, width * -0.05, height * 0.15, width * 0.32, primary, 0.011, steps=22)
    _radial_glow(c, width * 1.06, height * 0.85, width * 0.32, container, 0.013, steps=20)

    _draw_header(c, width, height, page_number)

    top_y = height - m - 30
    section_y = top_y - 46

    _draw_tracked_text(c, m, section_y, "SEM COMPLICAÇÃO", FONT_REGULAR,
                        KICKER_SIZE, primary, KICKER_TRACKING)

    title_lines = _wrap(title, FONT_BOLD, SECTION_TITLE_SIZE, width - 2 * m - 40)
    ty = section_y - 34
    c.setFont(FONT_BOLD, SECTION_TITLE_SIZE)
    for line in title_lines:
        c.setFillColorRGB(*on_bg)
        c.drawString(m, ty, line)
        ty -= SECTION_TITLE_LEADING

    desc_lines = _wrap(description, FONT_REGULAR, SECTION_BODY_SIZE, width - 2 * m - 60)
    by = ty - 18
    c.setFont(FONT_REGULAR, SECTION_BODY_SIZE)
    for line in desc_lines:
        c.setFillColorRGB(*muted)
        c.drawString(m, by, line)
        by -= SECTION_BODY_LEADING

    mockup_top = by - 26
    mockup_h = 200
    mockup_y = mockup_top - mockup_h

    c.saveState()
    c.setFillColorRGB(*_hex(THEME["surfaceContainerLowest"]), alpha=0.35)
    c.setStrokeColorRGB(*outline, alpha=0.3)
    c.setLineWidth(0.6)
    c.roundRect(m, mockup_y, width - 2 * m, mockup_h, 10, stroke=1, fill=1)
    c.restoreState()

    if mockup_desktop_path or mockup_mobile_path:
        desktop_w = (width - 2 * m) * 0.58
        desktop_h = mockup_h * 0.72
        desktop_x = m + (width - 2 * m) * 0.08
        desktop_y = mockup_y + mockup_h - desktop_h - 24

        _radial_glow(c, desktop_x + desktop_w / 2, desktop_y + desktop_h / 2,
                     desktop_w * 0.55, primary, 0.02, steps=16)
        _draw_device_frame(c, desktop_x, desktop_y, desktop_w, desktop_h, 10,
                            mockup_desktop_path)

        mobile_w = desktop_w * 0.34
        mobile_h = mockup_h * 0.82
        mobile_x = desktop_x + desktop_w - mobile_w * 0.45
        mobile_y = mockup_y + 16

        _draw_device_frame(c, mobile_x, mobile_y, mobile_w, mobile_h, 16,
                            mockup_mobile_path, show_dots=False)
    else:
        _draw_flow(c, m + 20, mockup_y, width - 2 * m - 40, mockup_h)

    benefits_top = mockup_y - 36
    n = max(len(benefits), 1)
    col_gap = 24
    col_w = (width - 2 * m - col_gap * (n - 1)) / n

    for i, benefit in enumerate(benefits):
        bx = m + i * (col_w + col_gap)
        c.saveState()
        c.setStrokeColorRGB(*primary, alpha=0.8)
        c.setLineWidth(1.4)
        c.line(bx, benefits_top, bx + 20, benefits_top)
        c.restoreState()

        title_text = benefit.get("title", "")
        body_text = benefit.get("description", "")

        c.setFont(FONT_BOLD, BENEFIT_TITLE_SIZE)
        c.setFillColorRGB(*on_bg)
        c.drawString(bx, benefits_top - 22, title_text)

        body_lines = _wrap(body_text, FONT_REGULAR, BENEFIT_DESC_SIZE, col_w)
        yy = benefits_top - 40
        c.setFont(FONT_REGULAR, BENEFIT_DESC_SIZE)
        for line in body_lines:
            c.setFillColorRGB(*muted)
            c.drawString(bx, yy, line)
            yy -= BENEFIT_DESC_LEADING

    _draw_footer(c, width, company_name, page_number, total_pages)

    c.showPage()