import numpy as np
import random
import simpy
import time 




montly_weight = {"January":1.5,"February":0.6,"March":1.3,"April":0.9,"May":1.6,"June":1.1,"July":0.3,"August":0.3,"September":0.7,"October":1.0,"November":1.4,"December":0.9}
working_days = ["Monday","Tuesday","Wednesday","Thursday","Friday"] 
NUMBER_OF_BOOKS = 111569 # There are 111569 published books in the library
NUMBER_OF_CHAIRS = 1000 #Tha capacity of the library is 1000 chairs
LIBRARY_STAFF = 2 # There are two person in the library staff in order to handle the students
MAXIMUM_BOOKS = 5 # A student can borrow maximum 5 books

BORROW_BOOK_TIME = 17 # books are added to the system by reading their qr code in 17s seconds
REGISTRATION_TIME = 900 #a registration takes maximum 15 minutes so it take 900 seconds
RETURN_BOOK_TIME = 3 #students drop the books on table in 3 seconds

LOOKING_FOR_BOOK_TIME = 420 #A student can find book that they are looking for at 7 minutes so it takes 420 seconds
STUDENTS_ARRIVAL_TIME = 25 # Student arrival time is approxiamately in 25 seconds
MAX_STUDY_TIME = 10800 #seconds
SIM_TIME_ALL_YEAR =  7171200 #working days in a year that students can use the library (for one day 8 hours = 28800 seconds and there are 249 working days in a year)
SIM_TIME_MOTNH = 7171200/12 # Every months have different number of students so we need simulate each individual month. 
SIM_TIME_DAY = 7171200/249
CHOICE_ARRAY = np.array([True,False]) # choices for student when they enter the library
LIBRARY_QUEUE_LENGTH = 0 # The queue length of the borrow/return desk is 0 at the beginning



class OUTPUT():
    FAIL = '\033[31m'
    SUCCESS = '\033[32m'
    PROCESS = '\033[33m'
    STARTING = '\033[37m'
    INFO = '\033[34m'

class LibraryStaff:
    def __init__(self, env, number_of_staff):
        self.env = env
        self.staff = simpy.Resource(env, number_of_staff)

class Chairs:
    def __init__(self, env, number_of_chairs):
        self.env = env
        self.chairs = simpy.Resource(env, number_of_chairs)

