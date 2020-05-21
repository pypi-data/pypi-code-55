import os
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from super_sweetest.elements import e
from super_sweetest.globals import g
from super_sweetest.log import logger
from super_sweetest.config import element_wait_timeout


def locating_element(element, action=''):
    el_location = None
    try:
        el, value = e.get(element)
    except:
        logger.exception(
            'Locating the element:%s is Failure, this element is not define' % element)
        raise Exception(
            'Locating the element:%s is Failure, this element is not define' % element)

    if not isinstance(el, dict):
        raise Exception(
            'Locating the element:%s is Failure, this element is not define' % element)

    wait = WebDriverWait(g.driver, element_wait_timeout)

    if el['by'].lower() in ('title', 'url', 'current_url'):
        return None
    else:
        try:
            el_location = wait.until(EC.presence_of_element_located(
                (getattr(By, el['by'].upper()), value)))
        except:
            sleep(5)
            try:
                el_location = wait.until(EC.presence_of_element_located(
                    (getattr(By, el['by'].upper()), value)))
            except :
                raise Exception('Locating the element:%s is Failure: Timeout' % element)
    try:
        if g.driver.name in ('chrome', 'safari'):
            g.driver.execute_script(
                "arguments[0].scrollIntoViewIfNeeded(true)", el_location)
        else:
            g.driver.execute_script(
                "arguments[0].scrollIntoView(false)", el_location)
    except:
        pass

    try:
        if action == 'CLICK':
            #增加class_name elements 通过 index定位 点击
            if  isinstance(int(el['remark']),int):
                el_location = {'elements': el['by'], 'value': value, 'index_': int(el['remark'])}  # 反回所需参数到mobile.py
            else:
                el_location = wait.until(EC.element_to_be_clickable(
                    (getattr(By, el['by'].upper()), value)))
        else:
            # elements 输入 remark 是 int 执行index取值
            if isinstance(int(el['remark']), int):
            # if 'class_name' == el['by'] and isinstance(int(el['remark']), int):
                el_location = {'elements': el['by'],'value': value,'index_': int(el['remark'])}  #反回所需参数到mobile.py
            else:
                el_location = wait.until(EC.visibility_of_element_located(
                    (getattr(By, el['by'].upper()), value)))
    except:
        pass

    return el_location


def locating_elements(elements):
    elements_location = {}
    for el in elements:
        elements_location[el] = locating_element(el)
    return elements_location


def locating_data(keys):
    data_location = {}
    for key in keys:
        data_location[key] = locating_element(key)
    return data_location


def locating_air_element(step):
    element = step['element']
    plan_name = g.plan_name
    try:
        el, value = e.get(element)
    except:
        logger.exception(
            'Locating the element:%s is Failure, this element is not define' % element)
        raise Exception(
            'Locating the element:%s is Failure, this element is not define' % element)

    if step['keyword'] in [ 'TAP', 'CHECK', 'NOTCHECK',  'WAIT_']:
        value_list = value.replace(' ', '').replace('，', ',').replace('\n','').split(',')

        # png
        png = [pho for pho in value_list if pho.endswith('.png')]
        photo = png[0] if png else value
        assert photo.endswith('.png'), '当前图片：%s 格式不正确，正确 png 格式：photoname.png' % photo
        photo_path = os.path.join('./data', plan_name, photo)

        # threshold
        thr = [thr for thr in value_list if 'threshold' in thr.lower()]
        threshold_value = thr[0].split('=')[1] if thr else 0.7

        # target_pos
        target_p = [target_p for target_p in value_list if 'target_pos' in target_p.lower()]
        target_pos_value = target_p[0].split('=')[1] if target_p else 5

        # rgb
        rg = [rg for rg in value_list if 'rgb' in rg.lower()]
        rgb_ = rg[0].split('=')[1] if rg else True
        rgb_value = False if not isinstance(rgb_, bool) and 'false' in rgb_.lower() else True

        el_location = photo_path, float(threshold_value), int(target_pos_value), rgb_value

    elif step['keyword'] in ['INPUT']:
        el_location = el['by'], value
    elif step['keyword'] == 'SWIPE':
        # 固定坐标滑动
        # assert re.match(r"^(?:[0-9]{1,4}\,){3}[0-9]{1,4}$", value), '当前坐标：%s 格式或数量不对，正确格式如：3000,20,3000,400'% value
        # 相对坐标滑动
        num_list = value.replace('，', ',').split(',')
        error_num_msg = '当前坐标：%s 格式或数量不对，正确格式如：0.2, 0.2, 2, 6\n' \
                                                                    'w,w,h,h\n' \
                                                                    'width  宽  w1 w2 小数  0.1 - 0.9\n' \
                                                                    'height 高  h1 h2 正数  1 - 9'% value
        assert (type(eval(num_list[0])) == float), error_num_msg
        assert (type(eval(num_list[1])) == float), error_num_msg
        assert (type(eval(num_list[2])) == int), error_num_msg
        assert (type(eval(num_list[3])) == int), error_num_msg

        el_location = num_list
    elif step['keyword'] == 'SWIPE_PHOTO':
        values = []
        value_ = value.replace('，',',').split(',')
        error_png_msg = '当前图片：%s 格式不正确，正确 图片滑动 格式：photoname.png#photoname1.png'% value
        if len(value_) != 2:
            raise error_png_msg
        for v in value_:
            assert v.endswith('.png'), error_png_msg
            values.append(os.path.join('./data', plan_name, v))
        el_location = values
    elif step['keyword'] in  ['CLICK', 'CHECK_TEXT', 'NOTCHECK_TEXT']:
        el_location = el['by'], value
    elif step['keyword'] in ('BACK', 'HOME', 'MENU', 'POWER'):
        el_location = step['keyword']
    else:
        el_location = value

    return el_location