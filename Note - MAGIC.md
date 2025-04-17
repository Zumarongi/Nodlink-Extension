Graph MAE（图掩码自动编码器）[GraphMAE: Self-Supervised Masked Graph Autoencoders | Proceedings of the 28th ACM SIGKDD Conference on Knowledge Discovery and Data Mining](https://dl.acm.org/doi/abs/10.1145/3534678.3539321)

- 无监督的APT检测
	- 检测APT存在性
	- 定位攻击实体
- 也可半监督和全监督
- 可选的模型适应机制（用户反馈通道）

攻击实例：Pine后门配合Drakon Dropper
- 攻击者构建了一个恶意可执行文件（/tmp/tcexec），并通过钓鱼邮件将其发送至目标主机。其目的是执行端口扫描以进行内部侦察，并在目标主机与攻击者之间建立一个静默连接。

Breakthrough:
- 完全自监督的异常检测方式
- 利用图表示模块（Graph representation module）对溯源图深层图特征提取→高质量嵌入
- Graph MAE→极大减小性能开销
- 通用性，多种场景下进行多粒度检测，适用于多来源的审计日志

MAGIC执行两个阶段两种粒度的检测：
- 批量日志级别的检测：对同一来源的日志检测APT存在性
- 系统实体级别的检测：精确定位恶意实体

四个主要组件：
- 溯源图构建（4.1 Provenance Graph Construction）
	- 日志解析
		- 放弃了时间戳信息
	- 初始嵌入
	- 噪声减少
		- 合并之后放弃边的统计信息
			- 第一步，每种类型只保留一条边
			- 第二步，进一步只保留均值
- 图表示模块（4.2 Graph Representation Module）
	- 特征掩码
		- 训练时随机选择一些节点进行掩码，用掩码值代替初始嵌入值
	- 图编码器
		- 图注意力网络（GAT）：衡量邻居的重要性
			- $\text{MSG}(src, dst) = W_{msg}(h_{src} \,||\, \text{emb}_e)$，其中 $h_{\text{src}}$ 是源节点的嵌入，$\text{emb}_e$ 是边的初始嵌入，$||$ 表示向量拼接，$W_{\text{msg}}$ 是可训练的线性变换矩阵。
			- 计算注意力系数 $a$ 
				- $\alpha(\text{src}, \text{dst}) = \text{LeakyReLU}(W^T_{\text{as}} h_{\text{src}} + W_{\text{am}} \cdot \text{MSG(src, dst)})$
				- $a(\text{src}, \text{dst}) = \text{Softmax}(\alpha(\text{src}, \text{dst}))$
			- 从节点入边聚合消息（加权求和更新节点嵌入值 $h_n$，$n$ 为层数）：
				- $\text{AGG}(h_{\text{dst}}, h_{\mathcal{N}}) = W_{\text{self}} h_{\text{dst}} + \sum_{i \in \mathcal{N}} a(i, \text{dst}) \cdot \text{MSG}(i, \text{dst})$
				- $h_n^l = \text{AGG}^l(h_n^{l-1}, h_{\mathcal{N}_n}^{l-1})$
			- 最后生成**节点嵌入**和**系统状态嵌入**（所有节点嵌入的平均值）
			- Note:
				- [GAN(THU)](https://mp.weixin.qq.com/s?__biz=MzI1MjQ2OTQ3Ng==&mid=2247610252&idx=1&sn=ecaf6dec0ec25d3443aff1dcff5bf3f0&chksm=e9e02607de97af11e4e5b4a58df387663c375f170d74fe365288de1998a0876988d857036aba&scene=27) [GAT](https://zhuanlan.zhihu.com/p/25307420715)
				- [Leaky ReLU](https://blog.csdn.net/IT_ORACLE/article/details/145804855)
				- 
	- 图解码器
		- 构建了一个用于优化图表示模块的目标函数
			- $x_n^\ast = AGG^\ast(h_n^\ast, h_{\mathcal{N}_n}^\ast)$
			- $\mathcal{L}_{fr} = \frac{1}{|\tilde{N}|} \sum_{n_i \in \tilde{N}} \left(1 - \frac{x_{n_i}^T x_{n_i}^\ast}{\|x_{n_i}\| \cdot \|x_{n_i}^\ast\|} \right)^\gamma$ 缩放余弦损失，$\gamma$ 为超参数
		- 随机采样负样本（在非掩码节点间进行），用两层MLP预测样本对是否有边
			- $\text{prob}(n,n')=\sigma(\text{MLP}(h_n || h_{n'}))$
		- 采用二元交叉熵损失
			- $\mathcal{L}_{sr} = -\frac{1}{|\hat{N}|} \sum_{n \in \hat{N}} \left[ \log(1 - \text{prob}(n, n^-)) + \log(\text{prob}(n, n^+)) \right]$
		- 自监督训练目标
			- $\mathcal{L} = \mathcal{L_{fr}} + \mathcal{L_sr}$
- 异常检测模块：在仅已知良性系统行为的前提下，识别出恶意的系统实体或系统状态——寻找离群点
	- 从训练中的良性嵌入构建一个K-D tree
	- 检测：
		- KNN ($\log(N)$ 复杂度)
		- 相似性标准（Euclid距离 $dist_x$）
		- 异常分数 $score$ 超过阈值 $\theta$ 则判定为异常
			- $score_x=\frac{dist_x}{{\over dist_x}}$
	- 前文提到的两种粒度即在这里体现：
		- 系统状态级别则采用图嵌入 $h_G$
		- 系统实体级别则采用实体嵌入 $h_n$
- 模型适应机制：应对“概念漂移”（对良性但先前未见过的行为会产生误报）
	- 安全人员识别出误报，然后模型从中学习
	- 图表示模块自监督，不依赖数据标签，从而有自适应新样本的能力
	- 检测模块
		- 折扣机制：类似于缓存机制LRU，使得记忆的良性嵌入保持最新状态

Implementation:
- 日志解析（支持多日志来源）：
	- StreamSpot
	- Camflow
	- CDM
- 图处理：
	- NetworkX
- 图存储：
	- Json
- 模型：
	- 图表示模块：
		- PyTorch & DGL
	- 异常检测：
		- sklearn
- 超参数设置
	- 特征重建损失缩放因子：$\gamma = 3$ 
    - k 近邻数量：$k = 10$
    - 学习率：$0.001$
    - 权重衰减：$5\times 10^{-4}$
    - 图编码层数：$3$ 层
    - 掩码率：$0.5$
    - 输出维度 $d$：
        - 批量日志级：$d = 256$
        - 系统实体级：$d = 64$（为节省资源）
	- 检测阈值 $\theta$：通过线性搜索方式在每个数据集上单独确定。
	    - 批量日志级： $\theta \in [1, 10]$
	    - 系统实体级（有点复杂）

Evaluation:
- Dataset
	- DARPA TC E3
	- StreamSpot
	- Unicorn Wget
- Baseline
	- ShadeWatcher
