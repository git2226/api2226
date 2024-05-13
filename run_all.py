#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2024/4/28 14:57
# Author    : smart
# @File     : run_all.py
# @Software : PyCharm
import unittest,os
from lib.HTMLTestRunner import HTMLTestRunner
from lib.send_email import send_email
from config.config import *
from test.suit.test_suit import *
import logging,time,pickle,sys

# class MyTestCase(unittest.TestCase):
#     def test_all(self):
#         logging.info("========运行所有的case========")
#         suit = unittest.defaultTestLoader.discover(test_path,'test*.py')
#         # t = time.strftime('%Y_%m_%d_%H_%M_%S')
#         with open(report_file,'wb') as f:
#             HTMLTestRunner(
#                 stream=f,
#                 title='xzs测试用例',
#                 description='xzs登陆和注册用例集',
#                 verbosity=2
#             ).run(suit)
#
#
#         send_email(report_file)
#         logging.info("========测试结束========")
#
# if __name__ == '__main__':
#     unittest.main()

def discover():#载入指定目录下的测试用例
    return unittest.defaultTestLoader.discover(test_case_path)

def run(suite):#执行测试用例，生成测试报告
    logging.info("====测试开始====")
    with open(report_file,'wb') as f:
        result = HTMLTestRunner(
            stream=f,
            title='接口测试',
            description='测试描述',
            verbosity=2
        ).run(suite)
    if result.failures:
        save_failures(result,last_fails_file)#保存失败用例到文件
        logging.error("测试失败，失败用例已保存到文件:{}".format(last_fails_file))
    else:
        logging.info("测试成功")

    if send_email_after_run:

    # logging.info("==== 测试报告已生成 ====")
        send_email(report_file)
    logging.info("====测试结束====")
def run_all():#运行所有用例
    run(discover())
def run_suite(suite_name):#运行自定义的testsuite
    suite = get_suite(suite_name)#通过套件名称返回套件实例
    print(suite)
    if isinstance(suite,unittest.TestSuite):
        run(suite)#运行套件
    else:
        print('TestSuite不存在')

def collect():
    suite = unittest.TestSuite()
    def _collect(tests):
        if isinstance(tests,unittest.TestSuite): #如果下级元素还是testsuite则继续往下找
            if tests.countTestCases() != 0: #如果testsuite中有用例则继续往下找
                for i in tests: #遍历testsuite
                    _collect(i) #递归调用
        else:
            suite.addTest(tests) #如果下级元素是testcase，则添加到testsuite中
    _collect(discover()) #unittest.defaulttestloader.discover(test_case_path)
    return suite

def collect_only(): #仅列出所有用例
    t0 = time.time() #开始时间
    i = 0 #用例计数
    for case in collect(): #遍历testsuite
        i += 1 #计数加1
        print("{}.{}".format(str(i),case.id()))
    print("---------------------------------")
    print("Collect {} tests is {:.3f}s".format(str(i),time.time() - t0))

def makesuite_by_testlist(test_list_file):
    with open(test_list_file,encoding='utf-8') as f:
        testlist = f.readlines()
    #去掉每行结尾的“/n"和#号开头的行
    testlist = [i.strip() for i in testlist if not i.startswith("#")]
    print(testlist)
    suite = unittest.TestSuite()
    all_cases = collect()#获取工程test/case目录及子目录下所有TestCase
    for case in all_cases:
        case_name = case.id().split('.')[-1] #获取TestCase名称
        print(case_name)
        if case_name in testlist:#从所有TestCase中匹配testlist中定义好的用例
            suite.addTest(case)
        # if case.testMethodName in testlist:#从所有TestCase中所配testlist中定义好的用例
        #     suite.addTest(case)
        return suite

# 根据tag来组建suite
def makesuite_by_tag(tag):
    # 申明一个suite
    suite = unittest.TestSuite()
    # 获取当前所有的testcase
    for i in collect():
        # tag和标签都包含的时候
        if i._testMethodDoc and tag in i._testMethodDoc:
            # 添加到testsuite中
            suite.addTest(i)
    return  suite

# 保存失败用例到文件
def save_failures(result,file):#file为序列化保存的文件名，配置在config/config.py中
    suite = unittest.TestSuite()
    for case_result in result.failures:
#         case_result是个元组，第一个元素是用例对象，后面是失败原因等等
        suite.addTest(case_result[0])
    with open(file,'wb') as f :
        pickle.dump(suite,f)#序列化到指定文件


def rerun_fails():#失败用例重跑方法
#   将用例路径添加到包搜索路径中，不然反序列化testsuite会找不到用例
    sys.path.append(test_case_path)
    with open(last_fails_file,'rb') as f:
        suite = pickle.load(f)#反序列化得到失败的testsuite
    run(suite)

def main():
    if options.collect_only:
        collect_only()
    elif options.rerun_fails:
        rerun_fails()
    elif options.tag:
        run(makesuite_by_tag(options.tag))
    elif options.test_list:  # 如果指定了--testlist参数
        run(makesuite_by_testlist(test_list_file))
    elif options.test_suite:  # 如果指定了--testsuite=***
        run_suite(options.test_suite)
    else:
        run_all()


if __name__ == '__main__':
    # collect_only()
    # suite = makesuite_by_testlist(test_list_file)
    # print(suite)
    # # suite = makesuite_by_tag("level1")
    # run(suite)
    # rerun_fails()
    run_all()
    # main()