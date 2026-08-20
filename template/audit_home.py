from config import ADJUST_VALUE
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from .component import _hex, _draw_tracked_text, _radial_glow, _draw_cube, _glow
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
FONT_BOLD
)

_FONTS_READY = False


def _ensure_fonts():
    """Garante que as fontes usadas estão registradas.

    Usa as fontes base do ReportLab (sempre disponíveis, sem depender
    de arquivos externos). Caso o projeto queira trocar por uma fonte
    própria da marca, registre-a aqui com TTFont e atualize as
    constantes FONT_REGULAR / FONT_BOLD acima.
    """
    global _FONTS_READY
    if _FONTS_READY:
        return
    # Exemplo de como uma fonte customizada seria plugada:
    #
    # pdfmetrics.registerFont(TTFont("Inter", "assets/fonts/Inter-Regular.ttf"))
    # pdfmetrics.registerFont(TTFont("Inter-Bold", "assets/fonts/Inter-Bold.ttf"))
    #
    # Mantido com as fontes base por não haver arquivo de fonte
    # fornecido ao componente.
    _FONTS_READY = True


# ---------------------------------------------------------------------------
# Fundo: base escura + halos de luz sutis
# ---------------------------------------------------------------------------

def _draw_background(c, width, height):
    bg = _hex(THEME["background"])
    primary = _hex(THEME["primary"])
    tertiary = _hex(THEME["tertiary"])
    container = _hex(THEME["primaryContainer"])

    c.setFillColorRGB(*bg)
    c.rect(0, 0, width, height, stroke=0, fill=1)

    # Halo principal, ancorado no canto onde o cubo vai ficar. O centro
    # fica levemente fora da página para que a borda externa do brilho
    # nunca apareça como um círculo nítido.
    _radial_glow(c, width * 1.02, height * 0.24, width * 0.62, primary, 0.009, steps=36)
    _radial_glow(c, width * 0.90, height * 0.24, width * 0.22, container, 0.018, steps=24)

    # Contraluz discreta perto do título, tom azulado, para dar
    # profundidade sem competir com o texto.
    _radial_glow(c, width * -0.06, height * 0.66, width * 0.32, tertiary, 0.007, steps=28)

    # Grade técnica muito sutil, apenas na metade inferior do fundo,
    # para reforçar a leitura de "estrutura / análise".
    c.saveState()
    grid_color = _hex(THEME["outlineVariant"])
    c.setStrokeColorRGB(*grid_color, alpha=0.10)
    c.setLineWidth(0.35)
    step = 26
    top = height * 0.44
    x = 0
    while x <= width:
        c.line(x, 0, x, top)
        x += step
    c.restoreState()


# ---------------------------------------------------------------------------
# Cubo isométrico: elemento visual principal
# ---------------------------------------------------------------------------



def _draw_cube_scene(c, width, height):
    """Posiciona o cubo no quadrante direito, com halo e moldura sutil."""
    cx = width * 0.745
    cy = height * 0.235
    scale = width * 0.125

    frame_pad = scale * 1.5
    c.saveState()
    c.setStrokeColorRGB(*_hex(THEME["outlineVariant"]), alpha=0.4)
    c.setLineWidth(0.6)
    c.rect(cx - frame_pad, cy - frame_pad * 0.72, frame_pad * 2, frame_pad * 1.55,
           stroke=1, fill=0)
    c.restoreState()

    # Marcações técnicas no canto da moldura (indicador de "leitura").
    tick_x = cx - frame_pad
    tick_y = cy + frame_pad * 0.83
    c.saveState()
    c.setStrokeColorRGB(*_hex(THEME["primary"]), alpha=0.7)
    c.setLineWidth(1.1)
    c.line(tick_x, tick_y, tick_x + 14, tick_y)
    c.line(tick_x, tick_y, tick_x, tick_y - 14)
    c.restoreState()

    _draw_cube(c, cx, cy, scale + ADJUST_VALUE, THEME)


# ---------------------------------------------------------------------------
# Componente principal
# ---------------------------------------------------------------------------

