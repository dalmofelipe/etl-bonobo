import bonobo

from bonobo.config import use_context_processor

import requests


COMMENTS_API_URL = 'https://jsonplaceholder.typicode.com/comments'


def extract_comments():
    yield from requests.get(COMMENTS_API_URL).json()
    # .get('records')


"""
def with_open_file(self, context):
    with open('output.txt', 'w+') as f:
        yield f
"""

def with_opened_file(self, context):
    with context.get_service('fs').open('outputs/output.txt', 'w+') as f:
        yield f


@use_context_processor(with_opened_file)
def write_repr_to_file(f, *row):
    """
    f = é o yield do decorator filesystem service

    *row = recebe o yiel do transformation extract_comments()
    """
    f.write(repr(row) + '\n')


def get_graph(**options):
    graph = bonobo.Graph()
    graph.add_chain(
        extract_comments, 
        bonobo.Limit(10),
        bonobo.CsvWriter('outputs/output.csv')
        # write_repr_to_file
    )
    return graph


def get_services(**options):
    """
    pip install fs-s3fs

    You must provide a bucket for which you have the write permission, and it’s up to you to setup your amazon credentials in such a way that boto can access your AWS account.
    """
    return {
        # 'fs': bonobo.open_fs('s3://bonobo-examples')
    }


if __name__ == '__main__':
    parser = bonobo.get_argument_parser()
    with bonobo.parse_args(parser) as options:
        bonobo.run(
            get_graph(**options), 
            services=get_services(**options)
        )
