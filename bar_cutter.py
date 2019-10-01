import numpy as np
import itertools
import sys
import json
np.seterr(divide='ignore')


## Create Bar Class
class Bar:
    def __init__(self, title, dia, length, number):
        self.title = title
        self.dia = dia
        self.length = length
        self.number = number
        
    def __repr__(self):
        return self.title

### End of Bar Class

## Get Numpy Array of Bat Length from BarList
def get_bar_length_array(barList):
    arr =[]
    for x in barList:
        arr.append(x.length)
    return np.array(arr)

### Get Numpy Array of Bar_Number_Array From BarList
def get_bar_number_array(barList):
    arr =[]
    for x in barList:
        arr.append(x.number)
    return np.array(arr)

### Get All Combinations of Coefficient from BarLength and Bar_Length_Array
def get_coefficien_list(L, bar_length_array):
    bar_length_min = min(bar_length_array)
    max_iter = int(L/bar_length_min)+1
    co_efficient_list = np.arange(max_iter)

    product_arguments = [co_efficient_list]*len(bar_length_array)

    # print(product_arguments)
    return list(itertools.product(*product_arguments))


### Get the All Realstic Combination of Coefficient from BarLength and Bar_Length_Array
def get_coefficien_arr(L, bar_length_array):
    coefficien_arr = np.array(get_coefficien_list(L, bar_length_array))

    sum_arr = np.sum(coefficien_arr*bar_length_array, axis=1)
    # Remove all item which sum length = 0 or greater than L
    condition = (sum_arr == 0) | (sum_arr > L)
    condition = np.invert(condition)

    return coefficien_arr[condition]


def get_final_coefficient_array(L,bar_length_array):
    # ## Create bar_length_array and bar_number_array from batList
    # bar_length_array = get_bar_length_array(barList)
    # bar_number_array = get_bar_number_array(barList)

    ## Calculate Coefficient Array from BarList and Length
    coefficient_array = get_coefficien_arr(L,bar_length_array)

    # Create a Mask where value Greater than 1 is replace to 1
    mask = np.where(coefficient_array>0,1,0)

    # Sorting the the index According to Min Length
    index_array =np.argsort((mask*bar_length_array).max(axis=1))

    # Reverse the index Array So that it was Sort According to Max Length
    index_array = index_array[::-1]

    ## Final Coefficient Arr from the Coefficient Array
    final_coefficient_array =coefficient_array[index_array]

    ## Rearrange the final_coefficient_array
    results = []
    for i,x in enumerate(bar_length_array):
        columnIndex = len(bar_length_array)-1-i
        mask =final_coefficient_array[:,columnIndex]>0
        f=final_coefficient_array[mask]
        f_comb=f[np.argsort(L-(f*bar_length_array).sum(axis=1))]
        results.extend(f_comb)

    rearrange_coefficient_array = np.array(results)

    return rearrange_coefficient_array


def get_primary_cut(L,barList):
    ## Create bar_length_array and bar_number_array from batList
    bar_length_array = get_bar_length_array(barList)
    bar_number_array = get_bar_number_array(barList)

    final_array = get_final_coefficient_array(L,bar_length_array)
    
    final_list = []
    for comb in final_array:
        if bar_number_array.sum()==0:
                break
        cond = bar_number_array!=0
        if comb.sum()==(comb*cond).sum():
            min_arr = bar_number_array/comb
            cut = int(np.nanmin(min_arr))
            if cut !=0:
                bar_number_array = bar_number_array - comb*cut
                westage = L-(bar_length_array*comb).sum()
                result = {'cut':cut,'combination':comb,'westage_per_cut':westage,'total_westage':cut*westage,'L':L}
                final_list.append(result)

    return final_list

def get_final_list(L,barList):
    primary_list = get_primary_cut(L,barList)

    for x in primary_list:
        bars = []

        for i,comb in enumerate(x['combination']):
            if comb != 0:
                bar = barList[i]
                b={}
                b['title'] = bar.title
                b['dia'] = bar.dia
                b['length'] = bar.length
                b['factor'] = comb
                b['number_of_bars']=x['cut']*b['factor']
                bars.append(b)

        x['bars'] = bars
        del x['combination']

    return primary_list





if __name__ == '__main__':
    L = sys.argv[2]
    data = json.loads(sys.argv[1])
    # L = 12
    # print(data)
    barList = []

    for x in data:
        # print(x['title'])
        bar = Bar(x['title'],x['dia'],x['length'],x['number_of_bars'])
        barList.append(bar)

    barList.sort(key=lambda x:x.length)
    print(barList)

    # bar1 = Bar('A', 12, 1.5, 1000)
    # bar2 = Bar('B', 12, 2.5, 2000)
    # bar3 = Bar('C', 12, 4, 328)
    # bar4 = Bar('D', 12, 6.5, 450)
    # bar5 = Bar('E', 12, 7.5, 530)
    # bar6 = Bar('F', 12, 8.5, 2000)

    # barList = [bar4,bar5,bar6,bar1,bar2,bar3]

    # ## Sort the BarList According to their Length
    # barList.sort(key=lambda x:x.length)
    # print(get_final_list(L,barList))

