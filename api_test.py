# --*-- encoding:utf-8 --*--
import os
import requests
import subprocess
from log import logging

try:
    from openpyxl import load_workbook
    from lxml import etree
except Exception as e:
    subprocess.call("pip install openpyxl", shell=True)
    subprocess.call("pip install lxml", shell=True)
    from openpyxl import load_workbook
    from lxml import etree


def check_version(response):
    page = etree.HTML((response.content.decode("utf-8")).lower())

    infos = page.xpath("//h3")

    for info in infos:
        # 原则上均能获取到版本号
        if "version:" in info.text:
            check_version = info.text

    return check_version


def api_test():
    try:
        cases = os.listdir("./testcase/")
        for case in cases:
            # 表格中行数，调用api_test()时从第i行开始读取数据
            i = 3
            wb = load_workbook("./testcase/" + case)
            sheet = wb["TestCase"]
            checked_version = check_version(requests.get(sheet["G2"].value))
            if checked_version != sheet["M2"].value:
                logging.info("checked %s update and the %s is Testing" % (checked_version, case))
                while sheet["B%d" % i].value is not None:
                    try:
                        url = sheet["G%d" % i].value
                        params = sheet["H%d" % i].value.encode('utf-8')
                        headers = {'Content-Type': 'application/json'}

                        # 确认请求类型
                        if sheet["F%d" % i].value == "Post":
                            response = requests.post(url, data=params, headers=headers)
                        elif sheet["F%d" % i].value == "Get":
                            response = requests.get(url, data=params, headers=headers)
                        elif sheet["F%d" % i].value == "Put":
                            response = requests.put(url, data=params, headers=headers)
                        elif sheet["F%d" % i].value == "Update":
                            response = requests.update(url, data=params, headers=headers)
                        elif sheet["F%d" % i].value == "Delete":
                            response = requests.delete(url, data=params, headers=headers)
                        else:
                            logging.error(
                                case + " " + sheet["A%d" % i].value + " request method " + sheet["F%d" % i].value +
                                " not support, please contact the admin")
                            continue

                        # 将返回的状态码写入测试结果
                        sheet["K%d" % i] = response.status_code
                        # 判断返回的状态码与预期是否一致，不一致则直接fail，一致则进一步判断返回值是否包含相应的关键字
                        if response.status_code == sheet["I%d" % i].value:
                            if sheet["J%d" % i].value in response.content.decode("utf-8"):
                                sheet["L%d" % i] = "Pass"
                                sheet["M%d" % i] = response.content.decode("utf-8")
                                logging.info(case + " " + sheet["A%d" % i].value + response.content.decode("utf-8"))
                            else:
                                sheet["L%d" % i] = "Fail"
                                sheet["M%d" % i] = response.content.decode("utf-8")
                                logging.error(
                                    case + " " + sheet["A%d" % i].value + response.content.decode("utf-8"))
                        else:
                            sheet["L%d" % i] = "Fail"
                            sheet["M%d" % i] = response.content.decode("utf-8")
                            logging.error(case + " " + sheet["A%d" % i].value + response.content.decode("utf-8"))

                        i += 1
                    except Exception as e:
                        logging.error(case + " " + sheet["A%d" % i].value + "Error: " + str(e))
                        i += 1
                        continue

                sheet["M2"].value = checked_version
                logging.info("The new version is updated. ")
                logging.info("the %s test is completed. " % case)
                logging.info("------------------------------------------------------------------------------------\n\n")
                wb.save("./testcase/" + case)
                subprocess.call("cp /opt/auto_run/testcase/%s /home/xjin/.jenkins/workspace/API_Test/" % case,
                                shell=True)
            else:
                logging.info("%s No new version found. " % case)
                logging.info("------------------------------------------------------------------------------------\n\n")
    except Exception as e:
        raise e


if __name__ == '__main__':
    api_test()
