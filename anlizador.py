variables = {}
palabras_reservadas = ["int", "float", "char", "bool", "string"]

def es_float(val):
    try:
        float(val)
        return True
    except ValueError:
        return False

def valor_valido_para_tipo(tipo, valor):
    if tipo == "int":
        return valor.isdigit()
    if tipo == "float":
        return es_float(valor)
    if tipo == "char":
        return len(valor) == 3 and valor.startswith("'") and valor.endswith("'")
    if tipo == "bool":
        return valor in ["true", "false"]
    if tipo == "string":
        return valor.startswith('"') and valor.endswith('"')
    return False

def obtener_valor_y_tipo(operando):
    if operando in variables:
        val = variables[operando]["valor"]
        tipo = variables[operando]["tipo"]
        if val is None:
            return None, None, f"Variable '{operando}' no está inicializada"
        return val, tipo, None
    if operando.startswith('"') and operando.endswith('"'):
        return operando, "string", None
    if len(operando) == 3 and operando.startswith("'") and operando.endswith("'"):
        return operando, "char", None
    if operando in ["true", "false"]:
        return operando, "bool", None
    if operando.isdigit():
        return operando, "int", None
    if es_float(operando):
        return operando, "float", None
    return None, None, f"Operando inválido '{operando}'"

def evaluar_expresion(expr):
    partes = [p.strip() for p in expr.split("+")]
    if len(partes) != 2:
        return None, None, "Expresión no soportada (solo se permite una suma con '+')"
    val1, tipo1, err1 = obtener_valor_y_tipo(partes[0])
    val2, tipo2, err2 = obtener_valor_y_tipo(partes[1])
    if err1 or err2:
        return None, None, err1 or err2
    if tipo1 in ["int", "float"] and tipo2 in ["int", "float"]:
        resultado = str(float(val1) + float(val2))
        tipo_res = "float" if "float" in (tipo1, tipo2) else "int"
        return resultado, tipo_res, None
    if tipo1 in ["string", "char"] and tipo2 in ["string", "char"]:
        resultado = val1.strip("'\"") + val2.strip("'\"")
        return f'"{resultado}"', "string", None
    return None, None, f"No se puede aplicar '+' entre '{tipo1}' y '{tipo2}'"

def analizar_declaracion(tipo, var, valor=None):
    if not var.isidentifier():
        print("Error: Nombre de variable inválido")
        return False
    if valor is None:
        variables[var] = {"tipo": tipo, "valor": None}
        print(f"Declaración válida: variable '{var}' de tipo {tipo}")
        return True
    elif valor_valido_para_tipo(tipo, valor):
        variables[var] = {"tipo": tipo, "valor": valor}
        print(f"Declaración válida: variable '{var}' de tipo {tipo} con valor {valor}")
        return True
    else:
        print(f"Error: Valor inválido para tipo {tipo}")
        return False

def analizar_asignacion(var, expr):
    if var not in variables:
        print(f"Error: Variable '{var}' no está declarada")
        return False
    tipo_var = variables[var]["tipo"]

    if "+" in expr:
        resultado, tipo_res, err = evaluar_expresion(expr)
        if err:
            print("Error:", err)
            return False
        if tipo_res != tipo_var and not (tipo_var == "float" and tipo_res == "int"):
            print(f"Error: El resultado '{tipo_res}' no es compatible con tipo '{tipo_var}'")
            return False
        variables[var]["valor"] = resultado
        print(f"Asignación válida: '{var}' = {resultado}")
        return True
    else:
        val, tipo_val, err = obtener_valor_y_tipo(expr)
        if err:
            print("Error:", err)
            return False
        if tipo_val != tipo_var and not (tipo_var == "float" and tipo_val == "int"):
            print(f"Error: Tipo '{tipo_val}' no compatible con '{tipo_var}'")
            return False
        variables[var]["valor"] = val
        print(f"Asignación válida: '{var}' = {val}")
        return True

def analizador(linea):
    linea = linea.strip()
    if not linea.endswith(";"):
        print("Error: Falta ';' al final")
        return False
    linea = linea[:-1].strip()

    if not linea:
        print("Error: Línea vacía")
        return False

    partes = linea.split()
    if partes[0] in palabras_reservadas:
        tipo = partes[0]
        if len(partes) == 2:
            return analizar_declaracion(tipo, partes[1])
        elif len(partes) == 4 and partes[2] == "=":
            return analizar_declaracion(tipo, partes[1], partes[3])
        else:
            print("Error: Sintaxis de declaración inválida")
            return False

    if "=" in linea:
        izq, der = [s.strip() for s in linea.split("=", 1)]
        return analizar_asignacion(izq, der)

    if "+" in linea:
        resultado, tipo, err = evaluar_expresion(linea)
        if err:
            print("Error:", err)
            return False
        print(f"Resultado de la expresión: {resultado}")
        return True

    print("Error: Línea no válida")
    return False

print("Introduce líneas de código C (deja una línea vacía para terminar):")
while True:
    linea = input(">")
    if linea.strip() == "":
        break
    analizador(linea)
