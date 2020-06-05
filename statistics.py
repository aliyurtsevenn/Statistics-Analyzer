'''
Statistics Analyzer

Ali Yurtseven

You can compare your variables statistically using this program. You only need to verify if your data
is dependent or independent. Also, if you use csv, you need to write your data in a tab separated way.

If you choose hypothesis testing

The output gives you:

1.  if each is normally distributed.
2. Coefficient of Variation in your each variable
3. Which statistical test is applied for comparison
4. If there are more than 2 groups, the program also pairwise comparison between groups


If you choose regression analysis,

You need to specific if you want categorical response (yes or no) or continuos response as outcome.

If you have categorical response, we apply logistic regression. Here, you need to show which variables
are dependent one.

If you have continuous response, we apply linear regression. Here, you don't need to specify your dependent
variable.

The output gives you:

1. If your dependent variable is related to your independent variables.
2. Comparision of relation between each independent variable and dependent variable if you have more than one
independent variable.


'''


import pandas as pd
import numpy as np
import pathlib
import os
from datetime import date


# Applied functions and tests
from scipy.stats import variation
from scipy.stats import shapiro
from scipy.stats import iqr
from scipy.stats import ttest_1samp
from scipy.stats import mannwhitneyu
from scipy.stats import ttest_ind
from scipy.stats import ttest_rel
from scipy.stats import wilcoxon
from scipy.stats import f_oneway
from scipy.stats import kruskal
from statsmodels.stats.anova import AnovaRM
from scipy.stats import friedmanchisquare
from scipy.stats import levene

'''
Note that your statistics.py and parameters.py files should be in the same folder or directory if you want your code to work
'''
parameter_path=os.path.join(pathlib.Path(__file__).parent.absolute(),'parameters.txt')

parameter=pd.read_csv(parameter_path,'\t',header=None)


data_with= pd.read_excel(parameter[0][6])


data_with=data_with.dropna()
statistics_type = str(parameter[0][0])
dependency=str(parameter[0][1])
data=data_with[data_with.columns[1:]]
comprasion_type=str(parameter[0][3])
number_of_dependent_group=str(parameter[0][4])
output_dir=str(parameter[0][5])

# Let me check if users gave the parameters  correctly! If not, they need to rewrite the parameters

while True:
    if statistics_type.isnumeric():
        if int(statistics_type)==0 or int(statistics_type)==1:
            break
        else:
            print("You typed a number different than 0 or 1 for statistics_type variable, please try again!.")
            statistics_type = input(
                "Type 0 (if you want regression analysis of your data), Type 1 (if you want hypothesis testing analysis of your data) :")

    else:
        print("statistics_type variable contains non-integer characters. You need to type only integer, either 0 or 1!")
        statistics_type = input(
            "Type 0 (if you want regression analysis of your data), Type 1 (if you want hypothesis testing analysis of your data) :")

while True:
    if dependency.isnumeric():
        if int(dependency)==0 or int(dependency)==1:
            break
        else:
            print("You typed a number different than 0 or 1 for dependency variable, please try again!.")
            statistics_type = input(
                "Type 0 (if your data is dependent), Type 1 (if your data is independent) :")

    else:
        print("statistics_type variable contains non-integer characters. You need to type only integer, either 0 or 1!")
        statistics_type = input(
            "Type 0 (if your data is dependent), Type 1 (if your data is independent) :")


