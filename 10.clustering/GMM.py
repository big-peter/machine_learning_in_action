import numpy as np


"""
Gaussian Mixture Model, refer to http://www.cnblogs.com/lyrichu/p/7814651.html
"""
def generateData(k, mu, sigma, dataNum):
    dataArray = np.zeros(dataNum, dtype=np.float32)
    n = len(k)
    for i in range(dataNum):
        rand = np.random.random()
        Sum = 0
        index = 0
        while (index < n):
            Sum += k[index]
            if (rand < Sum):
                dataArray[i] = np.random.normal(mu[index], sigma[index])
                break
            else:
                index += 1
    return dataArray


def normPdf(x, mu, sigma):
    return (1./np.sqrt(2*np.pi))*(np.exp(-(x-mu)**2/(2*sigma**2)))


def em(alpha, mu, sigma, data, step=10):
    k = len(alpha)
    dataSize = data.shape[0]
    gama = np.zeros([k, dataSize])
    for s in range(step):
        for i in range(k):
            for j in range(dataSize):
                currentCompent = alpha[i] * normPdf(data[j], mu[i], sigma[i])
                compentSum = sum([alpha[t] * normPdf(data[j], mu[t], sigma[t]) for t in range(k)])
                gama[i, j] = currentCompent / compentSum
        for i in range(k):
            mu[i] = sum(gama[i, :] * data) / sum(gama[i, :])
        for i in range(k):
            sigma[i] = np.sqrt(sum(gama[i, :] * (data - mu[i]) ** 2) / sum(gama[i, :]))
        for i in range(k):
            alpha[i] = sum(gama[i, :]) / dataSize
    return alpha, mu, sigma


if __name__ == '__main__':
    k = [0.35,0.15,0.05, 0.45]
    mu = [1,2,4,3]
    sigma = [1,2,1,3]
    dataNum = 5000
    dataArray = generateData(k,mu,sigma,dataNum)
    # 注意em算法对于参数的初始值是十分敏感的
    k0 = [0.35,0.15,0.45, 0.05]
    mu0 = [2,2,2,2]
    sigma0 = [1,1,1,1]
    step = 6
    k1,mu1,sigma1 = em(k0,mu0,sigma0,dataArray,step)
    print("参数实际值:")
    print("k:",k)
    print("mu:",mu)
    print("sigma:",sigma)
    print("参数估计值:")
    print("k1:",k1)
    print("mu1:",mu1)
    print("sigma1:",sigma1)
