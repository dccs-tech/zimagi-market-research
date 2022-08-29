from systems.commands.index import Command

from utility.browser import Browser

import re


class Test(Command('business.test')):

    def exec(self):
        self.load_companies('tech/django-companies')


    def load_companies(self, focus):

        def load_page(page_number):
            has_companies = False

            base_url = "https://builtin.com/companies/{}".format(focus)
            url      = "{}?page={}".format(base_url, page_number) if page_number > 1 else base_url

            self.notice("Loading companies: {}".format(url))
            browser = Browser(url)

            for element in browser.get_classes('company-card-col'):
                self.load_company(
                    element.get_css('h2.company-name a').text,
                    element.get_css('h2.company-name a').attr('href')
                )
                has_companies = True

            if has_companies:
                load_page(page_number + 1)

        load_page(1)


    def load_company(self, name, url):
        browser = Browser(url)

        # Fields
        #--------------------
        # name
        # built_in_url
        # url
        # tagline
        # description
        # location (city, state)
        # employees
        # year founded
        # industries
        # jobs
        # technologies

        self.data(name, url)
        self.info(browser.get_css('a.company-website-link').attr('href'))
        self.info(browser.get_css('p.tagline').text)
        self.info(browser.get_css('p.full-description').text)

        location = [ element.strip() for element in browser.get_css('p.main-location').text.split(",") ]
        self.notice(location[0])
        self.notice(location[1])

        self.info(re.sub(r'[^\d]+', '', browser.get_css('div.employees span.value').text))
        self.info(browser.get_css('div.founded span.value').text)

        self.notice('Industries')
        for element in browser.get_css_list('li.industry'):
            industry = re.sub(r'\s+', '-', element.text.lower())
            self.info(industry)

        self.notice('Jobs')
        for element in browser.get_css_list('button.expertise-filter'):
            job_category = re.sub(r'\s+', '', element.get_css('div.job-category').text.removesuffix('Jobs'))
            job_count = element.get_css('div.job-count').text
            self.info(job_category)
            self.info(job_count)

        self.notice('Technologies')
        for element in browser.get_css_list('li.technology'):
            technology_name = element.get_css('div.name').text
            technology_type = element.get_css('div.sub-type').text.lower()
            self.info(technology_name)
            self.info(technology_type)