def render_home(
    c:canvas.Canvas,
    name: str,
    date: str,
    logo_path: str | None = None,
):
    """Desenha a capa (Home) do relatório de Auditoria Digital na página
    atual do canvas `c`. Não chama showPage() nem save() — isso é
    responsabilidade de quem monta o PDF completo.

    Args:
        c: canvas do ReportLab (reportlab.pdfgen.canvas.Canvas)
        name: nome da empresa auditada
        date: data do relatório, já formatada como texto
        logo_path: caminho opcional para a logo em modo claro
            (ex.: PNG com transparência), usada no cabeçalho
    """
    _ensure_fonts()

    width, height = c._pagesize
    m = PAGE_MARGIN

    on_bg = _hex(THEME["onBackground"])
    muted = _hex(THEME["onSurfaceVariant"])
    primary = _hex(THEME["primary"])
    on_primary_container = _hex(THEME["onPrimaryContainer"])
    outline = _hex(THEME["outlineVariant"])

    _draw_background(c, width, height)

    # -- Cabeçalho -----------------------------------------------------
    top_y = height - m

    if logo_path:
        try:
            img = ImageReader(logo_path)
            iw, ih = img.getSize()
            logo_h = 20
            logo_w = logo_h * (iw / ih)
            c.drawImage(
                img, m, top_y - logo_h, width=logo_w, height=logo_h,
                mask="auto", preserveAspectRatio=True,
            )
        except Exception:
            _draw_tracked_text(c, m, top_y - 14, "VOIDCUBE", FONT_BOLD,
                                BRAND_SIZE, on_bg, BRAND_TRACKING)
    else:
        _draw_tracked_text(c, m, top_y - 14, "VOIDCUBE", FONT_BOLD,
                            BRAND_SIZE, on_bg, BRAND_TRACKING)

    _draw_tracked_text(c, width - m, top_y - 11, "RELATÓRIO CONFIDENCIAL",
                        FONT_REGULAR, KICKER_SIZE, muted, KICKER_TRACKING,
                        anchor="right")
    _draw_tracked_text(c, width - m, top_y - 22, "AUDITORIA DIGITAL · 2026",
                        FONT_REGULAR, KICKER_SIZE, muted, KICKER_TRACKING,
                        anchor="right")

    c.saveState()
    c.setStrokeColorRGB(*outline, alpha=0.5)
    c.setLineWidth(0.6)
    c.line(m, top_y - 34, width - m, top_y - 34)
    c.restoreState()

    # -- Kicker acima do título -----------------------------------------
    title_block_y = height * 0.60

    _draw_tracked_text(c, m, title_block_y + 46, "PRESENÇA ONLINE",
                        FONT_REGULAR, KICKER_SIZE, primary, KICKER_TRACKING)

    # -- Título -----------------------------------------------------------
    # COPY:
    # Título e subtítulo definidos pelo agente durante a implementação,
    # seguindo os princípios de copywriting descritos no briefing:
    # objetivo, com senso de autoridade, sem exageros nem clichês.
    title_lines = [
        "O que sua empresa parece,",
        "vista de fora.",
    ]

    c.setFont(FONT_BOLD, TITLE_SIZE)
    ty = title_block_y
    for line in title_lines:
        c.setFillColorRGB(*on_bg)
        c.drawString(m, ty, line)
        ty -= TITLE_LEADING

    subtitle_lines = [
        "Reunimos aqui o que encontramos ao analisar sua empresa em",
        "buscas, redes e canais digitais: pontos fortes, falhas e prioridades.",
    ]

    sy = ty - 18
    c.setFont(FONT_REGULAR, SUBTITLE_SIZE)
    for line in subtitle_lines:
        c.setFillColorRGB(*muted)
        c.drawString(m, sy, line)
        sy -= SUBTITLE_LEADING

    # -- Cubo / cena visual -------------------------------------------
    _draw_cube_scene(c, width, height)

    # -- Rodapé: empresa / data ------------------------------------------
    footer_y = m + 30

    c.saveState()
    c.setStrokeColorRGB(*outline, alpha=0.5)
    c.setLineWidth(0.6)
    c.line(m, footer_y + 26, width - m, footer_y + 26)
    c.restoreState()

    _draw_tracked_text(c, m, footer_y + 10, "EMPRESA", FONT_REGULAR,
                        LABEL_SIZE, muted, LABEL_TRACKING)
    c.setFont(FONT_BOLD, VALUE_SIZE)
    c.setFillColorRGB(*on_bg)
    c.drawString(m, footer_y - 6, name)

    date_x = width - m
    _draw_tracked_text(c, date_x, footer_y + 10, "DATA", FONT_REGULAR,
                        LABEL_SIZE, muted, LABEL_TRACKING, anchor="right")
    c.setFont(FONT_REGULAR, VALUE_SIZE)
    c.setFillColorRGB(*on_bg)
    c.drawRightString(date_x, footer_y - 6, date)

    # Pequeno indicador técnico, alinhado à direita, reforçando a
    # sensação de estrutura / documento numerado.
    _draw_tracked_text(c, date_x, m - 6, "01", FONT_REGULAR, 7.4,
                        on_primary_container, 1.4, anchor="right")
    
    c.showPage()