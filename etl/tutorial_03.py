import bonobo

from bonobo.config import use_context_processor, use


COMMENTS_API_URL = 'https://jsonplaceholder.typicode.com/comments'


@use('http')
def extract_comments(http):
    yield from http.get(COMMENTS_API_URL).json()


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
        bonobo.CsvWriter('outputs/output_tutorial_03.csv')
    )
    return graph


def get_services(use_cache=False, **options):
    """
    pip install requests-cache

    habilitando cache nas consultas a apis externas
    """
    # service override 
    http = None
    if use_cache:
        from requests_cache import CachedSession
        http = CachedSession('http.cache')
    else:
        import requests
        http = requests.Session()
    http.headers = { 'User-Agent': 'Monkeys!' }
    return {
        # 'fs': bonobo.open_fs('s3://bonobo-examples')
        'http': http    
    }


if __name__ == '__main__':
    parser = bonobo.get_argument_parser()
    # parser.add_argument(
    #     '--use-cache', 
    #     action='store_true', 
    #     default=False
    # )

    with bonobo.parse_args(parser) as options:
        bonobo.run(
            get_graph(**options), 
            services=get_services(**options)
        )
