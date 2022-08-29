from systems.plugins.index import BaseProvider
from utility.browser import Browser
from utility.data import get_identifier

import re


class Provider(BaseProvider('source', 'built_in')):

    def item_columns(self):
        return {
            'industry': [
                'name'
            ],
            'technology': [
                'name',
                'type'
            ],
            'business': [
                'name',
                'built_in_url',
                'company_url',
                'tagline',
                'description',
                'location_id',
                'city',
                'state',
                'employees',
                'year_founded',
                'industries',
                'technologies'
            ],
            'job_category': [
                'business',
                'name',
                'count'
            ]
        }


    def load_items(self, context):

        def load_business(name, url):
            browser = Browser(url)
            business = {
                'name': name,
                'built_in_url': url,
                'company_url': browser.get_css('a.company-website-link').attr('href'),
                'tagline': browser.get_css('p.tagline').text,
                'description': browser.get_css('p.full-description').text
            }

            employees = re.sub(r'[^\d]+', '', browser.get_css('div.employees span.value').text)
            business['employees'] = int(employees) if employees else None

            year_founded = browser.get_css('div.founded span.value').text
            business['year_founded'] = int(year_founded) if year_founded else None

            location = [
                element.strip() for element in browser.get_css('p.main-location').text.split(",")
            ]
            if len(location) == 2:
                business['city'] = location[0]
                business['state'] = location[1]
                business['location_id'] = get_identifier(location)
            else:
                business['city'] = None
                business['state'] = None
                business['location_id'] = None

            industries = []
            for element in browser.get_css_list('li.industry'):
                industry = re.sub(r'\s+', '-', element.text.lower())
                industries.append(industry)
            business['industries'] = industries

            job_categories = {}
            for element in browser.get_css_list('button.expertise-filter'):
                job_category = re.sub(r'\s+', '', element.get_css('div.job-category').text.removesuffix('Jobs'))
                job_count = re.sub(r'[^\d]+', '', element.get_css('div.job-count').text)
                job_categories[job_category] = int(job_count) if job_count else None
            business['job_categories'] = job_categories

            technologies = {}
            for element in browser.get_css_list('li.technology'):
                technology_name = element.get_css('div.name').text
                technology_type = element.get_css('div.sub-type').text.lower()
                technologies[technology_name] = technology_type
            business['technologies'] = technologies

            return business

        page_state_id = "{}-{}-page".format(self.state_id, self.field_focus)
        page          = self.command.get_state(page_state_id, 1)

        while True:
            has_companies = False
            base_url = "https://builtin.com/companies/{}".format(self.field_focus)
            url      = "{}?page={}".format(base_url, page) if page > 1 else base_url

            self.command.notice("Loading companies: {}".format(url))
            browser = Browser(url)

            for element in browser.get_classes('company-card-col'):
                business = load_business(
                    element.get_css('h2.company-name a').text,
                    element.get_css('h2.company-name a').attr('href')
                )
                has_companies = True
                yield business

            page += 1
            self.command.set_state(page_state_id, page)

            if not has_companies:
                self.command.delete_state(page_state_id)
                break


    def load_item(self, business, context):
        industries = []
        for name in business.get('industries', []):
            industries.append([ name ])

        technologies = []
        technology_names = []
        for name, type in business.pop('technologies', {}).items():
            technology_names.append(name)
            technologies.append([ name, type ])
        business['technologies'] = technology_names

        job_categories = []
        for name, count in business.pop('job_categories', {}).items():
            job_categories.append([
                business['name'],
                name,
                count
            ])

        business_fields = []
        for field in self.item_columns()['business']:
            business_fields.append(business[field])

        return {
            'industry': industries,
            'technology': technologies,
            'business': [ business_fields ],
            'job_category': job_categories
        }
