'''
HMM 假设：任意时刻t的状态只依赖于其前一时刻的状态（齐次马尔科夫性假设）；任一时刻的观测值只依赖于该时刻的马尔科夫链的状态（观测独立性假设）
3 quetions：
    概率计算问题：给定模型λ和观测序列O，计算在该模型下该观测序列出现的概率P(O|λ)
    学习问题：已知观测序列O，估计模型λ的参数，使得在该模型下该观测序列的概率最大（即用极大似然估计的方法估计参数）
    预测问题（解码问题）：已知模型λ和观测序列O，求对给定观测序列条件概率P(I|O)最大的状态序列（即给定观测序列，求最有可能的对应的状态序列）
'''

import numpy as np

# 概率计算问题

A = np.matrix('0.5 0.2 0.3; 0.3 0.5 0.2; 0.2 0.3 0.5').A
B = np.matrix('0.5 0.5; 0.4 0.6; 0.7 0.3').A
PI = np.array([0.2, 0.4, 0.4]).T
Q = set([1, 2, 3])
O = [0, 1, 0, 0, 1, 1]

# 直接计算：罗列出所有可能的状态序列，复杂度为(N^T);某个状态序列产生该输出，复杂度为T.总复杂度为（TN^T）,不可行

# 前向算法:递推计算，直接引用前面的计算结果，避免重复计算，复杂度为(TN^2)
def forward(A, B, PI, Q, O):
	alpha = np.multiply(PI, B[:, O[0]])	# 初值

	def forward_(alpha, t, T, N):	# 递推计算: t-需要计算的时刻t T-最后时刻t N-状态个数
		if t > T:
			return alpha
		alpha_new = np.zeros(N)
		for k in range(N):
			p = 0
			for l in range(N):
				p += alpha[l] * A[l, k]
			alpha_new[k] = p * B[k, O[t]]
		return forward_(alpha_new, t+1, T, N)

	alpha_NT = forward_(alpha, 1, len(O)-1, len(Q))

	prob = alpha_NT.sum()
	return prob

print('forward algorithm: the probability is ', forward(A, B, PI, Q, O))

# 后向算法
def backward(A, B, PI, Q, O):
	beta = np.ones(len(Q))

	def backward_(beta, t, N):
		if t < 1:
			return beta
		beta_ = np.zeros(N)
		for i in range(N):
			p = 0
			for k in range(N):
				p += A[i, k] * B[k, O[t]] * beta[k]
			beta_[i] = p
		return backward_(beta_, t-1, N)

	beta = backward_(beta, len(O)-1, len(Q))

	prob = np.multiply(np.multiply(PI, B[:, O[0]]), beta).sum()
	return prob

print('backward algorithm: the probability is ', backward(A, B, PI, Q, O))



# 学习算法

O = [['A', 'B', 'A', 'C', 'C'], ['B', 'A', 'B', 'A', 'C'], ['C', 'B', 'A', 'B', 'A'], ['A', 'C', 'C', 'A', 'B'], ['C', 'A', 'B', 'A', 'C']]
I = [['a', 'b', 'a', 'b', 'b'], ['b', 'a', 'b', 'a', 'a'], ['a', 'b', 'a', 'b', 'a'], ['a', 'a', 'a', 'a', 'b'], ['a', 'a', 'b', 'a', 'a']]
I_set = ['a', 'b']
O_set = ['A', 'B', 'C']

# 监督学习法：利用极大似然估计法估计参数
def supervised(O, I, N, M, O_set, I_set):

	def getMatchNum(a, b, l):
		i = 0
		for k in range(len(l) - 1):
			if l[k] == a and l[k+1] == b:
				i += 1
		return i

	A = np.zeros((N, N))
	for i in range(N):
		for j in range(N):
			k = 0
			for l in I:
				k += getMatchNum(I_set[i], I_set[j], l)
			A[i, j] = k
	A = A / A.sum()

	B = np.zeros((N, M))
	for i in range(N):
		for j in range(M):
			p = 0
			for k in range(len(I)):
				for l in range(len(I[k])):
					if I[k][l] == I_set[i] and O[k][l] == O_set[j]:
						p += 1
			B[i, j] = p
	print(B)
	B = B / B.sum()

	PI = np.zeros(N)
	for i in range(N):
		p = 0
		for l in I:
			if l[0] == I_set[i]:
				p += 1
		PI[i] = p
	PI = PI / PI.sum()

	return A, B, PI

print('supervised learning: ', supervised(O, I, 2, 3, O_set, I_set))


# 非监督算法：Baum-Welch(EM)


