class statistics():
    def __init__(self, statistics_type,data,dependency,data_with,comprasion_type,number_of_dependent_group):
        self.statistics_type = statistics_type
        self.data=data
        self.dependency=dependency
        self.data_with=data_with
        self.comrasion_type=comprasion_type
        self.number_of_dependent_group=number_of_dependent_group
    def analyzer(self):
        global name, p_val
        statistics_type=self.statistics_type
        data_with=self.data_with
        mydata=self.data_with
        comprasion_type=self.comrasion_type
        number_of_dependent_group=self.number_of_dependent_group
        '''
        Let me check if your data contains any categorical value in the first column! If no, 
        this part will be extracted for the comparison between continuous variables 
        '''
        if int(comprasion_type)==0:
            num=[]
            for i in range(0,len(data_with.columns)):
                k = data_with[data_with.columns[i]].tolist()
                for j in k:
                    if (str(j).isalpha())==True:
                        num.append(i)
                        break
            if len(num)==1:
                mydata = mydata.drop(mydata.columns[num[0]], axis=1)
            else:
                mydata = mydata.drop(mydata.columns[num], axis=1)
        elif int(comprasion_type)==1:
            num=[]
            for i in range(0,len(data_with.columns)):
                k = data_with[data_with.columns[i]].tolist()
                for j in k:
                    if (str(j).isalpha())==True:
                        num.append(i)
                        break
            num.remove(number_of_dependent_group-1)
            if len(num)==1:
                mydata = mydata.drop(mydata.columns[num[0]], axis=1)
            else:
                mydata = mydata.drop(mydata.columns[num], axis=1)


        number_of_groups= len(mydata.columns)
        sample_size=mydata.shape[0]
        mydata.dropna()

        # Firstly, let me write the statical test analysis
        if int(statistics_type)==1: # 1 means that the user selected the statistical analysis
            if int(comprasion_type) == 0:  # 1 means that your comprasion is for continuous data
                if int(number_of_groups)==1:   # Here, number is how many groups or variables the data contains

                    '''
                    If you have only 1 sample, you need to use one sample t-test. 
                    Here, you compare sample means with the population mean. As a result, 
                    you need to give the population mean.            
                    '''
                    mean_val=mydata.mean().to_list()[0]
                    median_val=mydata.median().to_list()[0]
                    std_val=mydata.std().to_list()[0]
                    one_group_list = [item for sublist in mydata.values.tolist() for item in sublist]
                    coef=variation(one_group_list)
                    shap_p_value=shapiro(one_group_list)[1]
                    rang=max(one_group_list)-min(one_group_list)
                    Interquile_rang=iqr(one_group_list)
                    p_val_one_sample_t=ttest_1samp(one_group_list,4)[1]
                    name="One sample t Test"
                    return statistics_type, number_of_groups,sample_size,mean_val,median_val,std_val,coef,shap_p_value,rang,Interquile_rang,p_val_one_sample_t,name
            if int(number_of_groups)==2:
                if int(comprasion_type)==0:  # 1 means that you confirmed that you compare continous data
                    if int(dependency)==1:
                        '''
                        Since your data is independent, you can use either parametric statistical test, which your data 
                        should be normally distributed and they should havve size bigger than 30. In this case, the 
                        program uses student t test. Other case, the program uses Mann Whitney U test. 
                        '''
                        mean_val = mydata.mean().to_list()
                        median_val = mydata.median().to_list()
                        std_val = mydata.std().to_list()
                        s1=mydata[mydata.columns[0]].to_list()
                        s2=mydata[mydata.columns[1]].to_list()
                        coef = variation(s1)
                        coef2 = variation(s2)
                        shap_p_1=shapiro(s1)[1]
                        shap_p_2=shapiro(s2)[1]
                        Interquile_range1=iqr(s1)
                        Interquile_range2=iqr(s2)
                        Int=[]
                        Int.append(Interquile_range1)
                        Int.append(Interquile_range2)
                        rn1=max(s1)-min(s1)
                        rn2=max(s2)-min(s2)
                        rn=[rn1,rn2]
                        if shap_p_1>0.05 and shap_p_2>0.05:
                            if sample_size>=30:
                                p_val= ttest_ind(s1,s2)[1]
                                name="Student's t Test"
                            else:
                                p_val = mannwhitneyu(s1, s2)[1]
                                name = "Mann Whitney U test"
                        else:
                            p_val= mannwhitneyu(s1,s2)[1]
                            name="Mann Whitney U test"
                        return sample_size,mean_val, median_val,std_val,coef,coef2,s1,s2,shap_p_1,shap_p_2,p_val,name,rn,Int
                    elif int(dependency)==0:    # Here you confirm that your data is dependent!
                        '''
                        If your 2 samples are  normally distributed and have sample size which are bigger than 
                        30. It means that you can use parametric statistical test analysis, which is 
                        Paired sample t test. Otherwise, you need to use nonparametric test which is Wilxcon 
                        Signed Rank test.     
                        '''
                        mean_val = mydata.mean().to_list()
                        median_val = mydata.median().to_list()
                        std_val = mydata.std().to_list()
                        s1=mydata[mydata.columns[0]].to_list()
                        s2=mydata[mydata.columns[1]].to_list()
                        coef = variation(s1)
                        coef2 = variation(s2)
                        shap_p_1=shapiro(s1)[1]
                        shap_p_2=shapiro(s2)[1]
                        Interquile_range1=iqr(s1)
                        Interquile_range2=iqr(s2)
                        Int=[]
                        Int.append(Interquile_range1)
                        Int.append(Interquile_range2)
                        rn1=max(s1)-min(s1)
                        rn2=max(s2)-min(s2)
                        rn=[rn1,rn2]
                        if shap_p_1 > 0.05 and shap_p_2 > 0.05:
                            if sample_size >= 30:
                                p_value = ttest_rel(s1, s2)[1]
                                name="Paired sample t test"
                            else:
                                p_value = wilcoxon(s1, s2)[1]
                                name = "Wilcoxon Singed Rank test"
                        else:
                            p_value = wilcoxon(s1, s2)[1]
                            name="Wilcoxon Singed Rank test"
                        return sample_size, mean_val, median_val, std_val, coef, coef2, s1, s2, shap_p_1, shap_p_2, p_value,name,rn,Int


            if int(number_of_groups)>= 3: # Here we will use statistical analysis for the groups more than  2
                if int(comprasion_type)==0:  # You state that your data is independent!
                    if int(dependency)==1:

                        '''
                        Since I have more than 2 independent groups, I can use either One way ANOVA or 
                        Kruskal Wallis test! Here, you can do one bye one comprasion of the groups by 
                        Post Hoc Analysis! Before, you need to know if your variables have equal variances 
                        or not using Levene's test! 
                        '''
                        mean_val = mydata.mean().to_list()
                        median_val = mydata.median().to_list()
                        std_val = mydata.std().to_list()
                        s=[]
                        coe=[]
                        shap=[]
                        rn=[]
                        Int=[]
                        count=0
                        for pp in range(0,number_of_groups):
                            s1 = mydata[mydata.columns[pp]].to_list()
                            s.append(s1)
                            coef = variation(s1)
                            coe.append(coef)
                            shap_p_1 = shapiro(s1)[1]
                            shap.append(shap_p_1)
                            k=iqr(s1)
                            Int.append(k)
                            sss=max(s1)-min(s1)
                            rn.append(sss)
                            count=count+1
                        p_levene = levene(*s)[1]



                        if all(j>0.05 for j in shap):
                            if sample_size>=30:
                                p_val= f_oneway(*s)[1]
                                name="One way ANOVA test"
                            else:
                                p_val = kruskal(*s)[1]
                                "Kruskal Wallis test"
                        else:
                            p_val=kruskal(*s)[1]
                            "Kruskal Wallis test"
                        return sample_size,mean_val,median_val,std_val,s,coe,shap,name,rn,Int,p_levene,p_val

                    elif int(dependency)==0:
                        '''
                        If my data is dependent and have more than 2 samples, I can use either 
                        RM ANOVA or Friedman test!
                        '''
                        mean_val = mydata.mean().to_list()
                        median_val = mydata.median().to_list()
                        std_val = mydata.std().to_list()
                        s=[]
                        coe=[]
                        shap=[]
                        rn=[]
                        Int=[]
                        count=0
                        for pp in range(0,number_of_groups):
                            s1 = mydata[mydata.columns[pp]].to_list()
                            s.append(s1)
                            coef = variation(s1)
                            coe.append(coef)
                            shap_p_1 = shapiro(s1)[1]
                            shap.append(shap_p_1)
                            k=iqr(s1)
                            Int.append(k)
                            sss=max(s1)-min(s1)
                            rn.append(sss)
                            count=count+1
                        p_levene = levene(*s)[1]
                        if all(j>0.05 for j in shap):
                            if sample_size>=30:
                                p_val="I couldn't find it, you should use RM ANOVA"
                                name='RMANOVA test'
                            else:
                                p_val=kruskal(*s)
                                name = "Friedman Chisquare Test"
                        else:
                            p_val=friedmanchisquare(*s)[1]
                            name= "Friedman Chisquare Test"
                        return sample_size,mean_val,median_val,std_val,s,coe,shap,name,rn,Int,p_levene,p_val