class Library:
    def __init__(self, env,mw, number_of_chairs, library_staff,number_of_book,borrow_book_time, registration_time, return_book_time, looking_for_book_time, max_study_time,queue_length):
        self.env = env
        self.mw = mw
        self.number_of_chairs = number_of_chairs
        self.library_staff = library_staff
        self.number_of_book=number_of_book
        self.borrow_book_time = borrow_book_time
        self.registration_time = registration_time
        self.return_book_time = return_book_time
        self.looking_for_book_time = looking_for_book_time
        self.max_study_time = max_study_time      
        self.queue_length = queue_length  
        self.chairs = Chairs(env, number_of_chairs).chairs
        self.staff = LibraryStaff(env, library_staff).staff
        self.looking_for_book = env.event()

    def register(self, student):
        random_time = max(1,np.random.normal(self.registration_time,4))
        if self.queue_length > 15:
                self.library_staff = 2
        else:
            self.library_staff = 1
        print(OUTPUT.INFO + f"Queue length of the borrow/return desk is {self.queue_length} at {env.now:.2f}")
        print(OUTPUT.INFO +f"Number of Library Staff is {self.library_staff} at {env.now:.2f}")
        print(OUTPUT.STARTING +f"Registeration procces for student {student} started at {self.env.now:.2f}")
        output.write(f"Queue length of the borrow/return desk is {self.queue_length} at {env.now:.2f}\n")
        output.write(f"Number of Library Staff is {self.library_staff} at {env.now:.2f}\n")
        output.write(f"Registeration procces for student {student} started at {self.env.now:.2f}\n")


        yield self.env.timeout(random_time)
        print(OUTPUT.SUCCESS +f"Student {student} successfully registered at {self.env.now:.2f}")
        output.write(f"Student {student} successfully registered at {self.env.now:.2f}\n")

    def look_for_book(self, student,number_of_books):
        random_time = max(1,np.random.normal(self.looking_for_book_time,4))
        print(OUTPUT.STARTING +f"Student {student} started looking for a {number_of_books} book  at {self.env.now:.2f}")
        output.write(f"Student {student} started looking for a {number_of_books} book(s)  at {self.env.now:.2f}\n")
        yield self.env.timeout(random_time)
        print(OUTPUT.SUCCESS +f"Student {student} found the book at {self.env.now:.2f}")
        output.write(f"Student {student} found the book at {self.env.now:.2f}\n")

    def borrow_book(self, student,number_of_books):
        random_time = max(1,np.random.normal(self.borrow_book_time,4))
        if self.number_of_book <= 0:
            print(OUTPUT.FAIL +f"All books are borrowed {env.now:.2f}")
            output.write(f"All books are borrowed {env.now:.2f}\n")
        
        if self.number_of_book < number_of_books:
            print(OUTPUT.FAIL +f"Student {student} cannot borrow {number_of_books} book at {self.env.now:.2f}")
            output.write(f"Student {student} cannot borrow {number_of_books} book at {self.env.now:.2f}\n")
        

        print(OUTPUT.INFO + f"The number of books in the library that are available is {self.number_of_book} at {env.now:.2f}")
        output.write(f"The number of books in the library that are available is {self.number_of_book} at {env.now:.2f}\n")
        if self.queue_length > 15:
                self.library_staff = 2
        else:
            self.library_staff = 1
        
        print(OUTPUT.INFO + f"Queue length of the borrow/return desk is {self.queue_length} at {env.now:.2f}")
        print(OUTPUT.INFO +f"Number of Library Staff is {self.library_staff} at {env.now:.2f}")
        print(OUTPUT.STARTING +f"Borrowing process for student {student} started at {self.env.now:.2f}")
        output.write(f"Queue length of the borrow/return desk is {self.queue_length} at {env.now:.2f}\n")
        output.write(f"Number of Library Staff is {self.library_staff} at {env.now:.2f}\n")
        output.write(f"Borrowing process for student {student} started at {self.env.now:.2f}\n")
        if number_of_books < 5:
            yield self.env.timeout(random_time)
            self.number_of_book = self.number_of_book - number_of_books
            print(OUTPUT.SUCCESS +f"Student {student} successfully borrowed {self.number_of_book} the book(s) at {self.env.now:.2f}")
            output.write(f"Student {student} successfully borrowed {self.number_of_book} the book(s) at {self.env.now:.2f}\n")
        else: 
            print(OUTPUT.FAIL +f"Student {student} cannot borrow more than 5 books at {self.env.now:.2f}")
            output.write(f"Student {student} cannot borrow more than 5 books at {self.env.now:.2f}\n")
    
    def return_book(self, student,has_book,number_of_books):
        random_time = max(1,np.random.normal(self.return_book_time,4))
        if has_book:
            print(OUTPUT.STARTING +f"Returning process for student {student} started at {self.env.now:.2f}")
            output.write(f"Returning process for student {student} started at {self.env.now:.2f}\n")
            yield self.env.timeout(random_time)
            self.number_of_book = self.number_of_book + number_of_books
            print(OUTPUT.SUCCESS +f"Student {student} successfully returned the book at {self.env.now:.2f}")
            output.write(f"Student {student} successfully returned the book at {self.env.now:.2f}\n")
        else:
        
            print(OUTPUT.FAIL +f"Student {student} has no book to return at {self.env.now:.2f}")
            output.write(f"Student {student} has no book to return at {self.env.now:.2f}\n")

    def study(self, student,study_time):
        study_time = study_time//self.mw
        print(OUTPUT.INFO + f"The number of chairs that are available is {self.number_of_chairs} at {env.now:.2f}")
        output.write(f"The number of chairs that are available is {self.number_of_chairs} at {env.now:.2f}\n")
        self.number_of_chairs = self.number_of_chairs - 1
        random_time = max(1,np.random.normal(self.max_study_time,4))
        print(OUTPUT.STARTING +f"Student {student} started studying at {self.env.now:.2f}")
        print(OUTPUT.INFO + f"Number of available chairs is {self.number_of_chairs} at {env.now:.2f}")
        output.write(f"Student {student} started studying at {self.env.now:.2f}\n")
        output.write(f"Number of available chairs is {self.number_of_chairs} at {env.now:.2f}\n")
        yield self.env.timeout(random_time)
        self.number_of_chairs = self.number_of_chairs + 1
        print(OUTPUT.PROCESS +f"Student {student} studied for {study_time/3600:.2f} hour(s).")
        output.write(f"Student {student} studied for {study_time/3600:.2f} hour(s).\n")
        print(OUTPUT.SUCCESS +f"Student {student} studied at {self.env.now:.2f}")
        output.write(f"Student {student} studied at {self.env.now:.2f}\n")


