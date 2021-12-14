import json


def json_reader(path):
    f = open(path)
    data = json.load(f)
    f.close()

    return data


def hex_to_dec(l):
    if l == 'A':
        return 10
    elif l == 'B':
        return 11
    elif l == "C":
        return 12
    elif l == "D":
        return 13
    elif l == "E":
        return 14
    elif l == "F":
        return 15
    else:
        return l

def dec_to_hex(l):
    if l == 10:
        return 'A'
    elif l == 11:
        return 'B'
    elif l == 12:
        return 'C'
    elif l == 13:
        return 'D'
    elif l == 14:
        return 'E'
    elif l == 15:
        return 'F'
    else:
        return l


def bit_revert(s):
    neg_num = ""
    for i, val in enumerate(s):
        if i > 0:
            neg_num = neg_num + str(1 - int(val))

    return str(neg_num)


def get_accode(cat_ac, z_r, val):
    ac_code = json_reader('AC_Code.json')

    cat_found = False
    i = 0
    run_cat = str(dec_to_hex(z_r)) + '/' + str(hex_to_dec(cat_ac))
    while not cat_found:
        if ac_code[i]["runcat"] == run_cat:
            base_code = ac_code[i]["base"]
            code_len = ac_code[i]["len"]
            cat_found = True
        else:
            if i > len(ac_code):
                cat_found = True

        i = i + 1

    data_len = str(code_len - len(str(base_code)))

    data = str('{0:0' + data_len + 'b}').format(val)
    if val < 0:
        data = bit_revert(data)

    code = base_code + data

    return code


def get_dccode(cat, val):
    cat = int(hex_to_dec(cat))
    dc_code = json_reader('DC_Code.json')
    base_code = dc_code[cat]["base"]
    code_len = dc_code[cat]["len"]

    data_len = str(code_len - len(str(base_code)))

    data = str('{0:0' + data_len + 'b}').format(val)
    if val < 0:
        data = bit_revert(data)

    code = base_code + data

    return code


def get_jpg_coef(val, t, z_r=0):
    code = ""
    jpg_coef = json_reader('JPEG_Coef.json')

    for i, rank in enumerate(jpg_coef):

        if rank["lower"] <= abs(val) <= rank["upper"]:
            if t == "dc":
                cat_dc = rank["dccat"]
                code = get_dccode(cat_dc, val)
            else:
                cat_ac = rank["accat"]
                code = get_accode(cat_ac, z_r, val)

    return code


def code_gen(sq, prev_dc):
    code = ""
    zero_run = 0
    for i in range(len(sq)):
        if i == 0:
            sq[i] = sq[i] - prev_dc
            prev_dc = sq[i]
            # Do DC
            code_dc = get_jpg_coef(sq[i], "dc")
            code = code + code_dc
        else:
            if sq[i] == 0 or sq[i] == '0':
                zero_run = zero_run + 1
            else:
                code_ac = get_jpg_coef(sq[i], "ac", zero_run)
                code = code + code_ac
                zero_run = 0

    code = code + "1010"
    return code, prev_dc




def zigzag(sq):
    rows = sq.shape[0]
    columns = sq.shape[1]
    solution = [[] for i in range(rows + columns - 1)]

    for r in range(rows):
        for c in range(columns):
            sm = r + c
            if sm % 2 == 0:
                solution[sm].insert(0, sq[r][c])
            else:
                solution[sm].append(sq[r][c])

    return sequence_matrix(solution)


def sequence_matrix(s):
    seq = []
    for i in s:
        for j in i:
            seq.append(j)

    return seq
