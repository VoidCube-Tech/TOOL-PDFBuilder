from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from template.audit_home import render_home
from template.audit_evaluation import render_evaluation
from template.audit_analysis_result import render_analysis_result
from template.audit_diagnosis import render_diagnosis
from template.audit_real_demand import render_real_demand
from template.audit_suggested_path import render_suggested_path
from template.audit_next_step import render_next_step 
from template.audit_no_complication import render_no_complication
from data import Data


def generate_pdf(
    data: Data
):
    c = canvas.Canvas(
        "auditoria.pdf",
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

    render_real_demand(
        c,
        company_name=data.name,
        service_name=data.service_name,
        location=data.location,
        trend_label=data.trend_label,
        trend_data=data.trend_data,
        demand_highlight=data.demand_highlight,
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


if __name__ == "__main__":
    data = Data(
        name="Nasdaq",
        audit_description= "A empresa apresenta um bom desempenho em termos de segurança cibernética",
        audit_categories=[
            {
                "name": "Segurança de Rede",
                "score": 90,
                "description": "A empresa implementou medidas robustas de segurança de rede, incluindo firewalls e sistemas de detecção de intrusões."
            },
            {
                "name": "Proteção de Dados",
                "score": 80,
                "description": "A empresa possui políticas de proteção de dados eficazes, garantindo a confidencialidade e integridade das informações."
            },
            {
                "name": "Conformidade Regulatória",
                "score": 75,
                "description": "A empresa está em conformidade com as regulamentações relevantes, mas há espaço para melhorias em algumas áreas."
            }
        ],
        finding_category= "Segurança de Rede",
        finding_title= "Vulnerabilidade em Firewall",
        finding_description= "Foi identificada uma vulnerabilidade crítica no firewall da empresa, que pode permitir acesso não autorizado à rede interna.",
        finding_impact= "Se explorada, essa vulnerabilidade pode resultar em perda de dados sensíveis e comprometimento da infraestrutura de TI.",
        strengths= [
            "Implementação de firewalls robustos",
            "Políticas de proteção de dados eficazes",
            "Conformidade com regulamentações relevantes"
        ],
        attention_points= [
            "Vulnerabilidade crítica no firewall",
            "Necessidade de atualização de sistemas de detecção de intrusões",
            "Revisão das políticas de segurança cibernética"
        ],
        service_name= "consultoria de segurança cibernética",
        location= "São Paulo",
        trend_label= "Tendência de busca",
        trend_data=[
            {"label": "Jan", "value": 120},
            {"label": "Feb", "value": 150},
            {"label": "Mar", "value": 180},
            {"label": "Apr", "value": 200},
            {"label": "May", "value": 220},
            {"label": "Jun", "value": 250}
        ],
        demand_highlight= "Alta demanda",
        interpretation= "A crescente demanda por serviços de segurança cibernética indica que as empresas estão cada vez mais conscientes da importância de proteger seus ativos digitais e estão buscando soluções especializadas para mitigar riscos e ameaças cibernéticas.",

        now_steps= [
            {
                "title": "Realizar uma auditoria completa da infraestrutura de TI",
                "description": "Auditoria detalhada da infraestrutura de TI para identificar pontos fracos e oportunidades de melhoria.",
                "effort": "Alto",
                "impact": "Alto"
            }
        ],
        next_steps= [
            {
                "title": "Revisar e atualizar as políticas de segurança cibernética",
                "description": "Revisão e atualização das políticas de segurança cibernética para garantir que estejam alinhadas com as melhores práticas e regulamentações.",
                "effort": "Médio",
                "impact": "Alto"
            }
        ],
        future_steps= [
            {
                "title": "Investir em soluções avançadas de detecção de ameaças",
                "description": "Investimento em tecnologias de detecção de ameaças para identificar e mitigar riscos de forma mais eficaz.",
                "effort": "Alto",
                "impact": "Alto"
            }
        ],

        no_benefits= [ 
            {
                "title": "[Benefit 1]",
                "description": "[Description 1]",
                "effort": "Alto",
                "impact": "Alto"
            },
            {
                "title": "[Benefit 2]",
                "description": "[Description 2]",
                "effort": "Médio",
                "impact": "Alto"
            },
            {
                "title": "[Benefit 3]",
                "description": "[Description 3]",
                "effort": "Baixo",
                "impact": "Médio"
            }
        ]
    )
    generate_pdf(data)