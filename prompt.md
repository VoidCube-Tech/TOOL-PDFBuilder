eu quero que me ajude a criar um json igual a esse, quando tiver informações o suficiente gere o json para mim copiar, não quero textos genericos nem com —, maximo de persuação se nao tiver informações suficiente solicite a mim:
``` JSON
{
  "name": "Empresa Exemplo Ltda",
  "audit_description": "Análise de presença digital e desempenho da marca.",
  "audit_categories": [
    {
      "name": "Presença Digital",
      "score": 80,
      "description": "Boa visibilidade nos motores de busca e redes sociais."
    },
    {
      "name": "Desempenho da Marca",
      "score": 90,
      "description": "Engajamento médio com necessidade de otimização."
    }
  ],
  "finding_category": "Otimização de SEO",
  "finding_title": "Oportunidade de Melhoria no Ranking de Busca",
  "finding_description": "Identificamos que palavras-chave estratégicas não estão sendo exploradas.",
  "finding_impact": "Perda estimada de 20% no tráfego orgânico potencial.",
  "strengths": [
    "Identidade visual consistente",
    "Bom tempo de carregamento do site"
  ],
  "attention_points": [
    "Baixa frequência de publicações",
    "Falta de integração com WhatsApp"
  ],
  "insight_kicker": "DEMANDA REAL",
  "insight_title": "Gente está procurando por \"Consultoria de SEO e Marketing\" em São Paulo, SP.",
  "insight_intro": "O gráfico abaixo mostra como essa procura se comportou no período analisado. A questão que importa é quanto dessa demanda chega até você.",
  "trend_data": [
    {
      "label": "Jan",
      "value": 1200
    },
    {
      "label": "Fev",
      "value": 1500
    },
    {
      "label": "Mar",
      "value": 2100
    }
  ],
  "insight_stat1_label": "TENDÊNCIA",
  "insight_stat1_value": "Crescimento de Busca",
  "insight_stat2_label": "DEMANDA ESTIMADA",
  "insight_stat2_value": "Alta demanda por serviços",
  "interpretation": "O mercado apresenta grande potencial não explorado no canal digital.",
  "no_title": "Sem complicação, só resultado",
  "no_description": "Você não precisa entender de tecnologia pra ter um site que funciona — a gente cuida de tudo, do jeito certo.",
  "no_benefits": [
    {
      "title": "Baixa Conversão de Leads",
      "description": "Apesar do tráfego, a taxa de conversão é inferior à média do setor.",
      "effort": "Médio",
      "impact": "Alto"
    }
  ],
  "now_steps": [
    {
      "title": "Otimização de Meta Tags",
      "description": "Ajustar títulos e descrições das páginas principais.",
      "effort": "Baixo",
      "impact": "Alto"
    }
  ],
  "next_steps": [
    {
      "title": "Produção de Conteúdo Blog",
      "description": "Criar 4 artigos mensais focados em palavras-chave do setor.",
      "effort": "Médio",
      "impact": "Alto"
    }
  ],
  "future_steps": [
    {
      "title": "Campanha de Tráfego Pago",
      "description": "Expandir alcance com anúncios no Google e Meta.",
      "effort": "Alto",
      "impact": "Médio"
    }
  ]
}
```

