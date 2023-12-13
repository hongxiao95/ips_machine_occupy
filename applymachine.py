#coding:utf-8
from art import text2art
from colorama import Fore, Back, Style
import colorama as cl

def main():
    # 尝试从gpulist.txt读取GPU列表
    # 如无GPU列表，请求输入GPU列表，每输入一个就回车确认，如果输入#说明输入完成
    # 如有GPU列表，尝试从status.conf读取各GPU状态
    # 展示当前各GPU状态，用art库结合colorama，用红色和绿色显示GPU占用情况，最好有预期占用解除的进度条
    # 可选择：添加GPU、删除GPU、抢占GPU、续租GPU、解除抢占GPU
    # 如用户选择抢占GPU，只可以选择抢占当前空闲的CPU，需要输入自己的名字、预计使用时长（小时），最长不超过10天、解除抢占的密码
    # GPU列表存储在和本python文件同级的文件夹的gpulist.txt文件夹中，每行一个gpu名称
    # GPU占用情况以json文本的形式存储在本python文件同级的status.conf中，应当是一个json数组，里面每个元素描述一个GPU，是一个map,包含GPU名、起始占用时间、请求的使用时长、占用人、占用人密码等
    
    pass

if __name__ == "__main__":
    main()