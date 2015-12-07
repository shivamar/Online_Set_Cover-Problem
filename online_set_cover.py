import random
from random import shuffle
import math
import copy

def generate_subsets(array,n):
    if n == -1:
        return [[]]
    else:
        subsets = generate_subsets(array,n-1)
        new_subsets = list(subsets)
        for s in list(subsets):
            s= list(s)
            s.append(array[n])
            new_subsets.append(s)
    return new_subsets

def get_all_subsets(n):
    input_set = [x for x in range(1,n+1)]
    return generate_subsets( input_set,len(input_set)-1)

def get_sample_subsets(subsets,n,probability):
    sample_subsets = []
    for s in subsets:
        if len(s)==0 or len(s)>=n-1:
            continue
        elif random.random() < probability:
            sample_subsets.append(s)
    return sample_subsets

def get_elements_from_subsets(subsets):
    elements = set()
    for subset in subsets:
        for element in subset:
            elements.add(element)
    return [x for x in elements]

def initialize_weights_new(sample_subsets):
    xs = len(sample_subsets)
    h={}
    for s in sample_subsets:
        h[s] =  1.0/(2*len(sample_subsets))
    return h;

def is_element_present_in_subsets(subsets,element):
    for s in subsets:
        if element in s:
            return True
    return False

def increase_weight_of_the_sets_containing_element(sets,element,alpha):
    for s,cost in sets.items():
        if element in s:
            sets[s] *=alpha
    return sets

def choose_element_with_minimum_cost(sets,element):
    MAX_INT = 10**20
    mincost = MAX_INT
    choosen_set = None;
    
    for s,cost in sets.items():        
        if element in s:
            #print element,s
            if sets[s]< mincost :
                mincost = sets[s]
                choosen_set = s
    return choosen_set  

def convertToTuple(sets):
    tuple_ = []
    for item in sets:
        t = tuple(item)
        tuple_.append(t)    
    tuple_ = tuple(tuple_)
    return tuple_

#calculate wj for a given element 
def cal_wj(sets, element):
    wj=0
    for each_set,cost in sets.items():
        if element in each_set:
            wj+=cost
    return wj

#calculate k for wj such that 1 < 2^k * wj < 2
def findK(wj):
    k=0
    multplying_factor=1
    while(wj < 1):
        k+=1
        multplying_factor*=2
        wj=wj*multplying_factor
    
    return k

# augemnts weight and returns the modified tuples which contributed to weight augmentation
def weight_augment(sets, element, k):
    modified_list=[]
    for set_tuple, cost in sets.items():
        if element in set_tuple:
            sets[set_tuple] = sets[set_tuple] * math.pow(2,k)
            modified_list.append(set_tuple)      
    modified_list = tuple(modified_list)
    return modified_list
    
# remove atmost 4logn modified tuples from sample subsets and add to final_subsets 
# such that potential function value is below potential function value before augmentation
def addAtmost4LogNSets(final_subset, sample_subsets, modified_tuples, max_num_additions, new_wj, wj, updated_phi_vector, phi_vector,input_set):

#limit max_num_additions to final_subset
#check if sum(updated_phi) > sum(phi)
#randomly select a modified tuple and add to final Set
#for each element in modified tuple check if it is in input_set, if yes remove it and 
#update the phi vector by removing that entry
#remove it from sample_subsets
    for x in range(max_num_additions):
        if x < len(modified_tuples):
            phi_e = sum(updated_phi_vector.values())
            phi_o = sum(phi_vector.values())
            
            if phi_e > phi_o:     
                tup = tuple(modified_tuples[x])
                final_subset.append(tup)
                del sample_subsets[tup]
                
                for element in tup:
                    if element in input_set:
                        input_set.remove(element)
                        del updated_phi_vector[element]                        
                        
    return final_subset,updated_phi_vector,input_set,sample_subsets

#potential function vector returns the 
#elements which are not covered yet and their wj 
def potential_function(sample_subsets,input_set):
    phi_vector = {}
    for element in input_set:
        wj = cal_wj(sample_subsets, element)
        phi_vector[element] = wj
        
    return phi_vector

def online_set_cover_problem(n):
    input_set = [x for x in range(1,n+1)]
    
    print("input set")
    print(input_set)
    print()
            
    all_subsets = get_all_subsets(n)
    sample_subsets = get_sample_subsets(all_subsets,n,0.25);
    adversary_set = get_elements_from_subsets(sample_subsets)
    
    print('Subsets')
    print(sample_subsets)
    
    print
    sample_subsets = convertToTuple(sample_subsets)
    sample_subsets = initialize_weights_new(sample_subsets)    
    
    phi_vector = potential_function(sample_subsets, input_set)
    updated_phi_vector = potential_function(sample_subsets, input_set)
    
    #print adversary_set;
    shuffle(adversary_set)
    
    print('Adversary sequence')
    print(adversary_set)
    print
    
    final_subsets = []
    final_cost = 0
    
    for a in adversary_set:
        wj = cal_wj(sample_subsets, a) 
        
        if wj < 1 and a in input_set:    
            k=findK(wj)
            modified_tuples = weight_augment(sample_subsets,a,k)        
            
            updated_phi_vector = potential_function(sample_subsets,input_set)
            # remove 4logN 
            max_no = 4 * math.log(n,2)
            final_subset,updated_phi_vector,input_set,sample_subsets = addAtmost4LogNSets(final_subsets, sample_subsets, modified_tuples, math.floor(max_no),wj * math.pow(2,k),wj,updated_phi_vector, phi_vector,input_set)              
            phi_vector = copy.deepcopy(updated_phi_vector)
            
    print('\nfinal subsets')
    print(final_subsets)
    
online_set_cover_problem(8);
