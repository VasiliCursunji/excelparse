import os
import django
import requests
import urllib.parse
from datetime import datetime
from bs4 import BeautifulSoup

from django.core.files.base import ContentFile

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from apps.resource.models import ResourceItem

months = {
    'Ianuarie': 1,
    'Februarie': 2,
    'Martie': 3,
    'Aprilie': 4,
    'Mai': 5,
    'Iunie': 6,
    'Iulie': 7,
    'August': 8,
    'Septembrie': 9,
    'Octombrie': 10,
    'Noiembrie': 11,
    'Decembrie': 12
}


def string_to_date(text):
    for key in months.keys():
        text = text.replace(key, str(months[key]))
    return datetime.strptime(text, '%m %d, %Y')


class GOVClient(requests.Session):
    base_url: str = 'https://date.gov.md'

    def request(self, method: str, url: str, **kwargs) -> requests.Response:
        return super(GOVClient, self).request(method, urllib.parse.urljoin(self.base_url, url), **kwargs)

    def get_dataset_11736(self) -> requests.Response:
        return self.get('ckan/ro/dataset/'
                        '11736-date-din-registrul-de-stat-al-unitatilor-de-drept-'
                        'privind-intreprinderile-inregistrate-in-repu')

    def get_dataset_11736_resource(self, resource_id) -> requests.Response:
        return self.get(f'ckan/ro/dataset/'
                        '11736-date-din-registrul-de-stat-al-unitatilor-de-drept-'
                        f'privind-intreprinderile-inregistrate-in-repu/resource/{resource_id}')


def download_files():
    client = GOVClient()

    main_response = client.get_dataset_11736()
    main_response.raise_for_status()

    main_soup = BeautifulSoup(main_response.content, features='html.parser')

    for link_soup in main_soup.select('section#dataset-resources > ul.resource-list > li.resource-item'):
        file_id = link_soup.attrs.get('data-id')

        if not ResourceItem.objects.filter(file_id=file_id).count():
            file_link = link_soup.select('a.resource-url-analytics')[0].attrs.get('href')
            file_name = link_soup.select('a.heading')[0].attrs.get('title')

            # download
            file_response = client.get(file_link)
            file_response.raise_for_status()

            # detail
            detail_response = client.get_dataset_11736_resource(file_id)
            detail_response.raise_for_status()
            detail_soup = BeautifulSoup(detail_response.content, features='html.parser')

            # data from table
            TD = [''.join(td.findAll(text=True)) for td in detail_soup.select('tbody td')]
            TH = [''.join(th.findAll(text=True)) for th in detail_soup.select('tbody th')]
            data = dict(zip(TH, TD))

            # create object
            ResourceItem.objects.create(
                hash=data['hash'],
                file_id=file_id,
                name=file_name,
                created_at=string_to_date(data['Creat']),
                updated_at=string_to_date(data['Ultima actualizare']),
                licensee=data['Licență'],
                format=data['format'],
                mimetype=data['mimetype'],
                resource_type=data['resource type'],
                resource_group_id=data['resource group id'],
                revision_id=data['revision id'],
                size=data['size'],
                state=data['state'],
                file=ContentFile(file_response.content, name=file_id + '.' + data['format'])
            )
            print(file_id, ' - downloaded')
