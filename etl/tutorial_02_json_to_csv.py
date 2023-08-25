import bonobo

from bonobo.config import use_context_processor

import requests


COMMENTS_API_URL = 'https://jsonplaceholder.typicode.com/comments'


def extract_comments():
    yield from requests.get(COMMENTS_API_URL).json()
    # .get('records')


def transform(*row:tuple):
    """
    id;postId;name;email;body
    {
        'postId': 1, 
        'id': 1, 
        'name': 'id labore ex et quam laborum', 
        'email': 'Eliseo@gardner.biz', 
        'body': 'laudantium enim quasi est quidem magnam voluptate ipsam eos\ntempora quo necessitatibus\ndolor quam autem quasi\nreiciendis et nam sapiente accusantium'
    }
    print(f'\t>>>>>> {type(row[0])}')
    print(f'\t>>>>>> {row[0]["name"]}')
    """
    comment = row[0]
    comment["body"] = comment["body"].replace('\n', '|')
    yield (
        comment["id"],
        comment["postId"],
        comment["name"],
        comment["email"],
        comment["body"],
    )

def with_opened_file(self, context):
    with context.get_service('fs').open('outputs/tutorial_02_json_to_csv.csv', 'w+') as f:
        f.write(f'id;postId;name;email;body\n')
        yield f


@use_context_processor(with_opened_file)
def write_repr_to_file(f, *row):
    """
    """
    line  = ';'.join(str(v) for v in row)
    f.write(line + '\n')


def get_graph(**options):
    graph = bonobo.Graph()
    graph.add_chain(
        extract_comments, 
        bonobo.Limit(10),
        #bonobo.CsvWriter('outputs/tutorial_02_json_to_csv.csv'),
        bonobo.PrettyPrinter(),
        transform,
        write_repr_to_file
    )
    return graph


def get_services(**options):
    """
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
