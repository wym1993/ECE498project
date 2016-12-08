#!/usr/bin/python
# -*- coding: utf-8 -*-
import random
import numpy as np
import networkx as nx
import math

def run(graph):
	chromlength = nx.number_of_nodes(graph);
	node=[]
	for no in graph.nodes():
		node.append(no);

	pc = 0.6;
	pm = 0.001;
	iteration = 50;	
	maxSize = 200
	if math.factorial(chromlength-2)>maxSize:
		popsize = maxSize;
	else:
		popsize = math.factorial(chromlength-2)
	pop = generatePop(node, chromlength, popsize);
	result = [0,0]
	if popsize==1:
		return pop[0];
	for i in range(iteration): #繁殖50代
		allSame = True;
		for j in range(1,popsize):
			if pop[j]!=pop[0]:
				allSame = False;
				break;
		if allSame:
			return result[1]

		fitvalue = calcfitvalue(graph, pop, popsize, chromlength) #计算目标函数值
		[bestindividual, bestfit] = best(pop, fitvalue, popsize) #选出最好的个体和最好的函数值
		if bestfit>result[0]:
			result = [bestfit,bestindividual];
		pop = selection(pop, fitvalue, popsize) #自然选择，淘汰掉一部分适应性低的个体
		pop = crossover(pop, pc, popsize, chromlength) #交叉繁殖
		pop = mutation(pop, pm, popsize, chromlength) #基因突变
	return result[1];

def generatePop(node,chromlength, popsize):
    pop=[]
    a=node
    a.remove(0);
    a.remove(189);
    i = 0;
    while i< popsize:
        ind = random.sample(a,len(a))
        if not ind in pop:
        	pop.append(ind);
        	i+=1;

    for j in range(popsize):
        pop[j].insert(0,0)
        pop[j].append(189)
    return pop;

def mutation(pop, pm, popsize, chromlength):
	for i in range(popsize):
		if random.random() < pm:
			temp1 = random.randint(1,chromlength-2);
			temp2 = random.randint(1,chromlength-2);
			pop[i][temp1], pop[i][temp2] = pop[i][temp2], pop[i][temp1];

	return pop;

def crossover(pop, pc, popsize, chromlength):
	for i in range(popsize):
		temp = [];
		cpoint = random.randint(0,chromlength);
		temp.extend(pop[i][cpoint : len(pop[i])]);
		temp.extend(pop[i][0:cpoint]);
	return pop;

def selection(pop, fitvalue, poplen): #自然选择（轮盘赌算法）
	newfitvalue = []
	totalfit = sum(fitvalue)
	for i in range(len(fitvalue)):
		newfitvalue.append(fitvalue[i] / totalfit)
	newfitvalue = np.cumsum(newfitvalue)
	ms = [];
	for i in range(poplen):
		ms.append(random.random()) #random float list ms
	ms.sort()
	fitin = 0
	newin = 0
	newpop = pop
	while newin < poplen :
		if(ms[newin] < newfitvalue[fitin]):
			newpop[newin] = pop[fitin]
			newin = newin + 1
		else:
			fitin = fitin + 1
	return newpop

def calcfitvalue(graph, pop, popsize, chromlength):
	fitvalue = [];
	for i in range(popsize):
		dis = 0;
		for j in range(0,chromlength-1):
			dis+=graph[pop[i][j]][pop[i][j+1]]['distance'];
		fitvalue.append(dis);
	for i in range(popsize):
		ReapDis = checkRepeat(graph, pop[i]);
		fitvalue[i] = 1/(fitvalue[i]*1.0+ReapDis);
	return fitvalue;

def checkRepeat(graph, chrom):
	path = [];
	point = len(chrom)-2;
	for j in range(0,len(chrom)-1):
		pa = graph[chrom[j]][chrom[j+1]]['path'];
		for p in pa:
			path.append(p);

	newPath = list(set(path));
	return int(len(path)-len(newPath)-point);

def best(pop, fitvalue, popsize): 
	bestindividual = pop[0];
	bestfit = fitvalue[0]
	for i in range(1,popsize):
		if fitvalue[i] > bestfit:
			bestfit = fitvalue[i]
			bestindividual = pop[i]
	return [bestindividual, bestfit]
