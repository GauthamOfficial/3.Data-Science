class Univariate():
    
    def quanQual(dataset):
        quan = []
        qual = []
        for columnName in dataset.columns:
            #print(columnName)
            if(dataset[columnName].dtype == 'O'):
                #print("qual")
                qual.append(columnName)
            else:
                #print("quan")
                quan.append(columnName)
        return quan, qual


    
    def freqTable(columnName, dataset):
        freqTable = pd.DataFrame(columns = ["Unique_Values", "Frequency", "Relative_Frequency", "Cumulative_Frequency"])
        freqTable["Unique_Values"] = dataset[columnName].value_counts().index
        freqTable["Frequency"] = dataset[columnName].value_counts().values
        freqTable["Relative_Frequency"] = (freqTable["Frequency"]/103)
        freqTable["Cumulative_Frequency"] = freqTable["Relative_Frequency"].cumsum()
        return freqTable


    def Univariate(dataset, quan):
        descriptive = pd.DataFrame(index = ["Mean", "Median", "Mode", "Q1:25%", "Q2:50%", "Q3:75%", "Q4:100%", "IQR", "1.5rule", "Lesser", "Greater", "Min", "Max"], columns = quan) 
        for columnName in quan:
            descriptive.loc["Mean", columnName] = dataset[columnName].mean()
            descriptive.loc["Median", columnName] = dataset[columnName].median()
            descriptive.loc["Mode", columnName] = dataset[columnName].mode().iloc[0]
            #descriptive.loc["Q1:25%", columnName] = np.percentile(dataset[columnName], 25)
            descriptive.loc["Q1:25%", columnName] = dataset.describe()[columnName]["25%"]
            descriptive.loc["Q2:50%", columnName] = dataset.describe()[columnName]["50%"]
            descriptive.loc["Q3:75%", columnName] = dataset.describe()[columnName]["75%"]
            descriptive.loc["Q4:100%", columnName] = dataset.describe()[columnName]["max"]
            descriptive.loc["IQR", columnName] = descriptive.loc["Q3:75%", columnName] - descriptive.loc["Q1:25%", columnName]
            descriptive.loc["1.5rule", columnName] = 1.5 * descriptive.loc["IQR", columnName]
            descriptive.loc["Lesser", columnName] = descriptive.loc["Q1:25%", columnName] - descriptive.loc["1.5rule", columnName]
            descriptive.loc["Greater", columnName] = descriptive.loc["Q3:75%", columnName] + descriptive.loc["1.5rule", columnName]
            descriptive.loc["Min", columnName] = dataset[columnName].min()
            descriptive.loc["Max", columnName] = dataset[columnName].max()
        return descriptive

    
    def check_values(descriptive, quan):
        lesser = []
        greater = []
        
        for columnName in quan:
            if descriptive[columnName]["Min"] < descriptive[columnName]["Lesser"]:
                lesser.append(columnName)
            if descriptive[columnName]["Max"] > descriptive[columnName]["Greater"]:
                greater.append(columnName)
        
        return lesser, greater

    
    def update_dataset_bounds(dataset, descriptive, lesser, greater):
        # Update values in lesser columns
        for columnName in lesser:
            dataset.loc[dataset[columnName] < descriptive[columnName]["Lesser"], columnName] = descriptive[columnName]["Lesser"]
    
        # Update values in greater columns
        for columnName in greater:
            dataset.loc[dataset[columnName] > descriptive[columnName]["Greater"], columnName] = descriptive[columnName]["Greater"]
    
        return dataset