from datetime import datetime, timedelta
import calendar

def get_dolar_contract(today=None):
    """
    Retorna o código do contrato vigente de mini dólar (WDO).
    Considera rolagem no último dia útil do mês.
    """
    if today is None:
        today = datetime.now()

    year = today.year % 100
    month = today.month

    # Último dia útil do mês
    last_day = calendar.monthrange(today.year, month)[1]
    last_date = datetime(today.year, month, last_day)

    # Ajusta se cair no fim de semana
    while last_date.weekday() >= 5:
        last_date -= timedelta(days=1)

    # Se hoje for o último dia útil ou depois, rola para o próximo mês
    if today.date() >= last_date.date():
        month += 1
        if month > 12:
            month = 1
            year += 1

    letras = {1: "F", 2: "G", 3: "H", 4: "J", 5: "K", 6: "M",
              7: "N", 8: "Q", 9: "U", 10: "V", 11: "X", 12: "Z"}

    return f"WDO{letras[month]}{year}"


def get_indice_contract(today=None):
    """
    Retorna o código do contrato vigente de mini índice (WIN).
    Considera rolagem no dia anterior ao vencimento.
    """
    if today is None:
        today = datetime.now()

    year = today.year % 100
    month = today.month

    # Próximo mês par
    if month % 2 != 0:
        month += 1
        if month > 12:
            month = 2
            year += 1

    # Vencimento: quarta-feira mais próxima do dia 15
    base_date = datetime(today.year, month, 15)
    weekday = base_date.weekday()

    if weekday <= 2:  # segunda a quarta
        vencimento = base_date - timedelta(days=weekday - 2)
    else:  # quinta a domingo
        vencimento = base_date + timedelta(days=2 - weekday)

    # Se hoje for o dia anterior ao vencimento ou depois, rola para o próximo par
    if today.date() >= (vencimento - timedelta(days=1)).date():
        month += 2
        if month > 12:
            month = 2
            year += 1

    letras = {2: "G", 4: "J", 6: "M", 8: "Q", 10: "V", 12: "Z"}

    return f"WIN{letras[month]}{year}"
