import scrapy
import json

class VagasSpider(scrapy.Spider):
    name = 'vagas'
    start_urls = ['https://www.catho.com.br/vagas/_next/data/3-dur8K5dZVecdIz78S0t/analista-de-dados.json?page=1&slug=analista-de-dados',
                  'https://www.catho.com.br/vagas/_next/data/3-dur8K5dZVecdIz78S0t/cientista-de-dados.json?page=1&slug=cientista-de-dados',
                  'https://www.catho.com.br/vagas/_next/data/3-dur8K5dZVecdIz78S0t/data-analyst.json?page=1&slug=data-analyst',
                  'https://www.catho.com.br/vagas/_next/data/3-dur8K5dZVecdIz78S0t/data-engineering.json?page=1&slug=data-engineering',
                  'https://www.catho.com.br/vagas/_next/data/3-dur8K5dZVecdIz78S0t/engenheiro-de-dados.json?page=1&slug=engenheiro-de-dados',
    ]

    def parse(self, response):
        cargo = response.url.split('slug=')[-1].replace('-', ' ').title()
        data = json.loads(response.text)  # Carregue o JSON da resposta
        jobs = data['pageProps']['jobSearch']['jobSearchResult']['data']['jobs']
        total_pages = data['pageProps']['pageState']['props']['totalPages']

        # Itera sobre as vagas no JSON
        for job in jobs:
            yield {
                'cargo buscado': cargo,
                'vaga': job['job_customized_data']['titulo'],
                'empresa': job['job_customized_data']['contratante']['nome'],
                'salario': job['job_customized_data']['faixaSalarial'],
                'cidade': job['job_customized_data']['vagas'][0]['cidade'],
                'estado': job['job_customized_data']['vagas'][0]['uf'],
                'data de atualizacao': job['job_customized_data']['dataAtualizacao'],
            }

        # Se houver próxima página, continue
        current_page = data['pageProps']['jobSearch']['queryParams']['page']
        next_page = current_page + 1 
        if next_page <= total_pages:
            next_url = response.url.replace(f'page={current_page}', f'page={next_page}')
            yield scrapy.Request(next_url, callback=self.parse)