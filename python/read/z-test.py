import scipy.stats, math, numpy

criticalValue = scipy.stats.norm.ppf(q=1-0.05/2)

print(criticalValue)

def get_z_test(oneMean, twoMean, oneLength, twoLength, oneStandardDeviation, twoStandardDeviation):
    nominator = oneMean - twoMean
    
    a = (((oneStandardDeviation**2) / oneLength) + ((twoStandardDeviation**2) / twoLength))

    denominator = math.sqrt (
        a
    )

    result = nominator / denominator
    if -criticalValue <= numpy.float64(result) <= criticalValue:
        print("Null hypothesis disproven")
    else:
        print("Null hypothesis proven")
    
    return result

reactSampleSizeTwo = 900
blazorSampleSizeTwo = 873

print(
F'''
SESSION 1

Gen. Time: {get_z_test(
    oneMean = 496463.0144, 
    twoMean = 189313.0848, 
    oneLength = reactSampleSizeTwo, 
    twoLength = blazorSampleSizeTwo,
    oneStandardDeviation = 55685.0394710555,
    twoStandardDeviation = 27833.7078789957
)}
Tree Size: {get_z_test(
    oneMean = 360071.8578, 
    twoMean = 17999.3677, 
    oneLength = reactSampleSizeTwo, 
    twoLength = blazorSampleSizeTwo,
    oneStandardDeviation = 5751612.38046917,
    twoStandardDeviation = 498883.896740049
)}
Amt spent gen.: {get_z_test(
    oneMean = 0.033333333, 
    twoMean = 0.034364261, 
    oneLength = reactSampleSizeTwo, 
    twoLength = blazorSampleSizeTwo,
    oneStandardDeviation = 0.003628872,
    twoStandardDeviation = 0.004905856
)}
''')

reactSampleSizeOne = 900
blazorSampleSizeOne = 889

print(
F'''
>>The big Z-Test<<

SESSION 2

Gen. Time: {get_z_test (
    oneMean = 305557.7878,
    twoMean = 121891.2936, 
    oneLength = reactSampleSizeOne, 
    twoLength = blazorSampleSizeOne,
    oneStandardDeviation = 61633.00045,
    twoStandardDeviation = 31244.52579
)}
Tree Size: {get_z_test (
    oneMean = 274851.04, 
    twoMean = 27307.83352, 
    oneLength = reactSampleSizeOne, 
    twoLength = blazorSampleSizeOne,
    oneStandardDeviation = 3365782.106,
    twoStandardDeviation = 363692.795893533
)}
Amt spent gen.: {get_z_test (
    oneMean = 0.033333333, 
    twoMean = 0.33745782, 
    oneLength = reactSampleSizeOne, 
    twoLength = blazorSampleSizeOne,
    oneStandardDeviation = 0.00670156,
    twoStandardDeviation = 0.00861693740459966
)}

''')

reactSampleSizeThree = 900
blazorSampleSizeThree = 930

print(
F'''
SESSION 3

Gen. Time: {get_z_test(
    oneMean = 124339.0278, 
    twoMean = 63010.23656, 
    oneLength = reactSampleSizeThree, 
    twoLength = blazorSampleSizeThree,
    oneStandardDeviation = 55304.5320223349,
    twoStandardDeviation = 22084.2602836391
)}
Tree Size: {get_z_test(
    oneMean = 214854.5733, 
    twoMean = 28712.32688, 
    oneLength = reactSampleSizeThree, 
    twoLength = blazorSampleSizeThree,
    oneStandardDeviation = 1674383.33185898,
    twoStandardDeviation = 272603.585289381
)}
Amt spent gen.: {get_z_test(
    oneMean = 0.033333333, 
    twoMean = 0.032258065, 
    oneLength = reactSampleSizeThree, 
    twoLength = blazorSampleSizeThree,
    oneStandardDeviation = 0.0147979638583837,
    twoStandardDeviation = 0.0112774714136609
)}

''')