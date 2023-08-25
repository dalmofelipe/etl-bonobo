import bonobo
import time


def extract():
    """
    Placeholder, change, rename, remove... 
    transformation extract não possui entrada de dados, tem 
    apenas saidas
    """
    time.sleep(5)
    yield 'hello'
    time.sleep(5)
    yield 'world'



def transform(*args):
    """
    Placeholder, change, rename, remove... 
    transformation transform tem entradas e pode gerar
    zero, uma ou varias saidas
    """
    yield tuple(
        map(str.title, args)
    )


def load(*args):
    """
    Placeholder, change, rename, remove... 
    possui apenas entrada de dados, não pode ter saida!
    """
    time.sleep(5)
    print(*args)


def get_graph(**options):
    """
    This function builds the graph that needs to be executed.

    :return: bonobo.Graph

    $ bonobo inspect --graph tutorial.py | dot -Tpng -o tutorial.png
    """
    graph = bonobo.Graph()
    graph.add_chain(extract, transform, load)

    return graph


def get_services(**options):
    """
    This function builds the services dictionary, which is a simple dict of names-to-implementation used by bonobo
    for runtime injection.

    It will be used on top of the defaults provided by bonobo (fs, http, ...). You can override those defaults, or just
    let the framework define them. You can also define your own services and naming is up to you.

    :return: dict
    """
    return {}


# The __main__ block actually execute the graph.
# bonobo run tutorial.py
# python tutorial.py
if __name__ == '__main__':
    parser = bonobo.get_argument_parser()
    with bonobo.parse_args(parser) as options:
        bonobo.run(
            get_graph(**options),
            services=get_services(**options)
        )