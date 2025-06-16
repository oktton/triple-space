import unittest
import time
from unittest.mock import Mock
from pynput.keyboard import Controller
from pynput import keyboard
from listener import TripleSpacesListener

class TestTripleSpacesListener(unittest.TestCase):

    def setUp(self):
        """在每个测试前创建一个新的 TripleSpacesListener 实例"""
        self.mock_on_fire = Mock()  # 创建一个 mock 函数
        self.listener = TripleSpacesListener(self.mock_on_fire)
        self.controller = Controller()  # 用于模拟按键输入

    def tearDown(self):
        """测试结束后停止监听器"""
        self.listener.kb_listener.stop()

    def test_triple_space_fires_event(self):
        """测试连续 3 次空格是否触发 on_fire()"""
        with self.listener:  # 进入监听模式
            time.sleep(0.1)  # 等待监听器启动
            
            # 模拟按键输入
            self.controller.press(' ')
            self.controller.release(' ')
            time.sleep(0.1)

            self.controller.press(' ')
            self.controller.release(' ')
            time.sleep(0.1)

            self.controller.press(' ')
            self.controller.release(' ')
            time.sleep(0.1)  # 确保监听器有时间检测输入

            # 断言 on_fire() 被调用了一次
            self.mock_on_fire.assert_called_once()

    def test_slow_triple_space_does_not_fire(self):
        """测试如果空格间隔超过 0.2 秒，不会触发 on_fire()"""
        with self.listener:
            time.sleep(0.1)

            self.controller.press(' ')
            self.controller.release(' ')
            time.sleep(0.3)  # 等待超过 0.2s

            self.controller.press(' ')
            self.controller.release(' ')
            time.sleep(0.1)

            self.controller.press(' ')
            self.controller.release(' ')
            time.sleep(0.1)

            # 断言 on_fire() **没有被调用**
            self.mock_on_fire.assert_not_called()

    def test_single_space_press(self):
        """测试单个空格键按下"""
        with self.listener:
            time.sleep(0.1)
            self.controller.press(' ')
            self.controller.release(' ')
            time.sleep(0.1)
            self.assertEqual(self.listener.space_count, 1)

    def test_no_fire_on_short_gap(self):
        """测试短时间间隔内的空格键不会触发 on_fire"""
        with self.listener:
            time.sleep(0.1)
            
            self.controller.press(' ')
            self.controller.release(' ')
            time.sleep(0.21)
            
            self.controller.press(' ')
            self.controller.release(' ')
            time.sleep(0.21)
            
            self.controller.press(' ')
            self.controller.release(' ')
            time.sleep(0.1)

            print(f"Final space_count: {self.listener.space_count}")
            self.assertLess(self.listener.space_count, 3, "空格计数不应达到3")
            self.mock_on_fire.assert_not_called()

    def test_space_time_gap(self):
        """测试空格间隔超过0.2秒"""
        with self.listener:
            time.sleep(0.1)
            
            self.controller.press(' ')
            self.controller.release(' ')
            time.sleep(0.3)
            
            self.controller.press(' ')
            self.controller.release(' ')
            time.sleep(0.1)

            self.assertEqual(self.listener.space_count, 1)


if __name__ == '__main__':
    unittest.main()