mydata=data_with
if int(comprasion_type)==0:
    num=[]
    for i in range(0,len(data_with.columns)):
        k = data_with[data_with.columns[i]].tolist()
        for j in k:
            if (str(j).isalpha())==True:
                num.append(i)
                break
    if len(num)==1:
        mydata = mydata.drop(mydata.columns[num[0]], axis=1)
    else:
        mydata = mydata.drop(mydata.columns[num], axis=1)
elif int(comprasion_type)==1:
    num=[]
    for i in range(0,len(data_with.columns)):
        k = data_with[data_with.columns[i]].tolist()
        for j in k:
            if (str(j).isalpha())==True:
                num.append(i)
                break
    num.remove(number_of_dependent_group-1)


if int(statistics_type)==1:
    if len(mydata.columns)==1:
        p = statistics(statistics_type, data, dependency,data_with,comprasion_type,number_of_dependent_group)
        statistics_type, number, sample_size, mean_val, median_val, std_val, coef, shap_p_val, range, Interquile_range, p_val,name = p.analyzer()
        new_frame=pd.DataFrame({'Applied Statistics Name':[name],'Sample size':[sample_size],'Mean Value':[mean_val],
                                'Median Value':[median_val],'Standard Deviation':[std_val],'Coefficient of variation':[coef],
                                'Range':[range],'Interquile Range':[Interquile_range],'Shapiro Wilk p value':[shap_p_val],'p value':[p_val]})
        new_frame.to_excel(output_dir,index=False)

    elif len(mydata.columns)==2:
        p=statistics(statistics_type,data,dependency,data_with,comprasion_type,number_of_dependent_group)
        sample_size,mean_val, median_val, std_val,coef,coef2,s1,s2,shap_p_1,shap_p_2,p_val,name,rn,Int= p.analyzer()
        shap_p_val=[shap_p_1,shap_p_2]
        coeff=[coef,coef2]
        mydict={'Applied Statistics Name':name,'Sample size':sample_size,'Mean Value':mean_val,
                                'Median Value':median_val,'Standard Deviation':std_val,'Coefficient of variation':coeff,
                                'Range':rn,'Interquile Range':Int,'Shapiro Wilk p value':shap_p_val,'p value':p_val}
        dict_df = pd.DataFrame({key: pd.Series(value) for key, value in mydict.items()})

        dict_df.to_excel(output_dir,index=False)


    elif len(mydata.columns)>2:
        p=statistics(statistics_type,data,dependency,data_with,comprasion_type,number_of_dependent_group)
        sample_size,mean_val,median_val,std_val,s,coe,shap_val,name,rn,Int,p_levene,p_val= p.analyzer()
        mydict = {'Applied Statistics Name': name, 'Sample size': sample_size, 'Mean Value': mean_val,
                  'Median Value': median_val, 'Standard Deviation': std_val, 'Coefficient of variation': coe,
                  'Range': rn, 'Interquile Range': Int, 'Shapiro Wilk p value': shap_val,'Levene test p value':p_levene,'p value':p_val}
        dict_df = pd.DataFrame({key: pd.Series(value) for key, value in mydict.items()})
        dict_df.to_excel(output_dir,index=False)


'''

Comprasion between pairs and adjsuted p values

'''



