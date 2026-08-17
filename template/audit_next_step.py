from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth

from .component import _draw_footer, _wrap, _hex, _radial_glow, _draw_header, _draw_tracked_text, _draw_cube
from .theme import THEME
from .const import (
PAGE_MARGIN,
KICKER_SIZE,
KICKER_TRACKING,

BRAND_SIZE,
BRAND_TRACKING,

FONT_REGULAR,
FONT_BOLD,

SECTION_TITLE_SIZE,
SECTION_TITLE_LEADING,
SECTION_BODY_SIZE,
SECTION_BODY_LEADING,

CTA_TEXT_SIZE,
CTA_NOTE_SIZE,

CONTACT_LABEL_SIZE,
CONTACT_LABEL_TRACKING,
CONTACT_VALUE_SIZE,

TAGLINE_SIZE
)


def _measure_contact_block(label, value):
    lw = stringWidth(label.upper(), FONT_REGULAR, CONTACT_LABEL_SIZE) + \
        CONTACT_LABEL_TRACKING * max(len(label) - 1, 0)
    vw = stringWidth(value, FONT_REGULAR, CONTACT_VALUE_SIZE)
    return max(lw, vw)


def _draw_contacts_row(c, center_x, y, contacts):
    on_bg = _hex(THEME["onBackground"])
    muted = _hex(THEME["onSurfaceVariant"])
    primary = _hex(THEME["primary"])

    gap = 34
    widths = [_measure_contact_block(label, value) for label, value, _ in contacts]
    total_w = sum(widths) + gap * max(len(contacts) - 1, 0)
    x = center_x - total_w / 2

    for (label, value, emphasized), w in zip(contacts, widths):
        accent = primary if emphasized else muted
        _draw_tracked_text(c, x, y, label.upper(), FONT_REGULAR,
                            CONTACT_LABEL_SIZE, accent, CONTACT_LABEL_TRACKING)
        c.setFont(FONT_REGULAR, CONTACT_VALUE_SIZE)
        c.setFillColorRGB(*on_bg)
        c.drawString(x, y - 15, value)
        x += w + gap


