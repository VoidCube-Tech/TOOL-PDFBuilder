from generate_pdf import generate_pdf
from data import Data


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
