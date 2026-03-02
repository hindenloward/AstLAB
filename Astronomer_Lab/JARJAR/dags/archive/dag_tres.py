
from airflow.sdk import dag, task
from datetime import datetime

@dag(start_date=datetime(2026, 2, 21),
    schedule=None, tags=['LAB']
)
#Defining general tasks - printing to logs
def dag_tres():
    @task
    def first_wt():
        var = 1
        print(var)
    @task
    def second_wt():
        var = 2
        print(var)
    @task
    def third_wt():
        var = 3
        print(var)
    @task
    def fourth_wt():
        var = 4
        print(var)
    @task
    def fifth_wt():
        var = 1
        print(var)
    @task
    def sixth_wt():
        var = 2
        print(var)
    @task
    def seventh_wt():
        var = 3
        print(var)
    @task
    def eight_wt():
        var = 4
        print(var)
    @task
    def ninth_wt():
        var = 1
        print(var)
    @task
    def tenth_wt():
        var = 2
        print(var)
    @task
    def eleventh_wt():
        var = 3
        print(var)
    @task
    def twelfth_wt():
        var = 4
        print(var)
    @task
    def thirtenth_wt():
        var = 1
        print(var)
    @task
    def fourtenth_wt():
        var = 2
        print(var)
    @task
    def fiftenth_wt():
        var = 3
        print(var)
    @task
    def sixtenth_wt():
        var = 4
        print(var)
    @task
    def sevententh_wt():
        var = 4
        print(var)
    @task
    def eightenth_wt():
        var = 1
        print(var)
    @task
    def ninetenth_wt():
        var = 2
        print(var)
    @task
    def twentyth_wt():
        var = 3
        print(var)
    @task
    def twentyrfirst_wt():
        var = 3
        print(var)
    @task
    def twentysecond_wt():
        var = 4
        print(var)
    @task
    def twentythird_wt():
        var = 1
        print(var)
    @task
    def twentryfourth_wt():
        var = 2
        print(var)
    @task
    def twentyfifth_wt():
        var = 3
        print(var)
    @task
    def twentysixth_wt():
        var = 4
        print(var)

#assigning variables to each task, since Airflow will start an instance every time a task is explicitly called

    a=first_wt()
    b=second_wt()
    c=third_wt()
    d=fourth_wt()
    e=fifth_wt()
    f=sixth_wt()
    g=seventh_wt()
    h=eight_wt()
    i=ninth_wt()
    j=tenth_wt()
    k=eleventh_wt()
    l=twelfth_wt()
    m=thirtenth_wt()
    n=fourtenth_wt()
    o=fiftenth_wt()
    p=sixtenth_wt()
    q=sevententh_wt()
    r=eightenth_wt()
    s=ninetenth_wt()
    t=twentyth_wt()
    u=twentyrfirst_wt()
    v=twentysecond_wt()
    w=twentythird_wt()
    x=twentryfourth_wt()
    y=twentyfifth_wt()
   
#dependency definition via variable
    a>>[b, c, d, e]

    b>>f
    c>>g
    d>>h
    e>>i

    f>>[j,k,l,m]
    g>>[n,o,p,q]
    h>>[r,s,t,u]
    i>>[v,w,x,y]





dag_tres()












