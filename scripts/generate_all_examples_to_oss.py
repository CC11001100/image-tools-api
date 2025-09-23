#!/usr/bin/env python3
"""
生成所有接口的示例图片并上传到OSS - 重构版本
从 picsum.photos 下载随机图片，通过各个接口处理，上传原图和效果图到OSS

这是原 generate_all_examples_to_oss.py 的重构版本，
将原来的548行大文件拆分为多个小模块，提高可维护性。
"""

from example_generator.main_controller import ExampleGeneratorController


def main():
    """主函数"""
    controller = ExampleGeneratorController()
    controller.generate_all_examples()


if __name__ == "__main__":
    main()
