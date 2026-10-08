# 周翔的 mini-Scheme 作答

学号：3250102669。使用 Python 3 标准库，无第三方依赖。

## 运行

在本目录中：

```text
python src/main.py example/01_arithmetic.scm
python autograder.pyz python src/main.py
python tests/run_tests.py
```

入口支持标准输入和多个文件；多个文件共享全局环境。

## 模块

- src/model.py：符号、点对、空表、闭包、环境与相等语义。
- src/reader.py：注释、字符串转义、词法及嵌套表达式读取。
- src/printer.py：值的规范输出。
- src/primitives.py：算术、比较、列表、类型谓词与输出内置函数。
- src/evaluator.py：特殊形式、求值与过程调用。
- src/main.py：文件与标准输入入口、结果输出及错误报告。

## 关键语义

只有 #f 为假；0 和空表都为真。if、cond、and、or 按规定控制求值顺序。
lambda 捕获定义时的环境；调用时创建参数环境，因此支持词法作用域、闭包和递归。
let 的所有右侧先在外层环境求值，然后一次性建立局部环境。
整数商向零截断，使用整数运算避免大整数转浮点失去精度。
quote 和 cons 使用同一套点对表示；eq? 对复合值比较对象身份，equal? 比较结构。
布尔值与整数、符号与字符串分别处理，避免 Python 的类型相等陷阱。

## 实际验证

2026-10-07：官方验收 12/12 通过；自编语义边界用例、多文件共享环境、标准输入通过。
测试输出见 verification.txt；tests/ 提供可重复运行的边界测试。
隐藏用例未提供，因此不宣称隐藏测试全部通过。未实现规格排除的宏、set! 或尾调用优化保证。

## AI 使用

使用 Codex 读取 README.md 和 spec.md，编写模块、运行官方验收、补充边界测试并整理说明。
按规格核对短路、闭包、let 并行绑定、整数除法、相等与打印规则；修复过 let 的过度限制。
这次没有创建个人 GitHub 远程仓库，按题目允许的源码 ZIP 方式提交。学习者应阅读并能解释最终代码。

原始题目来源：https://github.com/woo114515/minischeme-starter
