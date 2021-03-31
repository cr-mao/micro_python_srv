# 变量定义
include config.mk

default:  install

common:
	@echo
	@echo "==== micro_python_srv develop environment ===="
	@echo "virtualenv location: $(VENV)"
	@echo "virtualenv python: $(VENV_PYTHON)"
	@echo


# 运行服务端
serve: common
	$(VENV_PYTHON) scripts/serve.py


# 别名，留在这里支持老的用法
install: pip

# 安装pip依赖
pip: common $(VENV)
	$(VENV_PYTHON) -m pip install -U pip
	$(VENV_PYTHON) -m pip install -r requirements.txt $(PIP_EXTRA_OPTIONS)

# 建立venv环境
$(VENV):
	$(PYTHON) -m venv $(VENV)

codegen:
	sh scripts/codegen.sh