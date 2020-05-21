# coding = utf-8
# f = open("./test.mgf").readlines()
from numpy import array, inner, linalg


def readMGF(mgf_path):
    print("reading mgf file")
    print("the mgf path is %s" % mgf_path)
    f = open(mgf_path).readlines()
    scanInfoDic = {}
    i = 0
    while i < len(f):
        if f[i].strip() != "BEGIN IONS":
            i += 1
        else:
            scanTitle = f[i+1].split("=")[1].strip()
            # print(i)
            scanNum = int(scanTitle.split(".")[1])
            charge = int(f[i+2].split("=")[1][:-2])
            mzPre = float(f[i+4].split("=")[-1].strip())
            specInfo = []
            p = i + 5
            while p < len(f):
                if f[p].strip() == "END IONS":
                    break
                else:
                    lineList = f[p].split(" ")
                    mz = float(lineList[0])
                    ints = float(lineList[1].strip())
                    specInfo.append([mz, ints])
                    p += 1
            scanInfoDic[scanTitle] = [mzPre, charge, specInfo]
        i = p + 1
    return scanInfoDic


def compare2mz(mz1, mz2, ppm_tol):
    delta = mz1 * ppm_tol / 1000000
    mz2_up = mz2 + delta
    mz2_down = mz2 - delta
    if mz1 > mz2_up:
        return "mz2_up"
    elif mz1 < mz2_down:
        return "mz1_up"
    else:
        return "upup"


def cal_cosin_dis(ints1_list, ints2_list):
    a1 = array(ints1_list)
    a2 = array(ints2_list)
    cos = inner(a1, a2)/linalg.norm(a1)/linalg.norm(a2)
    return 0.5+0.5*cos


def cal_ints_dis(ints1_list, ints2_list):
    if len(ints1_list) != len(ints2_list):
        print("wrong")
        return 
    else:
        max_ints1 = max(ints1_list)
        max_ints2 = max(ints2_list)

        dist = 0
        for i in range(len(ints1_list)):
            int_v = [ints1_list[i]/max_ints1, ints2_list[i]/max_ints2]
            if 0 in int_v:
                dist += sum(int_v)
            else:
                dist += pow((int_v[0]-int_v[1]), 2)
        return dist


def compare2spec(ref_spec, spec2):
    dist = 0
    mz1_list = [x[0] for x in ref_spec]
    max_ints_ref = max([x[1] for x in ref_spec])
    mz2_list = [x[0] for x in spec2]
    max_ints_real = max([x[1] for x in spec2])
    mz1_alone = []
    mz2_alone = []
    ints1_list = []
    ints2_list = []
    overlap = []
    idx1 = 0
    idx2 = 0
    while idx1 < len(mz1_list) and idx2 < len(mz2_list):
        state = compare2mz(mz1_list[idx1], mz2_list[idx2], 500)
        if state == 'mz1_up':
            mz1_alone.append(mz1_list[idx1])
            ints1_list.append(ref_spec[idx1][1])
            ints2_list.append(0)
            # dist += ref_spec[idx1][1]/max_ints_ref
            idx1 += 1
        elif state == "mz2_up":
            mz2_alone.append(mz2_list[idx2])
            ints2_list.append(spec2[idx2][1])
            ints1_list.append(0)
            # dist += spec2[idx2][1]/max_ints_real
            idx2 += 1
        else:
            overlap.append([mz1_list[idx1], mz2_list[idx2]])
            ints1_list.append(ref_spec[idx1][1])
            ints2_list.append(spec2[idx2][1])
            # dist += pow(ref_spec[idx1][1]/max_ints_ref-spec2[idx2][1]/max_ints_real, 2)
            idx1+= 1
            idx2 += 1

    # print(idx1, idx2)
    # print(len(mz1_list), len(mz2_list))        

    if idx1 == len(mz1_list):
        mz2_alone.extend(mz2_list[idx2:])
        for i in range(idx2, len(mz2_list)):
            # dist += spec2[i][1]/max_ints_real
            ints2_list.append(spec2[i][1])
            ints1_list.append(0)
    elif idx2 == len(mz2_list):
        mz1_alone.extend(mz1_list[idx1:])
        for i in range(idx1, len(mz1_list)):
            # dist += ref_spec[i][1]/max_ints_ref
            ints1_list.append(ref_spec[i][1])
            ints2_list.append(0)
    
    dist = cal_cosin_dis(ints1_list, ints2_list)
    # dist = cal_ints_dis(ints1_list, ints2_list)
    return round(dist, 4)

if __name__ == "__main__":
    scanInfoDic = readMGF("./AC_IR7_SDA_dyn7_R1_HCDFT.mgf")
    scan_list = [7390, 7847, 10186, 10431, 10618, 10680]
    for i in range(len(scan_list)-1):
        scan1 = scan_list[i]
        spec1 = scanInfoDic[scan1][-1]
        for j in range(i+1, len(scan_list)):
            scan2 = scan_list[j]
            spec2 = scanInfoDic[scan2][-1]
            print(scan1, scan2)
            print(compare2spec(spec1, spec2))
    # spec7390 = scanInfoDic[7390][-1]
    # spec7847 = scanInfoDic[7847][-1]
    # spec10186 = scanInfoDic[10186][-1]
    # spec10431 = scanInfoDic[10431][-1]
    # spec10618 = scanInfoDic[10618][-1]
    # spec10680 = scanInfoDic[10680][-1]
    # print(compare2spec(spec7390, spec7847))
    # print(compare2spec(spec10186, spec7847))
    # print(compare2spec(spec10186, spec10431))
    # print(compare2spec(spec10618, spec10431))
    # print(compare2spec(spec10680, spec10431))
    # print(compare2spec(spec10680, spec10618))