def render_next_step(
    c,
    company_name: str,
    message: str,
    description: str,
    cta_text: str,
    cta_note: str = "",
    whatsapp: str | None = None,
    instagram: str | None = None,
    website: str | None = None,
    email: str | None = None,
    logo_path: str | None = None,
    qr_code_path: str | None = None,
    tagline: str = "Presença digital que trabalha por você.",
    page_number: int = 8,
    total_pages: int | None = None,
):
    width, height = c._pagesize
    m = PAGE_MARGIN
    center_x = width / 2

    on_bg = _hex(THEME["onBackground"])
    muted = _hex(THEME["onSurfaceVariant"])
    primary = _hex(THEME["primary"])
    outline = _hex(THEME["outlineVariant"])
    container = _hex(THEME["primaryContainer"])
    on_primary_container = _hex(THEME["onPrimaryContainer"])
    surface = _hex(THEME["surfaceContainer"])

    c.setFillColorRGB(*_hex(THEME["background"]))
    c.rect(0, 0, width, height, stroke=0, fill=1)

    _radial_glow(c, center_x, height * 0.42, width * 0.75, primary, 0.009, steps=32)
    _radial_glow(c, center_x, height * 0.42, width * 0.32, container, 0.02, steps=22)

    cube_scale = width * 0.16
    c.saveState()
    c.setFillAlpha(0.22)
    _draw_cube(c, center_x, height * 0.44, cube_scale, THEME)
    c.restoreState()

    _draw_header(c, width, height, page_number)

    top_y = height - m - 30
    section_y = top_y - 60

    kicker_text = "PRÓXIMO PASSO"
    kicker_w = stringWidth(kicker_text, FONT_REGULAR, KICKER_SIZE) + \
        KICKER_TRACKING * (len(kicker_text) - 1)
    _draw_tracked_text(c, center_x - kicker_w / 2, section_y, kicker_text,
                        FONT_REGULAR, KICKER_SIZE, primary, KICKER_TRACKING)

    title_lines = _wrap(message, FONT_BOLD, SECTION_TITLE_SIZE, width - 2 * m - 80)
    ty = section_y - 34
    c.setFont(FONT_BOLD, SECTION_TITLE_SIZE)
    for line in title_lines:
        lw = stringWidth(line, FONT_BOLD, SECTION_TITLE_SIZE)
        c.setFillColorRGB(*on_bg)
        c.drawString(center_x - lw / 2, ty, line)
        ty -= SECTION_TITLE_LEADING

    desc_lines = _wrap(description, FONT_REGULAR, SECTION_BODY_SIZE, width - 2 * m - 140)
    by = ty - 18
    c.setFont(FONT_REGULAR, SECTION_BODY_SIZE)
    for line in desc_lines:
        lw = stringWidth(line, FONT_REGULAR, SECTION_BODY_SIZE)
        c.setFillColorRGB(*muted)
        c.drawString(center_x - lw / 2, by, line)
        by -= SECTION_BODY_LEADING

    cta_top = by - 34
    cta_w = min(width - 2 * m, 360)
    cta_h = 64
    cta_x = center_x - cta_w / 2
    cta_y = cta_top - cta_h

    _radial_glow(c, center_x, cta_y + cta_h / 2, cta_w * 0.75, primary, 0.03, steps=18)

    c.saveState()
    c.setFillColorRGB(*container, alpha=0.85)
    c.setStrokeColorRGB(*primary, alpha=0.75)
    c.setLineWidth(1)
    c.roundRect(cta_x, cta_y, cta_w, cta_h, cta_h / 2, stroke=1, fill=1)
    c.restoreState()

    c.setFont(FONT_BOLD, CTA_TEXT_SIZE)
    cta_w_text = stringWidth(cta_text, FONT_BOLD, CTA_TEXT_SIZE)
    c.setFillColorRGB(*on_primary_container)
    c.drawString(center_x - cta_w_text / 2, cta_y + cta_h / 2 - 5, cta_text)

    note_y = cta_y - 22
    if cta_note:
        note_lines = _wrap(cta_note, FONT_REGULAR, CTA_NOTE_SIZE, width - 2 * m - 160)
        ny = note_y
        c.setFont(FONT_REGULAR, CTA_NOTE_SIZE)
        for line in note_lines:
            lw = stringWidth(line, FONT_REGULAR, CTA_NOTE_SIZE)
            c.setFillColorRGB(*muted)
            c.drawString(center_x - lw / 2, ny, line)
            ny -= CTA_NOTE_SIZE + 4
        note_y = ny

    if qr_code_path:
        try:
            qr_img = ImageReader(qr_code_path)
            qr_size = 66
            qr_x = center_x - qr_size / 2
            qr_y = note_y - qr_size - 12
            c.saveState()
            c.setFillColorRGB(*surface, alpha=0.6)
            c.setStrokeColorRGB(*outline, alpha=0.5)
            c.setLineWidth(0.7)
            c.roundRect(qr_x - 8, qr_y - 8, qr_size + 16, qr_size + 16, 8, stroke=1, fill=1)
            c.drawImage(qr_img, qr_x, qr_y, width=qr_size, height=qr_size, mask="auto")
            c.restoreState()
            note_y = qr_y - 20
        except Exception:
            pass

    contacts = []
    if whatsapp:
        contacts.append(("WhatsApp", whatsapp, True))
    if instagram:
        contacts.append(("Instagram", instagram, False))
    if website:
        contacts.append(("Site", website, False))
    if email:
        contacts.append(("E-mail", email, False))

    contacts_y = note_y - 26
    if contacts:
        _draw_contacts_row(c, center_x, contacts_y, contacts)
        divider_y = contacts_y - 40
    else:
        divider_y = note_y - 20

    c.saveState()
    c.setStrokeColorRGB(*outline, alpha=0.4)
    c.setLineWidth(0.6)
    c.line(center_x - 60, divider_y, center_x + 60, divider_y)
    c.restoreState()

    brand_y = divider_y - 34

    if logo_path:
        try:
            logo_img = ImageReader(logo_path)
            iw, ih = logo_img.getSize()
            logo_h = 26
            logo_w = logo_h * (iw / ih)
            c.drawImage(logo_img, center_x - logo_w / 2, brand_y - logo_h,
                        width=logo_w, height=logo_h, mask="auto",
                        preserveAspectRatio=True)
            brand_y -= logo_h + 10
        except Exception:
            brand_w = stringWidth("VOIDCUBE", FONT_BOLD, BRAND_SIZE) + \
                BRAND_TRACKING * (len("VOIDCUBE") - 1)
            _draw_tracked_text(c, center_x - brand_w / 2, brand_y - 14, "VOIDCUBE",
                                FONT_BOLD, BRAND_SIZE, on_bg, BRAND_TRACKING)
            brand_y -= 24
    else:
        brand_w = stringWidth("VOIDCUBE", FONT_BOLD, BRAND_SIZE) + \
            BRAND_TRACKING * (len("VOIDCUBE") - 1)
        _draw_tracked_text(c, center_x - brand_w / 2, brand_y - 14, "VOIDCUBE",
                            FONT_BOLD, BRAND_SIZE, on_bg, BRAND_TRACKING)
        brand_y -= 24

    if tagline:
        c.setFont(FONT_REGULAR, TAGLINE_SIZE)
        tw = stringWidth(tagline, FONT_REGULAR, TAGLINE_SIZE)
        c.setFillColorRGB(*muted)
        c.drawString(center_x - tw / 2, brand_y - 6, tagline)

    _draw_footer(c, width, company_name, page_number, total_pages)