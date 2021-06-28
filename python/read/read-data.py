import json, glob, os, math, statistics, xlsxwriter, datetime, scipy.stats as pystats
import components.devToolUtilities as dtu

FUNCTION_NAME = "TimerFire"

IGNORE_INITIALISER_FUNCTION_NAMES = [
    "_mono_set_timeout"
]
# Used to filter out Blazor initialise call and get a comparable sample
# So it will ignore anything with the duration below this value
TIMER_FIRE_IGNORE_MAX_MICROSECONDS = 1000

# Keep this one the same as experiment application
PARAMETER_EXPERIMENT_TOTAL_TIME_SECONDS = 30
# To catch the heap allocation events that occurs after JS is done
PARAMETER_TS_HEAP_EVENT_MARGIN_MICROSECONDS = 10
# X Phase type, used in trace format to identify complete events.
COMPLETE_EVENT_TYPE = 'X'

#CSV / XLSX Headers
HEADER_GENERATION_TIME = "generation_time (μs)"
HEADER_TREE_SIZE_MEMORY = "tree_size (bytes)"
# PU = Procent usage
HEADER_PU_USAGE = "pu_usage (loading precentage of experiment time)"

HEADER_PU_SD = "pu_standard_deviation"
HEADER_TREE_SIZE_SD = "tree_size_standard_deviation"
HEADER_GENERATION_TIME_SD = "generation_time_standard_deviation"

COLUMN_INDEX_DICTIONARY = {
    # COLLECTED VALUES
    HEADER_GENERATION_TIME: 0,
    HEADER_TREE_SIZE_MEMORY: 1,
    HEADER_PU_USAGE: 2,
    # STANDARD DEVIATION
    HEADER_GENERATION_TIME_SD: 3,
    HEADER_TREE_SIZE_SD: 4,
    HEADER_PU_SD: 5
}

def get_list_from_tuple_column(tupleList, tupleIndex):
    return [tupleItem[tupleIndex] for tupleItem in tupleList]

# Standard deviation for a sample
def get_standard_deviation(sampleList):
    print("Sample list from stdr dev: ", sampleList)
    n = len(sampleList)
    # sum(X^2) - sum(X)^2 => x - y    
    x = 0
    y = 0

    for value in sampleList:
        x += value**2
        y += value

    y = y**2
    # Returns standard deviation
    return math.sqrt((n * x - y) / (n*(n - 1)))

def last(n):
    return n[len(n) - 1]

# Retrieves and returns a list of lists [Generation time, heap difference during period, generation / totalTime procentage of total run]
def get_data_tuple_list(file):
    returningDataList = []
    usedHeapTimelineList = []

    jsonParsedObject = json.loads(file)

    for index, heapCall in enumerate(jsonParsedObject):
        try:
            usedHeapMemory = heapCall['args']['data']['jsHeapSizeUsed']
            usedHeapTimelineList.append((usedHeapMemory, heapCall['ts']))
            if index == 0:
                # Set initial heap usage to emulate how DevTools visualises start usage
                usedHeapTimelineList.append((usedHeapMemory, 0))
        except KeyError:
            # Could not find right format, instead of crashing just continue the search
            continue
    usedHeapTimelineList.sort(key=last)

    total_generation_time_microseconds = 0

    lastAllocatedHeapAmount = usedHeapTimelineList[0][0]
    for functionCall in jsonParsedObject:
        functionName = str()
        functionType = str()
        
        # Validate, if fails then look at the next
        try:
            functionName = functionCall['name']
            functionType = functionCall['ph']
        except KeyError:
            continue

        if functionName == FUNCTION_NAME and functionType == COMPLETE_EVENT_TYPE:
            # Google DevTools, "profiles with sampling rate of 1000 samples/seconds = 1 sample/millisecond"
            # But timestamps are stored in microseconds due to the value being retrieved from the CPU clock.
            
            # Ignore any TimerFired called by function in ignore list
            ignoreThisFunctionCall = False
            for stack in dtu.get_stack_trace_by_timer_id(functionCall['args']['data']['timerId'], jsonParsedObject):
                if stack['functionName'] in IGNORE_INITIALISER_FUNCTION_NAMES:
                    ignoreThisFunctionCall = True
                    break
            
            if ignoreThisFunctionCall:
                continue
            
            functionCallDuration = 0
            try:
                functionCallDuration = functionCall['dur']
            except KeyError:
                functionCallDuration = functionCall['tdur']
            
            # Ignores anything smaller than constant. 
            # This is specifically for Blazor since it invokes TimerFire for a few microseconds before the real task is done.
            if functionCallDuration <= TIMER_FIRE_IGNORE_MAX_MICROSECONDS:
                continue

            total_generation_time_microseconds += functionCallDuration

            heapUsageAndAllocationTimeList = [heapTuple for heapTuple in usedHeapTimelineList if heapTuple[1] >= functionCall['ts'] and heapTuple[1] <= functionCall['ts'] + functionCallDuration + PARAMETER_TS_HEAP_EVENT_MARGIN_MICROSECONDS]
            
            print("Heapusage and heap time: ", heapUsageAndAllocationTimeList)
            if len(heapUsageAndAllocationTimeList) > 0:
                memoryDifference = last(heapUsageAndAllocationTimeList)[0] - lastAllocatedHeapAmount
                lastAllocatedHeapAmount = last(heapUsageAndAllocationTimeList)[0]
            else:
                memoryDifference = 0

            returningDataList.append (
                [functionCallDuration, memoryDifference, 0] # Generation time procentage is set after this loop, don't worry 😊
            )
    print("Sum of all generation times: " ,total_generation_time_microseconds)
    for dataTuple in returningDataList:
        dataTuple[2] = dataTuple[0] / total_generation_time_microseconds
    return returningDataList

