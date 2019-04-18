import math
import argparse
import matplotlib.pyplot as plt
import numpy as np 
from scipy.interpolate import griddata
from mpl_toolkits.mplot3d import Axes3D
from subject_scraping import init_subject_dict
from random import randint as rand
from random import shuffle
from copy import copy, deepcopy
# subject codes [1..5]

def wam_change(before,after):
    results = []  
    for skip in range(1,5):
        for i in range(101):
            for num_subs in range(1,14):
                if math.fabs(after - (before*num_subs+i*skip)/(num_subs+skip)) < 1e-2:
                    # print(skip, i,num_subs)

                    # skip --> number of subjects whose wam have change 
                    # i -> calculated grade 
                    # num subs - number of subjects a student has taken so far 
                    results.append((skip,num_subs,i))
    return results

def plot_surf_res(wams):

    x,y,z = zip(*wams)
    grid_x, grid_y = np.mgrid[min(x):max(x):100j,min(y):max(y):100j]
    grid_z = griddata((x,y),z,(grid_x,grid_y),method='cubic')

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.plot_surface(grid_x,grid_y,grid_z,cmap=plt.cm.Spectral)
    ax.set_title("BEFORE: {} | AFTER: {}".format(args.before,args.after))
    ax.set_xlabel("NUM SUBS CHANGED / WEIGHTING")
    ax.set_ylabel("NUM SUBS COMPLETED")
    ax.set_zlabel("SCORE")
    return fig

class Subjects(object):

    def __init__(self):
        self.enrolments = dict()
        self.subject_list = init_subject_dict()
        self.students = {} 
    def enroll_student(self,student_id, subjects):
        if student_id not in self.students: 
            self.students[student_id] = []

        for s in subjects: 
            # update the student edge list 
            if s not in self.students[student_id]:
                self.students[student_id].append(s)

            if s in self.subject_list: 
                # we can update / create an entry in the enrollment list 
                if s not in self.enrolments: 
                    self.enrolments[s] = self.subject_list[s]

                # else we can just update the enrollment of the student 
                self.enrolments[s]["enrolled"].add(student_id)

            else:
                # error handling, for now lets do nothing 
                printf("..................")
   
    def update_subject_model(self):
        # right now lets read this from a file 
        fp = open("changed.data")
        lines = fp.readlines() 
        
        for sid in lines: 
            # student id
            print(sid.strip(),end=" ")
            sid_subs = self.students[sid.strip()] 

            # for each of the subejcts in the student id, check their enrollments and update the 
            # subject dict 
            for s in sid_subs: 
                entry = self.subject_list[s]

                entry["changed"].add(sid)
        print()
    def simulate_students(self,num_common=0): 
        
        NUM_STUDENTS = 10
        students = range(NUM_STUDENTS)
        student_list = {} 
        subjects = [] 
        for s in self.subject_list: 
            subjects.append(s)
        shuffle(subjects) 
        subjects = subjects[:10]
        
        all_indexes = set()
        # randomise the subjects per person 
        for s in students:
            indexes = set() 
            student_list[str(s)] = []
            # generate the subjects 
            while len(indexes) < 4 :
                ind = rand(0,len(subjects)-1)
                
                if ind not in indexes: 
                    indexes.add(ind)
                    all_indexes.add(ind)
                
                if len(indexes) == 4: 
                    break
            for ind in indexes:
                student_list[str(s)].append(subjects[ind])

        # choose common subjects between students 
        # pick a random student 
        # this is the reference student 
        sid_ref = rand(0,NUM_STUDENTS-1) 
        common_subs = [] 
        # choose two subjects from this person, lets just pick the first n 
        if num_common == 4:
            common_subs = student_list[str(sid_ref)]
            for sid in student_list:
                student_list[sid] = common_subs


        elif num_common > 0: 
            common_subs = student_list[str(sid_ref)][:num_common]
            print(common_subs)     
            # for each student, we want to get their new subject list 
            for sid in student_list:
                if sid == str(sid_ref):
                    continue

                # we can interate through all the students and update their subjects accordingly
                new_subs = set()
                for i in common_subs:
                    new_subs.add(i)
                
                # generate the new list of subs for each student 
                
                for sub in student_list[sid]:
                    new_subs.add(sub)
                    
                    if len(new_subs) == 4:
                        break   
                # change the subject list of that student 
                new_subs = [i for i in new_subs]
                student_list[sid] = new_subs
                
        # for each student we want to add them to the model 
        for sid in student_list:    
            subs = student_list[sid]
            self.enroll_student(sid,subs)
        
        return

    def print_students(self):
        for sid in self.students:
            print("{} : {}".format(sid,self.students[sid]))

    def print_enrolment_stats(self):
        for en in self.enrolments: 
            num_changed = len(self.enrolments[en]["changed"])
            num_enrolled = len(self.enrolments[en]["enrolled"])

            print("{} : {}/{}".format(en,num_changed,num_enrolled))
                    
def plot_scatter_res(wams):

    x,y,z = zip(*wams)
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.scatter(x,y,z,cmap=plt.cm.Spectral)
    ax.set_title("BEFORE: {} | AFTER: {}".format(args.before,args.after))
    ax.set_xlabel("NUM SUBS CHANGED / WEIGHTING")
    ax.set_ylabel("NUM SUBS COMPLETED")
    ax.set_zlabel("SCORE")
    return fig

    
# PROCESS THE ARGUMENTS
parser = argparse.ArgumentParser(description='Musician Multhreaded Testing')
parser.add_argument('-b', '--before',
                        help='Dataset name',
                        choices=range(0,101),
                        required=True,
                        type=int)

parser.add_argument('-a', '--after',
                        help='Dataset name',
                        choices=range(0,101),
                        required=True,
                        type=int)

parser.add_argument('-p', '--plot',
                        help='Plot Type',
                        choices={"scatter","surf"},
                        default="scatter",
                        type=str)

parser.add_argument('-c', '--common',
                        help='Number of Common Subjects',
                        choices=range(5),
                        default=0,
                        type=int)
args = parser.parse_args()

a = wam_change(args.before,args.after)

model = Subjects() 
model.simulate_students(num_common=args.common)
print("STUDENT SUBJECT LIST")
model.print_students()
print()
print("CLASS STATS - Before update")
model.print_enrolment_stats()
print()
print("CLASS STATS - After update")
print("the students who reported a change: ", end="")
model.update_subject_model()
model.print_enrolment_stats()
if args.plot == "surf":
    plot_surf_res(a)
else:
    plot_scatter_res(a)