def visit_library(env, name, library):
    global students_handled
    prob_not_registered = 0.25*library.mw
    prob_registered = 1-prob_not_registered
    is_registered = np.random.choice(CHOICE_ARRAY, p=[prob_registered, prob_not_registered])
    is_borrow_book = np.random.choice(CHOICE_ARRAY, p=[0.3, 0.7])
    is_return_book = np.random.choice(CHOICE_ARRAY, p=[0.3, 0.7])
    prob_study = 0.5*library.mw
    prob_not_study = 1-prob_study
    is_studying_after_borrowing_returning = np.random.choice(CHOICE_ARRAY, p=[prob_study, prob_not_study])
    number_of_books = random.randint(1,MAXIMUM_BOOKS)
    has_book = np.random.choice(CHOICE_ARRAY, p=[0.9, 0.1])
    study_time = random.randint(int(1800*library.mw),int(MAX_STUDY_TIME*library.mw))
    print(OUTPUT.INFO +f"Student {name} enters library at {env.now:.2f}!")
    output.write(f"Student {name} enters library at {env.now:.2f}!\n")
    if not is_registered:
        
        library.queue_length += 1
        with library.staff.request() as request:
            yield request
            yield env.process(library.register(name))
            library.queue_length -= 1

    if is_borrow_book:  
        
            
        with library.staff.request() as request:

            yield request
            for i in range(number_of_books):
                yield env.process(library.look_for_book(name,i+1))
            library.queue_length += 1  
            for j in range(number_of_books):
                yield env.process(library.borrow_book(name,j+1))
            library.queue_length -= 1
        if is_studying_after_borrowing_returning:
            with library.chairs.request() as request:
                yield request
                print(OUTPUT.PROCESS +f"Student {name} is studying after borrowing at {env.now:.2f}!")
                output.write(f"Student {name} is studying after borrowing at {env.now:.2f}!\n")
                yield env.process(library.study(name,study_time))
    
           
            
    
    elif is_return_book:
        with library.staff.request() as request:
            yield request
            if has_book: number_of_books = 1
            for i in range(number_of_books):
                yield env.process(library.return_book(name,has_book,i+1))
        
        if is_studying_after_borrowing_returning:
            with library.chairs.request() as request:
                yield request
                print(OUTPUT.PROCESS +f"Student {name} is studying after returning at {env.now:.2f}!")
                output.write(f"Student {name} is studying after returning at {env.now:.2f}!\n")
                yield env.process(library.study(name,study_time))
        
       
    else:
        with library.chairs.request() as request:
            yield request
            yield env.process(library.study(name,study_time))
       
    
    print(OUTPUT.SUCCESS +f"Student {name} leaves library at {env.now:.2f}!")
    output.write(f"Student {name} leaves library at {env.now:.2f}!\n")

    students_handled +=1

def setup(env,mw,number_of_chairs,number_of_books ,library_staff, student_interval, borrow_book_time, registration_time, return_book_time, looking_for_book_time, max_study_time,queue_length):
    library = Library(env,mw, number_of_chairs,number_of_books, library_staff,borrow_book_time, registration_time, return_book_time, looking_for_book_time, max_study_time,queue_length)

    for i in range(1,10):
        env.process(visit_library(env, i, library))

    while True:
        yield env.timeout(random.randint(student_interval -1, student_interval +1))
        i+=1
        env.process(visit_library(env, i, library))
        print(OUTPUT.INFO +f"There are  {i-students_handled} students in library")
        output.write(f"There are  {i-students_handled} students in library \n")



