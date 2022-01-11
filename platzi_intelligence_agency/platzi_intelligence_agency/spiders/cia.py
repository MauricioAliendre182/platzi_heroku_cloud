import scrapy

# Expresiones de XPATH que vamos usando
# Links =  '//a[starts-with(@href, "collection") and (parent::h3|parent::h2)]/@href'
# Title = '//h1[@class = "documentFirstHeading"]/text()'
# Paragraph = '//div[contains(@class, "field-item")]/p[not(child::strong and child::i) and not(@class)]/text()'
# Imagen = '//div[@class="field-item even"]//a[not(@class) and @target="_blank"]/img/@src'

# Creamos la clase principal


class SpiderCIA(scrapy.Spider):
    # Referencia unica al Spider
    name = 'cia'

    # URLs de trabajo
    start_urls = [
        'https://www.cia.gov/readingroom/historical-collections'
    ]

    # Definimos los Customs Settings
    # custom_settings = {
    #     'FEED_URI': 'cia.json',
    #     'FEED_FORMAT': 'json',
    #     'FEED_EXPORT_ENCODING': 'utf-8'
    # }

    custom_settings = {
        'FEEDS': {
            'cia.json': {
                'format': 'json',
                'encoding': 'utf8',
                'store_empty': False,
                'fields': None,
                'indent': 4,
                'overwrite': True,
                'item_export_kwargs': {
                    'export_empty_fields': True,
                },
            },
        },
        # Colocar otras configuraciones interesante
        # Con esto le decimos a scrappy que realice 24 peticiones a la vez
        # debido a quees un Framework assincrono
        'CONCURRENT_REQUEST': 24,
        # Cantidad de memoria RAM que le permitimos usar a Scrappy
        # Esto para no sobrecargar la computadora
        'MEMUSAGE_LIMIT_MB': 2048,
        # Este atributo tiene una lista con Emails a los que scrappy va avisar si la memoria
        # RAM llega a pasarse del limite
        'MEMUSAGE_NOTIFY_MAIL': ['maps.3167@gmail.com'],
        # Decirle si va a obedecer al archivo ROBOTS.TXT
        'ROBOTSTXT_OBEY': True,
        # Puedo enviar el User_agent, aqui se indica al sitio web quienes somos nosotros
        # generalmente sale el navegador, como GOOGLE CHROME
        'USER_AGENT': 'Maps182',
        # Cambiar el encoding
        # 'FEED_EXPORT_ENCODING': 'utf-8'

    }

    # Creamos el metodo fundamental
    def parse(self, response):
        links_declassified = response.xpath(
            '//a[starts-with(@href, "collection") and (parent::h3|parent::h2)]/@href').getall()
        # Empezamos a recorrer esta lista de links
        for link in links_declassified:
            # response.urljoin(link): une cada uno de los links con la URL principal de la pagina de la CIA
            yield response.follow(link, callback=self.parse_link, cb_kwargs={'url': response.urljoin(link)})

    def parse_link(self, response, **kwargs):
        link = kwargs['url']
        title = response.xpath(
            '//h1[@class = "documentFirstHeading"]/text()').get()
        paragraph = ''.join(response.xpath(
            '//div[contains(@class, "field-item")]/p[not(child::strong and child::i) and not(@class)]/text()').getall())
        image = response.xpath(
            '//div[@class="field-item even"]//a[not(@class) and @target="_blank"]/img/@src').get()
        if image != None:
            yield {
                'url': link,
                'logo': 'https://www.cia.gov' + image,
                'title': title,
                'body': paragraph,
            }
        else:
            yield {
                'url': link,
                'logo': 'https://image.shutterstock.com/image-photo/london-uk-march-18th-2018-600w-1051373186.jpg',
                'title': title,
                'body': paragraph,
            }
