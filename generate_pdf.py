from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from template.audit_home import render_home
from template.audit_evaluation import render_evaluation
from template.audit_analysis_result import render_analysis_result
from template.audit_diagnosis import render_diagnosis
from template.audit_real_demand import render_insight_trend
from template.audit_suggested_path import render_suggested_path
from template.audit_next_step import render_next_step
from template.audit_no_complication import render_no_complication
from data import Data


def generate_pdf(
    data: Data,
    output_filename: str = "auditoria.pdf"
):
    c = canvas.Canvas(
        output_filename,
        pagesize=A4,
    )

    render_home(
        c,
        name=data.name,
        date=data.date,
    )

    render_evaluation(
        c,
        company_name=data.name,
    )

    render_analysis_result(c,
        company_name= data.name,
        score_description= data.audit_description,
        categories= data.audit_categories
    )

    render_diagnosis(c,
        company_name=data.name,
        central_finding= {
            "category": data.finding_category,
            "title": data.finding_title,
            "description": data.finding_description,
            "impact": data.finding_impact
        },
        strengths= data.strengths,
        attention_points= data.attention_points
    )

    render_insight_trend(
        c,
        company_name=data.name,
        kicker=data.insight_kicker,
        title=data.insight_title,
        intro=data.insight_intro,
        trend_data=data.trend_data,
        stat1_label=data.insight_stat1_label,
        stat1_value=data.insight_stat1_value,
        stat2_label=data.insight_stat2_label,
        stat2_value=data.insight_stat2_value,
        interpretation=data.interpretation
    )

    render_suggested_path(
        c,
        company_name=data.name,
        priorities={
            "now": data.now_steps,
            "next": data.next_steps,
            "future": data.future_steps
        }
    )

    render_no_complication(
        c,
        title=data.no_title,
        description=data.no_description,
        benefits=data.no_benefits,
        mockup_desktop_path=data.no_mockup_desktop_path,
        mockup_mobile_path=data.no_mockup_mobile_path,
        company_name=data.name
    )

    render_next_step(
        c,
        company_name=data.name,
        message=data.cta_message,
        description=data.cta_description,
        cta_text=data.cta_text,
        cta_note=data.cta_note,
        whatsapp=data.cta_whatsapp
    )

    c.save()