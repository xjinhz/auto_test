import logging

# 设置log默认级别为info
# logging.basicConfig(filename='./log/'+'log.log', \
# 	format='[%(asctime)s-%(filename)s-%(levelname)s:%(message)s]', level=logging.INFO, \
# 	filemode='a', datefmt='%Y-%m-%d %I:%M:%S %p')

# Filename：指定路径的文件。这里使用了+—name—+是将log命名为当前py的文件名
# Format：设置log的显示格式（即在文档中看到的格式）。分别是时间+当前文件名+log输出级别+输出的信息
# Level：输出的log级别，优先级比设置的级别低的将不会被输出保存到log文档中
# Filemode： log打开模式
# a：代表每次运行程序都继续写log。即不覆盖之前保存的log信息。
# w：代表每次运行程序都重新写log。即覆盖之前保存的log信息


logger = logging.getLogger()  # 不加名称设置root logger
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')

# 使用FileHandler输出到文件
fh = logging.FileHandler("./log/log.log")
fh.setLevel(logging.INFO)
fh.setFormatter(formatter)

# 使用StreamHandler输出到控制台
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(formatter)


# 添加两个Handler
logger.addHandler(ch)
logger.addHandler(fh)
