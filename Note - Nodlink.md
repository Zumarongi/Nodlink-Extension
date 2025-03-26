To build Provenance Graph as a Online Steiner Tree Problem

原始算法基本思路：
    贪心，对于新加入的终端节点，对之前所有节点跑一遍最短路，找到这些最短路径中的最短路

Competitive Ratio:
    在线算法与离线算法的效果之比，$O(\log(k))$

Energy of Hopset: $E = \epsilon^{\text{age}} \ast \text{HAS}(h)$作为缓存达到上限时选择替换的标准（替换最低的）

专注于进程节点（启动进程的命令行、其访问的文件、访问的IP $\Rightarrow$ 嵌入向量），使用机器学习模型检测异常
- 嵌入：command_line, file_path, ip_address$\Rightarrow$一个自然语言句子(删去一些不具有自然语义的token)$\Rightarrow$(FastText)一个数值向量
	- $V_p = w_c\ast V_c + \sum w_{f_i}\ast V_{f_i} + \sum w_{n_i}\ast V_{n_i}$
		- $w_{f_i} = \log(\frac{P}{P_{f_i}}), w_{n_i} = \log(\frac{P}{P_{n_i}})$
		- $w_c = {1\over {|\text{Files}| + |\text{IPs}|}}(\sum w_{f} + \sum w_{n})$ (?)
- VAE：生成$V_p$的重构向量$V_p'$，$\text{RE}=\text{MSELoss}(V_p, V_p')$衡量二者差异
- 结合$\text{SV}$(进程稳定性)得到进程的异常值$\text{AS}(p)=\log(\frac{\text{RE}(p)}{\text{SV}(p)})$
	- 当$\text{AS}$超过90百分位数时报为异常

Hopset构建
- 从每一个终端节点出发根据重要性评分$\text{IV}$贪心地搜索（替换了原始算法的最短路更新），直到找到$\theta$个节点
	- 重要性评分$\text{IV}(n) = \alpha^i(\beta\ast\text{AS}(n)+\gamma\ast\text{FANOUT}(n))$
		- $\text{FANOUT}(n)=\frac{\text{deg}_\text{out}}{\text{deg}_\text{in} + 1}$，以排除相对不重要的节点
		- $\beta >> \gamma$，以使异常值占主导
- 每个节点的搜索生成一个hopset，搜索过程中如果两个hopset碰头则合并
- 最后为得到的每个hopset赋一个$\text{HAS}$值：$\text{HAS}(H_i) = \sum_{n\in H_i}\text{AS}(n)$

缓存更新
- 若当前window的hopset与缓存的hopset有重合则采取合并策略
	- 通过替换$IV$小的节点，将一个终端的hopset大小始终限制在 $\theta$ 内，以防止依赖爆炸
	- 重新计算$\text{HAS}$值
- Grubbs‘ test检验离群的$\text{HAS}$值，若有离群值则触发报警

评估
- 标准：
	- 精确率$\text{precision} = \frac{\text{GTP}}{\text{GTP}+\text{GFP}}$或$\frac{\text{NTP}}{\text{NTP}+\text{NFP}}$
	- 召回率$\text{recall} = \frac{\text{GTP}}{\text{GTP}+\text{GFN}}$或$\frac{\text{NTP}}{\text{NTP}+\text{NFN}}$
	- $\text{G}$和$\text{N}$分别对应graph-level和node-level


