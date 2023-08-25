

def passicional_args_nomedo_kargs(a, b = 0, *args, c = 3, d = 4, funcao = "nomeado", **kargs):
    """
    parametros possicionais (a) são obrigatorios!
    """
    print(f"a {a}, b {b}, c {c}, d {d}")
    print(f"função = {funcao}")
    for arg in args: print(f"arg {arg}")
    for value in kargs.values(): print(f"karg {value}")



if __name__ == '__main__':

    kargs_params = {
        'id_origin': 1010,
        'id_destine': 2020,
        'ammount': 4200
    }

    passicional_args_nomedo_kargs(22, 44, 55, kargs_params, d=222, c = 99, funcao='programador')
