def progress_bar(value, max_value, size):
    """
    Cria uma barra de progresso em texto.
    :param value: Valor atual (int ou float)
    :param max_value: Valor máximo (int ou float)
    :param size: Tamanho da barra (número de caracteres)
    :return: dict com 'bar' (str) e 'percentage_text' (str)
    """
    if max_value == 0:
        percentage = 0
    else:
        percentage = value / max_value

    progress = round(size * percentage)
    empty_progress = size - progress

    progress_text = "▇" * progress
    empty_progress_text = "—" * empty_progress
    percentage_text = f"{round(percentage * 100)}%"

    bar = progress_text + empty_progress_text
    return {"bar": bar, "percentage_text": percentage_text}