def get_formated_sample_from_files(directoryName):
    os.chdir("./{directory}".format(directory=directoryName))
    totalSample = list()
    for file in glob.glob("*.json"):
        print("\n\n---OPENING {fileName}\n".format(fileName = file))
        totalSample += get_data_tuple_list(open(file, 'r').read())

    print(totalSample)
    # Redirects to src folder so it can analyse another folder
    os.chdir("..")
    return totalSample

def generate_xlsx_from_sample(sampleList, prefixName="gen"):
    try:
        os.chdir("./output")
    except FileNotFoundError:
        os.mkdir("output")
        os.chdir("./output")
    
    sampleWorkbook = xlsxwriter.Workbook("{prefix}-{name}-output.xlsx".format(
        name=str(datetime.datetime.now()).replace(':','.'),
        prefix=str(prefixName)
        )
    )
    sampleWorksheet = sampleWorkbook.add_worksheet("Results")
    # NORMAL VALUES
    
    # Bold for titles
    bold = sampleWorkbook.add_format({'bold': True})
    # Row and column
    sampleWorksheet.write(0, COLUMN_INDEX_DICTIONARY[HEADER_GENERATION_TIME], HEADER_GENERATION_TIME, bold)
    sampleWorksheet.write(0, COLUMN_INDEX_DICTIONARY[HEADER_TREE_SIZE_MEMORY], HEADER_TREE_SIZE_MEMORY, bold)
    sampleWorksheet.write(0, COLUMN_INDEX_DICTIONARY[HEADER_PU_USAGE], HEADER_PU_USAGE, bold)

    allGenerationTimeList = []
    allHeapUsageList = []
    allPUsageList = []

    for index, timeHeapPuTuple in enumerate(sampleList):
        allPUsageList.append(timeHeapPuTuple[2])
        allHeapUsageList.append(timeHeapPuTuple[1])
        allGenerationTimeList.append(timeHeapPuTuple[0])

        dataRowIndex = index + 1
        sampleWorksheet.write(dataRowIndex, COLUMN_INDEX_DICTIONARY[HEADER_GENERATION_TIME], timeHeapPuTuple[0])
        sampleWorksheet.write(dataRowIndex, COLUMN_INDEX_DICTIONARY[HEADER_TREE_SIZE_MEMORY], timeHeapPuTuple[1])
        sampleWorksheet.write(dataRowIndex, COLUMN_INDEX_DICTIONARY[HEADER_PU_USAGE], timeHeapPuTuple[2])

    # STANDARD DEVIATION VALUES FOR EACH SAMPLE COLLECTION
    sampleWorksheet.write(0, COLUMN_INDEX_DICTIONARY[HEADER_GENERATION_TIME_SD], HEADER_GENERATION_TIME_SD, bold)
    sampleWorksheet.write(0, COLUMN_INDEX_DICTIONARY[HEADER_TREE_SIZE_SD], HEADER_TREE_SIZE_SD, bold)
    sampleWorksheet.write(0, COLUMN_INDEX_DICTIONARY[HEADER_PU_SD], HEADER_PU_SD, bold)
    
    # Putting the values in
    sampleWorksheet.write(1, COLUMN_INDEX_DICTIONARY[HEADER_GENERATION_TIME_SD], get_standard_deviation(allGenerationTimeList))
    sampleWorksheet.write(1, COLUMN_INDEX_DICTIONARY[HEADER_TREE_SIZE_SD], get_standard_deviation(allHeapUsageList))
    sampleWorksheet.write(1, COLUMN_INDEX_DICTIONARY[HEADER_PU_SD], get_standard_deviation(allPUsageList))

    sampleWorkbook.close()
    os.chdir("..")

selection = input("Hello!\nHave you put profiles in corresponding 'blazor' and 'react' folders and placed this script in the same directory as said folders? (Y/N)")
if selection.capitalize() == 'Y':
    print("Reading...")
    blazorSample = get_formated_sample_from_files("blazor")
    generate_xlsx_from_sample(blazorSample, "blazor")
    
    reactSample = get_formated_sample_from_files("react")
    generate_xlsx_from_sample(reactSample, "react")

    reactGenerationTimes = get_list_from_tuple_column(reactSample, 0)
    reactHeapUsage = get_list_from_tuple_column(reactSample, 1)
    reactPuUsage = get_list_from_tuple_column(reactSample, 2)

    blazorGenerationTimes = get_list_from_tuple_column(blazorSample, 0)
    blazorHeapUsage = get_list_from_tuple_column(blazorSample, 1)
    blazorPuUsage = get_list_from_tuple_column(blazorSample, 2)
    
    input("\n\nDone!\n\n>>T-VALUES ABOVE ARE NOT SAVED, COPY BEFORE FINISHING<<\n\n\nPress enter to finish...")
else:
    quit()
