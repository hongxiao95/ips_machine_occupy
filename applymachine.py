#coding:utf-8
from art import text2art
from colorama import Fore, Back, Style
import colorama as cl
import json
import os
from datetime import datetime, timedelta

# 初始化 colorama
cl.init()

def load_gpu_list():
    """从文件中加载 GPU 列表"""
    if os.path.exists("gpulist.txt"):
        with open("gpulist.txt", "r") as file:
            return [line.strip() for line in file.readlines()]
    else:
        return []

def save_gpu_list(gpus):
    """将 GPU 列表保存到文件"""
    with open("gpulist.txt", "w") as file:
        for gpu in gpus:
            file.write(gpu + "\n")

def load_status():
    """从文件中加载 GPU 状态。如果文件为空或格式不正确，则返回空列表。"""
    try:
        if os.path.exists("status.conf"):
            with open("status.conf", "r") as file:
                data = file.read()
                # 检查文件是否为空
                if not data:
                    return []
                return json.loads(data)
        else:
            return []
    except json.JSONDecodeError:
        # 如果 JSON 数据格式不正确
        return []

def save_status(status):
    """将 GPU 状态保存到文件"""
    with open("status.conf", "w") as file:
        json.dump(status, file, indent=4)

def display_status(gpus, status):
    """展示 GPU 状态"""
    for gpu in gpus:
        # 查找 GPU 的当前状态
        gpu_status = next((item for item in status if item["name"] == gpu and item["end_time"] > datetime.now().isoformat()), None)

        # 如果找到了状态且 GPU 被占用
        if gpu_status:
            occupied = Back.RED + text2art(f"{gpu} Occupied") + Style.RESET_ALL
            print(f"{occupied} by {gpu_status['user']} until {gpu_status['end_time']}\n")
        else:
            # 否则认为 GPU 空闲
            available = Back.GREEN + text2art(f"{gpu} Available") + Style.RESET_ALL
            print(f"{available}\n")

def add_gpu(gpus):
    """添加 GPU"""
    new_gpu = input("Enter the name of the new GPU: ")
    gpus.append(new_gpu)

def delete_gpu(gpus):
    """删除 GPU"""
    gpu_to_delete = input("Enter the name of the GPU to delete: ")
    gpus.remove(gpu_to_delete)

def occupy_gpu(gpus, status):
    """抢占 GPU"""
    print("Available GPUs:")
    available_gpus = []
    for gpu in gpus:
        if not any(item for item in status if item["name"] == gpu and item["end_time"] > datetime.now().isoformat()):
            available_gpus.append(gpu)
            print(f"[{len(available_gpus)}] {gpu}")

    if not available_gpus:
        print("No GPUs available at the moment.")
        return

    try:
        choice = int(input("Choose a GPU to occupy (enter number): ")) - 1
        if choice < 0 or choice >= len(available_gpus):
            print("Invalid choice.")
            return
    except ValueError:
        print("Invalid input. Please enter a number.")
        return

    gpu_name = available_gpus[choice]
    user = input("Enter your name: ")
    duration = int(input("Enter the duration of use in hours (max 240): "))
    if duration > 240:
        print("Duration exceeds the maximum limit of 240 hours.")
        return
    password = input("Enter a password to release occupation: ")
    end_time = (datetime.now() + timedelta(hours=duration)).isoformat()

    # 更新状态
    status.append({"name": gpu_name, "start_time": datetime.now().isoformat(), "end_time": end_time, "user": user, "password": password})

def release_gpu(status):
    """释放 GPU 占用"""
    # 展示所有当前被占用的 GPUs
    occupied_gpus = [gpu for gpu in status if gpu["end_time"] > datetime.now().isoformat()]
    if not occupied_gpus:
        print("No GPUs are currently occupied.")
        return

    print("Occupied GPUs:")
    for i, gpu in enumerate(occupied_gpus, start=1):
        print(f"[{i}] {gpu['name']} (occupied by {gpu['user']})")

    try:
        choice = int(input("Choose a GPU to release (enter number): ")) - 1
        if choice < 0 or choice >= len(occupied_gpus):
            print("Invalid choice.")
            return
    except ValueError:
        print("Invalid input. Please enter a number.")
        return

    gpu_to_release = occupied_gpus[choice]
    password = input("Enter the password to release occupation: ")

    # 检查密码是否正确
    if gpu_to_release["password"] == password:
        status.remove(gpu_to_release)
        print(f"GPU {gpu_to_release['name']} has been released.")
    else:
        print("Incorrect password.")


def main():
    gpus = load_gpu_list()
    if not gpus:
        print("No GPU list found. Please enter GPU names (type '#' to finish):")
        while True:
            gpu_name = input()
            if gpu_name == '#':
                break
            gpus.append(gpu_name)
        save_gpu_list(gpus)

    status = load_status()
    display_status(gpus, status)

    # 用户交互部分
    while True:
        print("\nOptions: [1] Add GPU [2] Delete GPU [3] Occupy GPU [4] Release GPU [5] Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            add_gpu(gpus)
            save_gpu_list(gpus)
        elif choice == '2':
            delete_gpu(gpus)
            save_gpu_list(gpus)
        elif choice == '3':
            occupy_gpu(gpus, status)
            save_status(status)
        elif choice == '4':
            release_gpu(status)
            save_status(status)
        elif choice == '5':
            break
        display_status(gpus, status)

if __name__ == "__main__":
    main()
