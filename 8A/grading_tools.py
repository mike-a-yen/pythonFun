import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mc
import math
import argparse
import re
from ConfigParser import SafeConfigParser
ColorConverter = mc.ColorConverter()

class GradeTable(object):
    '''
    Tools to make grading easier for physics 8A
    '''
    def __init__(self,path=None,section=None):
        '''
        open the .csv file containing grades
        '''
        if os.path.exists(path):
            self.grade_table = pd.read_csv(path)
        else:
            raise IOError('No such file or directory')
        
        # replace all NaNs with 0
        self.grade_table.fillna(0, inplace=True)
        self.__clean_possible_points__()
        self.__clean_column_names__()
        self.__clean_columns__()
        self.columns = self.grade_table.columns

        if section != None:
            self.grade_table = self.__SelectSection__(int(section))

    def __clean_column_names__(self):
        '''
        Rename the columns to something easier
        Removes weird characters at the end of
        the column names
        '''
        rename = lambda x: re.sub('\s[()0-9].*','',x)
        self.grade_table.rename(columns=rename, inplace=True)
        self.columns = self.grade_table.columns

    def __clean_columns__(self):
        '''
        Perform some processing on the columns to make
        them easier to work with
        '''
        self.grade_table['Section Number'] = self.grade_table['Section'].apply(\
                                                  GradeTable.__CleanSection__)
        is_num = lambda x: (re.search('^[0-9.-]+',x) is not None)
        object_columns = self.grade_table.select_dtypes(['object'])

        for col in object_columns.columns:
            object_columns[col] = object_columns[col].astype('str')
            contains_nums = object_columns[col][1:].apply(is_num)
            if np.all(contains_nums):
                self.grade_table[col] = self.grade_table[col].astype(float)

        self.grade_table['Section Number'] = self.grade_table['Section Number'].astype(int) 
       
    @classmethod
    def __CleanSection__(cls,section):
        if isinstance(section,str):
            return re.findall(r'\b\d+\b',section)[0]
        else:
            return section

    def __clean_possible_points__(self):
        '''
        Replace all instances of (read only) with 100
        '''
        self.grade_table.loc[self.grade_table['Student']=='    Points Possible'] = self.grade_table.loc[self.grade_table['Student']=='    Points Possible'].replace('(read only)',100)
        
    def SelectColumn(self,name):
        return self.grade_table[name]

    def NumberOfStudents(self):
        return len(self.grade_table)-1

    def PossiblePoints(self):
        return self.grade_table.loc[self.grade_table['Student']=='    Points Possible']

    def Below(self,cut,name,include=True):
        '''
        Select entries below a threshold
        '''
        if include:
            return self.grade_table[self.grade_table[name] <= cut]
        else:
            return self.grade_table[self.grade_table[name] < cut]
       
    def Above(self,cut,name,include=True):
        '''
        Select entries above a theshold
        '''
        if include:
            return self.grade_table[self.grade_table[name] >= cut]
        else:
            return self.grade_table[self.grade_table[name] > cut]
       
    def Between(self,low,high,name,include=True):
        '''
        Select entries in a range
        '''
        if include:
            mask = (self.grade_table[name] >= low) & (self.grade_table[name] <= high)
            return self.grade_table[mask]
        else:
            mask = (self.grade_table[name] > low) & (self.grade_table[name] < high)
            return self.grade_table[mask]

    def __SelectSection__(self,section):
        mask1 = (self.grade_table['Section Number'] == section)
        mask2 = (self.grade_table['Student'] == '    Points Possible')
        return self.grade_table[mask1 | mask2]

    def Mean(self,name):
        return self.grade_table[name][1:].mean()
    def Median(self,name):
        return self.grade_table[name][1:].median()
    def Std(self,name):
        return self.grade_table[name][1:].std()

    def Histogram(self,name,bin_width=None,cuts=[1,2],title=None,color='blue',edge_color=None):
        outOf = self.PossiblePoints()[name][0]
        mean = self.Mean(name)
        median = self.Median(name)
        sigma = self.Std(name)
        grades = self.SelectColumn(name)[1:]
        
        if bin_width == None:
            if outOf <= 10:
                bin_width = 1
            elif outOf <= 100:
                bin_width = 5
        bins = np.arange(0,outOf+bin_width, bin_width)

        if title == None:
            title = name

        if edge_color == None:
            edge_color = ColorConverter.to_rgba(color)
        color = ColorConverter.to_rgba(color,alpha=0.8)
            
        fig, ax = plt.subplots(2,1,figsize=(8.5,11),tight_layout=True)
        fig.patch.set_facecolor('0.65')
        ax[0].set_title(title, fontsize=20,
                        bbox=dict(facecolor='white',edgecolor='black',pad=10))
        n,bins,patches = ax[0].hist(grades.values.astype(float),bins,rwidth=0.8,histtype='bar',
                                    color=color,edgecolor=edge_color,linewidth=1.5)

        # mean
        ax[0].axvline(mean,color='r',linestyle='dashed',linewidth=2,alpha=0.75)
        ax[0].text(mean,1.13*max(n),'$Mean$',color='black',rotation=270)
        # sigma lines
        for c in cuts:
            if mean-c*sigma > 0:
                ax[0].axvline(mean-c*sigma,color='y',linestyle='dashed',linewidth=2,alpha=0.75)
                ax[0].text(mean-c*sigma,1.13*max(n),'$%.1f \sigma$'%c,color='black',rotation=270)
            if mean+c*sigma < outOf:
               ax[0].axvline(mean+c*sigma,color='y',linestyle='dashed',linewidth=2,alpha=0.75)
               ax[0].text(mean+c*sigma,1.13*max(n),'$%.1f \sigma$'%c,color='black',rotation=270)

        # stats box
        ax[0].text(bins[0]+bin_width,0.9*max(n),
                   'Mean: %.2f\nMedian: %.2f\nStd: %.2f'%(mean,median,sigma),
                   color='black',bbox=dict(facecolor='white',edgecolor='black'))
        ax[0].set_xticks(bins)
        ax[0].set_xlim(0,1.1*bins[-1])
        ax[0].set_ylim(0,1.2*max(n))
        ax[0].set_xlabel('Grade [Points]')

        # Make table of distribution
        columns = ('Score','Number of Students','Percentage','Cumulative Percentage')
        rows = ['%d-%d'%(l,l+bin_width) for l in bins[:-1]]
        data = [ [rows[i],int(num),
                  np.round(num/sum(n)*100,2),
                  np.round(sum(n[0:i+1])/sum(n)*100,2)]
                 for i,num in enumerate(n)]
        ax[1].set_frame_on(False)
        ax[1].axes.get_xaxis().set_visible(False)
        ax[1].axes.get_yaxis().set_visible(False)
        t=ax[1].table(cellText=data,
                      colLabels=columns,
                      rowLoc='right',colLoc='center',
                      loc='upper center')
        for i in xrange(len(columns)):
            t.auto_set_column_width(i)

        message = 'This distribution was made by binning scores in %d point intervals. '\
                  'The lower limit of the bin is the minimum required score to be placed\n'\
                  'in that bin. For example, a score of %d is placed the the %d-%d bin not '\
                  'the 0-%d bin.'%(bin_width,bin_width,bin_width,2*bin_width,bin_width)
        fig.text(0.5,0.01,message,fontsize=8,color='black',ha='center',
                 bbox=dict(facecolor='gray',edgecolor='black'))
        plt.show()
        toSave = raw_input('Save figure? [y/n]')
        if toSave.lower() == 'y':
            name = raw_input('Save as: ')
            fig.savefig(name)
        plt.close('all')
