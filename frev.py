def change_date_format(to_update):
    '''to_update=l[2]'''
    l1=to_update.split("/")
    #print(l1)
    temp=l1[0]
    l1[0]=l1[2]
    l1[2]=temp
    #print(l1)
    to_update=l1[0]+"/"+l1[1]+"/"+l1[2]
    return to_update


'''print(l)
l[2]=change_date_format(l[2])
print(l)'''

def change_date_time_format(l):
    tp=l[3]
    tpl=tp.split(" ")
    tpl[0]=change_date_format(tpl[0])
    l[2]=tpl[0]
    #print(tpl[0])
    #print(tpl[1])
    #print(tpl[2])
    if tpl[2]=="PM":
        tpl2=tpl[1].split(":")
        temp=tpl2[0]
        temp=int(temp)+12
        if temp==24:
            tpl2[0]="00"
        else:
            tpl2[0]=str(temp)
       # print(temp)
        #print(tpl2[0])
        tpl[1]=tpl2[0]+":"+tpl2[1]+":"+tpl2[2]
        to_return = tpl[0] + " " + tpl[1]
    elif tpl[2]=="AM":
        to_return=tpl[0]+" "+tpl[1]
    return to_return

def change_last(t):
    t2=""
    for i in range(len(t)):
        if t[i]=="\n":
            break
        else:
            t2=t2+t[i]
    return t2

def bal_change(l):
    t=l[7]
    t1=l[8]
    t2=""
    t21=""
    for i in range(len(t)):
        if t[i]==",":
            continue
        else:
            t2=t2+t[i]
    for j in range(len(t1)):
        if t1[j]==",":
            continue
        else:
            t21=t21+t1[j]
    l[7]=t2
    l[8]=t21
    return l

