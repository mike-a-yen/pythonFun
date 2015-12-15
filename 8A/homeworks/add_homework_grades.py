import pandas as pd
import numpy as np

grade_book = pd.read_csv('mastering_physics/09_Dec_10-22_Grades-PHYSICS_8A_-_LEC_002.csv')
homework_book = pd.read_csv('SPELIOPHY8AF15-20151209-Scores.csv',
                            header=2,
                            skip_footer=2)

total_grade = homework_book.columns[-1]
print total_grade
possible = 887. # looked up from .csv
homework_book['Total Percent'] = homework_book[total_grade]/possible

# convert Mastering Physics grade to bCourse Grade
out_of = 50. # 10% of total grade, half of a midterm
missing_file = open('Spelio_missing.txt','w')
missing_file.write('Students whose IDs were not found in Mastering Physics\n')
grade_book['Homework'] = 0
for i,student in grade_book.iterrows():
    if student['Student'].strip()=='Points Possible':
        grade_book.loc[i,('Homework',)] = out_of
        continue
    
    sid = student['SIS User ID']
    if isinstance(sid,(int,float)) and np.isnan(sid):
        print '...........NAN.............'
        print student
        continue
    if len(sid) != 8:
        print '='*30+' NOT PRESENT '+'='*30
        print student
        print '='*70
        missing_file.write(student['Student']+'\n')
        continue
    sid = str(int(sid))
    # check if sid is in mastering physics
    if sid not in homework_book['Student ID'].values:
        # student not in mastering physics
        print '='*30+' NOT PRESENT '+'='*30
        print student
        print '='*70
        missing_file.write(student['Student']+'\n')
        continue
    elif len(np.argwhere(sid == homework_book['Student ID'])) > 1:
        # student in mastering physics more than once
        print '*'*30+' DUPLICATE '+'*'*30
        print student
        print '*'*70
       
    hw_grade = homework_book.loc[homework_book['Student ID']==sid]['Total Percent'].values.max()
    grade_book.loc[i,('Homework',)] = hw_grade*out_of

print grade_book['Homework'].describe()
grade_book.to_csv('09_Dec_10-22_Grades-PHYSICS_8A_-_LEC_002.csv',index=False)
missing_file.close()
