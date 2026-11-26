f65c713e-0f6c-4b7a-a40c-c71afeb29c51
# b4n1-公证人

证明您交付了什么以及何时交付。

b4n1-notary 将项目密封到一个 Merkle 根中并写入一个可移植的证明文件。稍后验证，或者将其交给客户端，答案是一行：已验证，或第一个不再匹配的文件。

## 为什么这很重要

版本控制记录更改的内容。它不会记录您在某一天交付的具体内容：标签可以移动，存档可以重新压缩。每个文件的默克尔根（带有时间戳）是不依赖于信任生成它的人的证据。

## 安装

- Python：pip install b4n1-notary
- JavaScript：npm install b4n1-notary
- Java：com.b4n1：b4n1-公证：0.2.0
- .NET：dotnet添加包B4n1.Notary
- Ruby：gem 安装 b4n1-notary
- PHP：作曲家需要 b4n1/b4n1-notary
- 去：去获取 github.com/B4N1-com/b4n1-notary/sdks/go

每个软件包都包含适用于 Linux、macOS 和 Windows 的预编译二进制文件。不需要编译器，也不需要安装任何其他东西。

## 你可以做什么

- 密封一棵树：标记打印文件计数、Merkle 根和证明路径。
- 稍后验证：验证重新计算根并命名任何不匹配的地方。
- 比特币中的锚点：verify-ots 使用键入的退出代码检查 OpenTimestamps 收据。
- 审计历史记录：历史记录列出了所有已密封的证据。

## 许可

SDK 包装器是商业源许可证 1.1。每个二进制文件都附带其自己的 EULA。
