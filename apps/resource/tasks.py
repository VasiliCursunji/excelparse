from celery import shared_task

from download import download_files
from parsefile import parse_docs


@shared_task(name='download_files_11736')
def download_files_11736():
    download_files()


@shared_task(name='parse_docs_11736')
def parse_docs_11736():
    parse_docs()
