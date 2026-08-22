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

  "_pagina_insight": "A página 5 (antes fixa em 'demanda de busca') agora é genérica: serve para qualquer achado baseado em série temporal (demanda de busca, queda de acessos, variação de avaliações etc.). Os campos abaixo substituem service_name/location/trend_label/demand_highlight — o '[serviço]' e a '[cidade]' usados nas buscas de Encontrabilidade/SEO continuam sendo a fonte primária de dado, mas agora são compostos manualmente dentro do texto em vez de irem soltos como campos próprios.",

  "insight_kicker": "Rótulo curto acima do título da página (kicker), em CAIXA ALTA. Decidido manualmente conforme o tipo de achado coletado nesta seção — ex.: 'DEMANDA REAL' quando o dado vem de Google Trends/Keyword Planner sobre busca pelo serviço, ou outro rótulo (ex.: 'QUEDA DE ACESSOS') se a métrica coletada for outra. Sem ferramenta própria.",

  "insight_title": "Frase-título da página, redigida usando o '[serviço]' (mesmo termo das buscas de Encontrabilidade/SEO local) e a cidade/região da empresa, no formato padrão 'Gente está procurando por \"[serviço]\" em [cidade].' quando o insight for demanda de busca. Se o achado coletado for de outra natureza, adaptar a frase ao dado real — nunca deixar o texto genérico.",

  "insight_intro": "Texto introdutório curto abaixo do título, explicando o que o gráfico abaixo representa. Pode reaproveitar a frase padrão ('O gráfico abaixo mostra como essa procura se comportou no período analisado...') quando o insight for demanda de busca, ou ser reescrito conforme o tipo de dado coletado. Sem ferramenta própria — redação manual.",

  "trend_data": "PENDENTE DE DEFINIÇÃO: o Google Trends (trends.google.com) fornece um índice relativo de 0 a 100 por período, não volume absoluto de buscas — os valores mensais aqui devem vir desse índice relativo, não de números de busca inventados. Se usar o Google Keyword Planner (conta Google Ads sem campanha ativa) em vez do Trends, ele dá só uma estimativa única de buscas/mês (não uma série mensal) — nesse caso este campo não se aplica e o dado vai em 'insight_stat2_value'.",

  "insight_stat1_label": "Rótulo do primeiro card de estatística da página (ex.: 'TENDÊNCIA'). Substitui o antigo 'trend_label' como rótulo — decidido manualmente conforme o tipo de dado do card.",
  "insight_stat1_value": "Valor/leitura do primeiro card, obtido do mesmo gráfico do Google Trends usado em 'trend_data' (ex.: 'Crescimento de Busca Orgânica'). É leitura do gráfico, sem cálculo — corresponde ao antigo valor de 'trend_label'.",

  "insight_stat2_label": "Rótulo do segundo card de estatística (ex.: 'DEMANDA ESTIMADA'). Decidido manualmente conforme o tipo de dado coletado.",
  "insight_stat2_value": "Valor do segundo card, preenchido com dado real. Com Google Trends: 'Buscas por [serviço] na região de [cidade] vêm demonstrando [tendência]'. Com Google Keyword Planner: 'Estimativa de [X] buscas/mês por [termo] na região' (X = número exato dado pela ferramenta). Corresponde ao antigo 'demand_highlight'.",

  "interpretation": "Leitura qualitativa complementar, usando o autocomplete do Google e a seção 'as pessoas também perguntam' como sinal extra, na mesma busca feita para o Trends/Keyword Planner. Ferramenta: Google Busca.",

  "no_title": "SEM INSTRUÇÃO DE COLETA DEFINIDA. Título da Página 8 (antes fixo em '[Title]', agora campo próprio no Data). Precisa decidir se é texto institucional fixo, igual pra todo cliente, ou redigido conforme o achado principal da auditoria.",
  "no_description": "SEM INSTRUÇÃO DE COLETA DEFINIDA. Descrição da Página 8 (antes fixa em '[Description]', agora campo próprio no Data). Mesma pendência de 'no_title': decidir se é texto institucional fixo ou personalizado por cliente.",
  "no_benefits": "SEM INSTRUÇÃO DE COLETA DEFINIDA. Esse bloco (funil + achado de conversão na Página 8) não está no guia de coleta atual. Precisa decidir se é texto institucional fixo, igual ao resto da página, ou se depende de algum dado específico por empresa — e nesse caso, qual ferramenta usar.",

  "now_steps": "Achados classificados manualmente como alto impacto + baixo esforço, a partir dos resultados já coletados nas 8 métricas. Sem ferramenta nova — é triagem manual.",
  "next_steps": "Achados de impacto médio/alto + esforço médio, mesma origem, mesma triagem manual.",
  "future_steps": "Achados de impacto menor ou esforço alto, mesma origem, mesma triagem manual."
}