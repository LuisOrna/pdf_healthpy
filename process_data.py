from datetime import date


def get_today():
    today = date.today()
    return str(today.day).zfill(2), str(today.month).zfill(2), str(today.year)


def calculate_age(nacimiento):
    day, month, year = nacimiento.split("-")
    today = date.today()
    birth = date(int(year), int(month), int(day))
    age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
    return str(age)


def get_form_type(nacimiento):
    age = int(calculate_age(nacimiento))
    return "djs_m" if age < 18 else "djs_a"


def split_birth_date(nacimiento):
    day, month, year = nacimiento.split("-")
    return day, month, year


def convert_sex(sexo):
    mapping = {
        "FEMENINO": "F",
        "MASCULINO": "M"
    }
    return mapping.get(sexo.upper(), sexo)


def process(verified_data):
    dia_hoy, mes_hoy, year_hoy = get_today()
    dia_nac, mes_nac, year_nac = split_birth_date(verified_data["nacimiento"])

    return {
        "titular":   verified_data["nombres"] + " " + verified_data["apellidos"],
        "declarante": verified_data["nombres"] + " " + verified_data["apellidos"],
        "cedula":    verified_data["numero"],
        "dia_nac":   dia_nac,
        "mes_nac":   mes_nac,
        "year_nac":  year_nac,
        "edad":      calculate_age(verified_data["nacimiento"]),
        "sexo":      convert_sex(verified_data["sexo"]),
        "dia":       dia_hoy,
        "mes":       mes_hoy,
        "year":      year_hoy,
        "Plan":      verified_data["plan"]
    }