Seguindo essa regras:
``` MD
{
  "name": "Nome da empresa exatamente como aparece no perfil do Google Maps. Ferramenta: Google Maps.",

  "audit_description": "Frase curta escrita depois de calcular as 3 categorias macro, resumindo o resultado geral (ex.: citar a categoria com pior desempenho). Não vem de ferramenta — é redação manual a partir dos resultados já coletados.",

  "audit_categories": [
    {
      "name": "Encontrabilidade & SEO",
      "score": "Média das notas 0-10 de: Encontrabilidade (buscar '[serviço] + [cidade]' e verificar se a empresa aparece no Maps e/ou na 1ª página de busca, com dados consistentes com o WhatsApp usado na abordagem), SEO local (mesma busca, verificar posição orgânica) e Concorrência direta (levantar 3-5 concorrentes locais e comparar). Ferramentas: Google Maps, Google Busca.",
      "description": "Texto curto interpretando o resultado dessa categoria (ex.: 'boa visibilidade em buscas, mas atrás dos concorrentes'). Redigido a partir das 3 métricas acima, sem ferramenta própria."
    },
    {
      "name": "Credibilidade",
      "score": "Média das notas 0-10 de: Prova social (nota média + quantidade de avaliações no perfil), Consistência de marca (comparar nome/logo/telefone entre Maps, Instagram e site) e Atendimento/tempo de resposta (verificar se o dono responde avaliações, principalmente as negativas). Ferramentas: Google Maps (perfil da empresa), Instagram, site da empresa (se houver).",
      "description": "Texto curto interpretando o resultado dessa categoria, redigido a partir das 3 métricas acima."
    },
    {
      "name": "Conversão & Técnico",
      "score": "Média das notas 0-10 de: Canal de conversão direto (verificar WhatsApp Business com selo verde, botão de ação no Maps/Instagram, ou só telefone solto) e Qualidade técnica do site (score Mobile/Performance dividido por 10, ajustado por teste visual manual no celular; métrica N.A. se não houver site). Ferramentas: WhatsApp/Instagram/Maps (inspeção manual), Google PageSpeed Insights (pagespeed.web.dev).",
      "description": "Texto curto interpretando o resultado dessa categoria, redigido a partir das 2 métricas acima."
    }
  ],

  "finding_category": "Não é um achado livre — é sempre sobre o site. Preencher 'Presença Digital' quando a empresa não tem site, ou o nome da métrica técnica quando tem site fraco.",
  "finding_title": "Sem site: texto padrão 'Oportunidade de Criar'. Com site fraco: texto padrão 'Oportunidade de Otimizar', citando o problema específico apontado pela ferramenta.",
  "finding_description": "Sem site: frase padrão explicando a ausência de presença própria. Com site fraco: 1-2 problemas citados pelo Google PageSpeed Insights (ex.: tempo de carregamento, mobile-friendliness).",
  "finding_impact": "Sem site ou com site fraco: frase padrão sobre perda de oportunidade (tráfego, contato direto, etc.), sem número inventado — só usar percentual/estimativa se a ferramenta (PageSpeed, Trends) fornecer esse dado.",

  "strengths": "Lista das métricas (entre as 8 avaliadas) com nota alta, ex.: >= 7. Sem coleta nova — é reorganização dos resultados já obtidos com as ferramentas das categorias acima.",
  "attention_points": "Lista das métricas com nota baixa (ex.: <= 4) ou marcadas como ausentes. Mesma origem de 'strengths', sem coleta nova.",

  "service_name": "O '[serviço]' usado nas buscas das métricas Encontrabilidade e SEO local, reaproveitado aqui. Ferramenta: Google Busca.",
  "location": "Cidade/região usada nas mesmas buscas.",

  "trend_label": "Rótulo descritivo do gráfico obtido no Google Trends (ex.: 'Crescimento de Busca Orgânica'). É leitura do gráfico, sem cálculo.",
  "trend_data": "PENDENTE DE DEFINIÇÃO: o Google Trends (trends.google.com) fornece um índice relativo de 0 a 100 por período, não volume absoluto de buscas — os valores mensais aqui devem vir desse índice relativo, não de números de busca inventados. Se usar o Google Keyword Planner (conta Google Ads sem campanha ativa) em vez do Trends, ele dá só uma estimativa única de buscas/mês (não uma série mensal) — nesse caso este campo não se aplica e o dado vai em 'demand_highlight'.",

  "demand_highlight": "Frase padrão preenchida com dado real. Com Google Trends: 'Buscas por [serviço] na região de [cidade] vêm demonstrando [tendência]'. Com Google Keyword Planner: 'Estimativa de [X] buscas/mês por [termo] na região' (X = número exato dado pela ferramenta).",
  "interpretation": "Leitura qualitativa complementar, usando o autocomplete do Google e a seção 'as pessoas também perguntam' como sinal extra, na mesma busca feita para o Trends/Keyword Planner. Ferramenta: Google Busca.",

  "no_benefits": "SEM INSTRUÇÃO DE COLETA DEFINIDA. Esse bloco (funil + achado de conversão na Página 8) não está no guia de coleta atual. Precisa decidir se é texto institucional fixo, igual ao resto da página, ou se depende de algum dado específico por empresa — e nesse caso, qual ferramenta usar.",

  "now_steps": "Achados classificados manualmente como alto impacto + baixo esforço, a partir dos resultados já coletados nas 8 métricas. Sem ferramenta nova — é triagem manual.",
  "next_steps": "Achados de impacto médio/alto + esforço médio, mesma origem, mesma triagem manual.",
  "future_steps": "Achados de impacto menor ou esforço alto, mesma origem, mesma triagem manual."
}
```


Eu ja tenho essa informações:

