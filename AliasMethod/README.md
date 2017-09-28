从离散分布中随机抽样的快速算法

参考原文：https://hips.seas.harvard.edu/blog/2013/03/03/the-alias-method-efficient-sampling-with-many-discrete-outcomes/

本实验评测了 Alias Method 与 numpy.random.multinomial 的性能和效果，结论是 Alias method 在高维数据采样下，效果和性能都超过 numpy 的默认函数。
