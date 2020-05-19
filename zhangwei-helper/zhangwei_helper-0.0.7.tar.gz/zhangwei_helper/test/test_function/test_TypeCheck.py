import pytest
import zhangwei_helper.function.TypeCheck as type_check
@pytest.mark.check_if_ipv4
class Test_check_if_ipv4(object):
    def test_value_type_not_string(self):
        assert type_check.check_if_ipv4(value=set()) == \
               False


    def test_value_split_not_4_element(self):
        assert type_check.check_if_ipv4(value='1.1.1') == \
               False

    def test_value_splitted_element_contain_0_string(self):
        assert type_check.check_if_ipv4(value=r"''.1.1.1") == \
               False

    def test_value_splitted_element_contain_4_string(self):
        assert type_check.check_if_ipv4(value=r"1111.1.1.1") == \
               False

    def test_value_splitted_element_cant_convert_int(self):
        assert type_check.check_if_ipv4(value=r"a.1.1.1") == \
               False

    def test_value_splitted_element_less_0(self):
        assert type_check.check_if_ipv4(value=r"-1.1.1.1") == \
               False

    def test_value_splitted_element_greater_0(self):
        assert type_check.check_if_ipv4(value=r"300.1.1.1") == \
               False

    def test_value_valid(self):
        assert type_check.check_if_ipv4(value=r"255.1.1.1") == \
               True


@pytest.mark.check_if_ipv4_port
class Test_check_if_ipv4_port(object):
    def test_value_type_not_string(self):
        assert type_check.check_if_ipv4_port(value=set()) == \
               False

    def test_value_cant_convert_int(self):
        assert type_check.check_if_ipv4_port(value='a') == \
               False

    def test_value_convert_less_0(self):
        assert type_check.check_if_ipv4_port(value='-1') == \
               False

    def test_value_convert_greater_65535(self):
        assert type_check.check_if_ipv4_port(value='1000000') == \
               False

    def test_value_correct(self):
        assert type_check.check_if_ipv4_port(value='8080') == \
               True