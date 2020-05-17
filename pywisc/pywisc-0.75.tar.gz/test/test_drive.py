from pywisc.tools.csv_drive import DriveCSV


def test_ver4_es_ar_6_0_drive():
    uid = '1qM_iwvnCLTlrudcaWr_scbrsYqy6g6GCyyYXImpO5uo'
    gid = '0'
    d = DriveCSV(name='wisc-4-es-ar-6-0-6-3',
                 unique_id_column='Escalar',
                 uid=uid, gid=gid,
                 force_re_download=True)
    data = d.tree
    for d in data:
        if d['Cl'] == 21:
            assert d['Escalar'] == 7


def test_ver4_es_ar_15_0_drive():
    uid = '1qM_iwvnCLTlrudcaWr_scbrsYqy6g6GCyyYXImpO5uo'
    gid = '1247042929'
    d = DriveCSV(name='wisc-4-es-ar-15-0-15-3',
                 unique_id_column='Escalar',
                 uid=uid, gid=gid,
                 force_re_download=True)
    data = d.tree
    for d in data:
        if d['Cl'] == 55:
            assert d['Escalar'] == 8


def testB_ver4_es_ar_15_0_drive():
    uid = '1qM_iwvnCLTlrudcaWr_scbrsYqy6g6GCyyYXImpO5uo'
    gid = '1247042929'
    d = DriveCSV(name='wisc-4-es-ar-15-0-15-3',
                 unique_id_column='Escalar',
                 uid=uid, gid=gid,
                 force_re_download=True)
    data = d.tree
    for d in data:
        if d['Co'] == 23:  # este tiene un elemento vacio
            assert d['Escalar'] == 13
        elif d['Co'] == 24:  # este tiene un elemento vacio
            assert d['Escalar'] == 15
