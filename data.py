from datetime import datetime
from typing import TypedDict

class AUDIT_TYPE(TypedDict):
    name: str
    score: int
    description: str

class TREND_TYPE(TypedDict):
    label: str
    value: int

class STEP_TYPE(TypedDict):
    title: str
    description: str
    effort: str
    impact: str

class Data:
    def __init__(
        self, 
        name:str,
        
        audit_description:str = "",
        audit_categories: list[AUDIT_TYPE] = [],

        finding_category: str = "",
        finding_title: str = "",
        finding_description: str = "",
        finding_impact: str = "",
        strengths: list[str] = [],
        attention_points: list[str] = [],

        # Página de insight com gráfico de tendência (antes "real demand").
        # Generalizado: não é mais só sobre demanda de busca, pode ser
        # perda de acessos, queda de avaliações, qualquer série temporal
        # relevante pro diagnóstico. Quem monta o Data decide o texto.
        insight_kicker: str = "INSIGHT",
        insight_title: str = "",
        insight_intro: str = "",
        trend_data: list[TREND_TYPE] = [],
        insight_stat1_label: str = "",
        insight_stat1_value: str = "",
        insight_stat2_label: str = "",
        insight_stat2_value: str = "",
        interpretation: str = "",

        no_title: str = "",
        no_description: str = "",
        no_benefits: list[STEP_TYPE] = ["[Benefit 1]", "[Benefit 2]", "[Benefit 3]"],

        now_steps: list[STEP_TYPE] = [],
        next_steps: list[STEP_TYPE] = [],
        future_steps: list[STEP_TYPE] = [],
    ):
        self.name = name
        self.date = datetime.now().strftime("%d/%m/%Y")
        self.audit_description = audit_description
        self.audit_categories = audit_categories
        self.finding_category = finding_category
        self.finding_title = finding_title
        self.finding_description = finding_description
        self.finding_impact = finding_impact
        self.strengths = strengths
        self.attention_points = attention_points

        self.insight_kicker = insight_kicker
        self.insight_title = insight_title
        self.insight_intro = insight_intro
        self.trend_data = trend_data
        self.insight_stat1_label = insight_stat1_label
        self.insight_stat1_value = insight_stat1_value
        self.insight_stat2_label = insight_stat2_label
        self.insight_stat2_value = insight_stat2_value
        self.interpretation = interpretation

        self.now_steps = now_steps
        self.next_steps = next_steps
        self.future_steps = future_steps
        self.no_title = no_title
        self.no_description = no_description
        self.no_mockup_desktop_path = None
        self.no_mockup_mobile_path = None
        self.no_benefits = no_benefits

        self.cta_message = "O diagnóstico está pronto. A decisão é sua."
        self.cta_description = "Encontramos uma oportunidade concreta na forma como sua empresa aparece hoje. Se fizer sentido para você, podemos conversar sobre como fechar essa lacuna."
        self.cta_text = "Conversar sobre o diagnóstico"
        self.cta_note = "Sem compromisso. Só uma conversa sobre o que faz sentido para o seu negócio."
        self.cta_whatsapp = " (91) 98185-9653"