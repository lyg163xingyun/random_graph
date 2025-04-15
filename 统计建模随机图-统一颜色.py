import networkx as nx
import random
import matplotlib.pyplot as plt
import numpy as np
import os
import pickle

# 设置随机种子以确保结果可重复
random_seed =40 # 你可以选择任何整数作为种子
random.seed(random_seed)
np.random.seed(random_seed)

# 创建图
G = nx.Graph()

# 添加100个节点
G.add_nodes_from(range(1, 101))

# 确保每个节点至少有一个边
edges = set()
nodes_list = list(G.nodes())  # 将节点视图转换为列表

# 为每个节点至少添加一条边
for node in nodes_list:
    other_nodes = [n for n in nodes_list if n != node]
    if other_nodes:
        connected_node = random.choice(other_nodes)
        edges.add((node, connected_node))

# 生成额外的边，使总边数达到150
while len(edges) < 150:
    u, v = random.sample(nodes_list, 2)  # 从列表中随机选择两个节点
    if not G.has_edge(u, v):
        edges.add((u, v))

G.add_edges_from(edges)

# 输出图的信息
print(f'Number of nodes: {G.number_of_nodes()}')
print(f'Number of edges: {G.number_of_edges()}')

# 打印边（不带括号）
print('Edges:')
for edge in G.edges():
    print(f'{edge[0]} {edge[1]}')

# 确保目标文件夹存在
output_dir = r'D:\统计建模数据'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 保存图的边到文件
with open(os.path.join(output_dir, '统计建模随机图-统一颜色.txt'), 'w') as f:
    # 文件头部，包含节点数和边数
    f.write(f'p edge {G.number_of_nodes()} {G.number_of_edges()}\n')

    # 写入边（每条边前缀为 `e`）
    for edge in G.edges():
        f.write(f'e {edge[0]} {edge[1]}\n')

# 绘制图形
plt.figure(figsize=(16, 12))  # 设置图形大小
# plt.title('Random Graph Visualization', fontsize=18)  # 设置标题
plt.axis('off')  # 关闭坐标轴

# 使用 spring_layout 布局，增加 k 值以增加节点间距
pos = nx.spring_layout(G, k=0.2, iterations=50)

# 保存节点布局位置到文件
with open(os.path.join(output_dir, 'node_layout.pkl'), 'wb') as f:
    pickle.dump(pos, f)

# 绘制节点
node_sizes = [300] * len(G.nodes())  # 设置节点大小
# 将所有节点颜色设置为红色
nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color='green', alpha=0.8)

# 绘制边
edge_colors = plt.cm.Blues(np.linspace(0.2, 0.8, len(G.edges())))  # 使用颜色映射
# nx.draw_networkx_edges(G, pos, width=0.8, alpha=0.6, edge_color=edge_colors)
nx.draw_networkx_edges(G, pos, width=0.8, alpha=0.6, edge_color='black')

# 绘制节点标签
nx.draw_networkx_labels(G, pos, font_size=10, font_color='black', font_weight='bold')

# 调整边框和背景
plt.tight_layout()
plt.gca().set_facecolor('#f8f8f8')  # 设置背景颜色

# 显示图形
plt.show()