if __name__ == "__main__":
    mode = input("Enter mode: (month,year)")
    if mode == "month":
        start_time = time.time()
        outputsh = open("outputmshd.txt", "w")
        outputsh.write("Output for MSHD,\n")
        output = open("output_each_month_daily.txt", "w")
        print(OUTPUT.STARTING+f"Library Simulation for each month {SIM_TIME_MOTNH/3600:.2f} hours")
        output.write(f"Library Simulation for 1 Year {SIM_TIME_MOTNH/3600:.2f} hours\n")
        total_handeled_students = 0
        monthly__handled_students = 0
        for mn in montly_weight:
            print(OUTPUT.STARTING+f"Library Simulation is running now for month {mn}...")
            output.write(f"Library Simulation is  running now for month {mn}...\n")
            for i in range(4):
                for day in working_days:
                    students_handled = 0 # Number of students that served by the library.
                    mw = montly_weight[mn]
                    print("-"*45)
                    output.write("-"*45 + "\n")
                    print(OUTPUT.STARTING+f"Library Simulation is running now for {day}...")
                    output.write(f"Library Simulation is  running now for {day}...\n")
                    random.seed(42)
                    env = simpy.Environment()
                    monthly_arrival_time = STUDENTS_ARRIVAL_TIME//mw
                    env.process(setup(env,mw,NUMBER_OF_CHAIRS,LIBRARY_STAFF,NUMBER_OF_BOOKS,monthly_arrival_time, BORROW_BOOK_TIME, REGISTRATION_TIME, RETURN_BOOK_TIME, LOOKING_FOR_BOOK_TIME, MAX_STUDY_TIME,LIBRARY_QUEUE_LENGTH))
                    env.run(until=SIM_TIME_DAY)
                    print(OUTPUT.STARTING+f"Library Simulation is finished for {day}.")
                    output.write(f"Library Simulation is finished for month {day}.\n")
                    print(OUTPUT.STARTING+f"For {day} number of handled student: ", students_handled)
                    output.write(f"For {day} number of handled student: "+str(students_handled)+"\n")
                    outputsh.write(f"{students_handled},\n")
                    monthly__handled_students += students_handled
                    print("-"*45)
                    output.write("-"*45 + "\n")
            print(OUTPUT.STARTING+f"Library Simulation is finished for month {mn}.")
            output.write(f"Library Simulation is finished for month {mn}.\n")
            print(OUTPUT.STARTING+f"For month {mn} number of handled student: ", monthly__handled_students)
            output.write(f"For month {mn} number of handled student: "+str(monthly__handled_students)+"\n")
            total_handeled_students += monthly__handled_students
        output.write("Library Simulation is finished.\n")
        print(OUTPUT.STARTING+"Student handled: ", total_handeled_students)
        output.write("Student handled: "+str(total_handeled_students)+"\n")
        end_time = time.time()
        print("Simulation tooks ", end_time-start_time, " seconds")
        output.write("Simulation tooks "+str(end_time-start_time)+" seconds\n")
        output.close()
        outputsh.close()
    elif mode == "year":
        start_time = time.time()
        output = open("output_all_year_daily.txt", "w")
        print(OUTPUT.STARTING+f"Library Simulation for 1 Year {SIM_TIME_ALL_YEAR/3600:.2f} hours")
        output.write(f"Library Simulation for 1 Year {SIM_TIME_ALL_YEAR/3600:.2f} hours\n")
        total_students_handled = 0 # Number of students that served by the library.
        for i in range(50):
            for day in working_days:
                students_handled = 0
                print("-"*45)
                output.write("-"*45 + "\n")
                print(OUTPUT.STARTING+f"Library Simulation is running now for {day}")
                output.write(f"Library Simulation is running now for {day}\n")
                random.seed(42)
                env = simpy.Environment()
                env.process(setup(env,1,NUMBER_OF_CHAIRS,LIBRARY_STAFF,NUMBER_OF_BOOKS,STUDENTS_ARRIVAL_TIME, BORROW_BOOK_TIME, REGISTRATION_TIME, RETURN_BOOK_TIME, LOOKING_FOR_BOOK_TIME, MAX_STUDY_TIME,LIBRARY_QUEUE_LENGTH))
                env.run(until=SIM_TIME_DAY)
                print(OUTPUT.STARTING+f"Library Simulation is finished for {day}.")
                output.write(f"Library Simulation is finished for {day}.\n")
                print(OUTPUT.STARTING+f"Student handled for {day}: ", students_handled)
                output.write(f"Student handled for {day}: "+str(students_handled)+"\n")
                print("-"*45)
                output.write("-"*45 + "\n")
                total_students_handled += students_handled
        print(OUTPUT.STARTING+"Library Simulation is finished.")
        output.write("Library Simulation is finished.\n")
        print(OUTPUT.STARTING+"Student handled : ", total_students_handled)
        output.write("Student handled : "+str(total_students_handled)+"\n")
        end_time = time.time()
        print("Simulation tooks ", end_time-start_time, " seconds")
        output.write("Simulation tooks "+str(end_time-start_time)+" seconds\n")
        output.close()
    else:
        print("Wrong mode")



