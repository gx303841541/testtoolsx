代码说明：
APIs\common_APIs.py：一些公用函数，被所有代码共享
APIs\security.py：加解密模块，提供加解密函数
basic: 一些独立的功能模块（彩色打印，log，任务队列）
connection：通讯模块（socket）
protocol:
protocol\protocol_process.py：通过class communication_base实现模拟器通讯框架抽象层，定义了模拟器内部的数据处理流程
protocol\light_protocol.py：通过class SDK(communication_base)实现模拟器的私有协议层，同时也实现了communication_base定义的数据通讯方式（TCP、UDP or 串口）
protocol\light_devices.py：通过class Dev(BaseSim)实现了模拟器的应用协议层，通过加载具体设备的配置文件，实现了具体设备的接口交互消息
protocol\config: 具体设备消息配置文件，具体可参考《轻量级设备-说明文档.docx》
dev_sim.py：实例化Dev，为用户提供CLI操作
