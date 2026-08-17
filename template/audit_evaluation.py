from .component import _draw_tracked_text, _draw_header, _draw_footer, _wrap, _hex, _radial_glow, _draw_cube
from .theme import THEME
from .const import (
PAGE_MARGIN,
KICKER_SIZE,
KICKER_TRACKING,

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



def _draw_card(c, x, y, w, h, index_label, title, body):
    surface = _hex(THEME["surfaceContainer"])
    outline = _hex(THEME["outlineVariant"])
    primary = _hex(THEME["primary"])
    on_bg = _hex(THEME["onBackground"])
    muted = _hex(THEME["onSurfaceVariant"])

    c.saveState()
    c.setFillColorRGB(*surface, alpha=0.55)
    c.setStrokeColorRGB(*outline, alpha=0.55)
    c.setLineWidth(0.7)
    c.roundRect(x, y - h, w, h, 6, stroke=1, fill=1)
    c.restoreState()

    pad = 18
    tx = x + pad
    ty = y - pad - 6

    c.saveState()
    c.setStrokeColorRGB(*primary, alpha=0.8)
    c.setLineWidth(1.1)
    c.line(tx, ty + 4, tx + 16, ty + 4)
    c.restoreState()

    _draw_tracked_text(c, tx, ty - 12, index_label, FONT_REGULAR,
                        CARD_LABEL_SIZE, primary, CARD_LABEL_TRACKING)

    c.setFont(FONT_BOLD, CARD_TITLE_SIZE)
    c.setFillColorRGB(*on_bg)
    c.drawString(tx, ty - 32, title)

    body_lines = _wrap(body, FONT_REGULAR, CARD_BODY_SIZE, w - pad * 2)
    by = ty - 52
    c.setFont(FONT_REGULAR, CARD_BODY_SIZE)
    c.setFillColorRGB(*muted)
    for line in body_lines:
        c.drawString(tx, by, line)
        by -= CARD_BODY_LEADING


def render_evaluation(c, company_name:str, page_number: int = 2):
    width, height = c._pagesize
    m = PAGE_MARGIN

    on_bg = _hex(THEME["onBackground"])
    muted = _hex(THEME["onSurfaceVariant"])
    primary = _hex(THEME["primary"])
    outline = _hex(THEME["outlineVariant"])
    container = _hex(THEME["primaryContainer"])

    c.setFillColorRGB(*_hex(THEME["background"]))
    c.rect(0, 0, width, height, stroke=0, fill=1)

    _radial_glow(c, width * -0.05, height * 0.95, width * 0.4, primary, 0.01, steps=24)
    _radial_glow(c, width * 1.05, height * 0.1, width * 0.35, container, 0.014, steps=20)

    _draw_header(c, width, height, page_number)

    top_y = height - m - 30
    section_y = top_y - 46

    _draw_tracked_text(c, m, section_y, "COMO AVALIAMOS", FONT_REGULAR,
                        KICKER_SIZE, primary, KICKER_TRACKING)

    title_lines = [
        "Simulamos o caminho que um cliente",
        "percorre até decidir te procurar.",
    ]
    ty = section_y - 34
    c.setFont(FONT_BOLD, SECTION_TITLE_SIZE)
    for line in title_lines:
        c.setFillColorRGB(*on_bg)
        c.drawString(m, ty, line)
        ty -= SECTION_TITLE_LEADING

    body_lines = [
        "Olhamos sua empresa pelos mesmos canais que um cliente usaria: busca,",
        "mapas e comparação direta com concorrentes da mesma região. Os dados",
        "são públicos e mostram o que qualquer pessoa encontra hoje, sem exigir",
        "acesso interno ao seu negócio.",
    ]
    by = ty - 16
    c.setFont(FONT_REGULAR, SECTION_BODY_SIZE)
    for line in body_lines:
        c.setFillColorRGB(*muted)
        c.drawString(m, by, line)
        by -= SECTION_BODY_LEADING

    cards_top = by - 34
    card_gap = 16
    card_w = (width - 2 * m - 2 * card_gap) / 3
    card_h = 128

    cards = [
        ("01", "Presença",
         "Como sua empresa aparece quando alguém pesquisa pelo serviço que você oferece."),
        ("02", "Contexto",
         "Como essa aparição se compara às alternativas que a mesma pessoa também encontra na região."),
        ("03", "Decisão",
         "O quanto o que foi encontrado facilita ou atrapalha o passo seguinte, entrar em contato."),
    ]
    for i, (label, title, body) in enumerate(cards):
        cx = m + i * (card_w + card_gap)
        _draw_card(c, cx, cards_top, card_w, card_h, label, title, body)

    second_y = cards_top - card_h - 56

    c.saveState()
    c.setStrokeColorRGB(*outline, alpha=0.5)
    c.setLineWidth(0.6)
    c.line(m, second_y + 30, width - m, second_y + 30)
    c.restoreState()

    cube_scale = width * 0.05
    cube_cx = width - m - cube_scale * 1.3
    cube_cy = second_y - 46
    c.saveState()
    c.setFillAlpha(0.5)
    _draw_cube(c, cube_cx, cube_cy, cube_scale, THEME)
    c.restoreState()

    _draw_tracked_text(c, m, second_y, "POR QUE ISSO IMPORTA", FONT_REGULAR,
                        KICKER_SIZE, primary, KICKER_TRACKING)

    reason_title_lines = [
        "Presença digital não fecha venda sozinha,",
        "mas decide quem chega até ela.",
    ]
    ry = second_y - 30
    c.setFont(FONT_BOLD, SECTION_TITLE_SIZE * 0.82)
    for line in reason_title_lines:
        c.setFillColorRGB(*on_bg)
        c.drawString(m, ry, line)
        ry -= SECTION_TITLE_LEADING * 0.86

    reason_body_lines = [
        "Boa parte da confiança em um serviço se forma antes do primeiro contato.",
        "Depender só de plataformas de terceiros tira parte desse controle das",
        "suas mãos. Estar bem posicionado importa menos pelo alcance e mais",
        "por aparecer exatamente no momento em que a decisão está sendo tomada.",
    ]
    rby = ry - 14
    c.setFont(FONT_REGULAR, SECTION_BODY_SIZE)
    max_w = width - 2 * m - cube_scale * 3
    for line in reason_body_lines:
        c.setFillColorRGB(*muted)
        c.drawString(m, rby, line)
        rby -= SECTION_BODY_LEADING

    _draw_footer(c, width, company_name, page_number, total_pages=4)

    c.showPage()