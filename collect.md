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