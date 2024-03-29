import streamlit as st
import pandas
import numpy
import sys
import os
import random

st.title('Unique Golf Pairings - Tournament') 
# page_bg_img = '''
# <style>
# body {
# background-image: url("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRcJswd0L7Q3dY3d1Zlsv-CmhhaB2LH3TPhIw&usqp=CAU");
# background-size: cover;
# }
# </style>
# '''

# st.markdown(page_bg_img, unsafe_allow_html=True)

#num = st.slider('How many players for your tournament? *Note: must be divisible by 3 or 4', min_value=9)  
#st.write('** For the pairings to be completely unique, the minimum # of players needs to be 9 for pairings of 3 and 16 for pairings of 4')

#div = st.slider('Size of the group',min_value=3, max_value=4)  
#st.write(x, 'Players. Great!')

### Create a way to shuffle the list.

div = st.radio("Size of the group", [3,4])

golfer_input = st.text_area("Golfer list")
playerslist = golfer_input.split('\n')

st.write("You currently have {0}".format(len(playerslist)) + " players entered")

reshuffle = st.radio('I want a shuffled list', ['No','Yes'])

if reshuffle == 'Yes':
    random.shuffle(playerslist)
    
    # shuffled  = True
    # playerslist = golfer_input.split('\n')
    # random.shuffle(playerslist)
    # num = len(playerslist)
    # ghosts = 0

    # if (num%4 != 0 and div == 4):
    #   ghosts = 4-(num%4)
    #   if ghosts == 1:
    #       playerslist.append('Ghost1')
    #   elif ghosts == 2:
    #       playerslist.append('Ghost2')
    #       playerslist.insert(0,'Ghost1')
    #   else:
    #       playerslist.append('Ghost3')
    #       playerslist.insert(0,'Ghost1')
    #       playerslist.insert(int((num/4)+3),'Ghost2')


num = len(playerslist)
ghosts = 0

if (num%4 != 0 and div == 4):
    ghosts = 4-(num%4)
    if ghosts == 1:
        playerslist.append('Ghost1')
    elif ghosts == 2:
        playerslist.append('Ghost2')
        playerslist.insert(0,'Ghost1')
    else:
        playerslist.append('Ghost3')
        playerslist.insert(0,'Ghost1')
        playerslist.insert(int((num/4)+3),'Ghost2')


def make_pairings(num, div):
    #num = int(entry1.get())
    #div = int(entry2.get())
    if num%div == 0:
        
        players = list(range(num))
        
        day1 = pandas.DataFrame(numpy.array(players).reshape(int(num/div),div))
        
        first= numpy.array(players)[0:int(num/div)]
        second = numpy.array(players)[int(num/div):(int(num/div)*2)]
        third = numpy.array(players)[int(num/div)*2:(int(num/div)*3)]
        
        day2 = pandas.DataFrame({0:first,1:second,2:third})
        
        if div == 4:
            fourth = numpy.array(players)[int(num/div)*3:(int(num/div)*4)]
            day2 = pandas.DataFrame({0:first,1:second,2:third,3:fourth}) 
        
        day2col2 = list(day2.loc[:,1])
        day3col2 = (day2col2[len(day2col2) - 1:len(day2col2)]
                   +day2col2[0:len(day2col2) - 1])
        day2col3 = list(day2.loc[:,2])
        day3col3 = (day2col3[len(day2col3) - 2:len(day2col3)]
                   +day2col3[0:len(day2col3) - 2])
        day3 = pandas.DataFrame({0:first,1:day3col2,2:day3col3})
        
        
        if div == 4:
            day2col4 = list(day2.loc[:,3])
            day3col4 = (day2col4[len(day2col4) - 3:len(day2col4)]
                       +day2col4[0:len(day2col4) - 3])
            day3 = pandas.DataFrame({0:first,1:day3col2,2:day3col3,3:day3col4})
        
        counter = 0
        for player in playerslist:
            day1 = day1.replace(counter,player)
            day2 = day2.replace(counter,player)
            day3 = day3.replace(counter,player)
            counter += 1

        day1 = day1.rename(columns=lambda s: 'Player_' + str(s+1), index=lambda s: 'Pairing_' + str(s+1))
        day2 = day2.rename(columns=lambda s: 'Player_' + str(s+1), index=lambda s: 'Pairing_' + str(s+1))
        day3 = day3.rename(columns=lambda s: 'Player_' + str(s+1), index=lambda s: 'Pairing_' + str(s+1))

    return day1, day2, day3


try:
    day1,day2,day3 = make_pairings(len(playerslist), div)
    
    st.write("Round 1:", day1)
    st.write("Round 2:", day2)
    st.write("Round 3:", day3)
    #st.write("Golferlist", golfer_input)
    #st.write("len", len(playerslist))
    #path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Documents\\pairings.txt')
    #st.write(path)
    #if st.button('Send text results to Documents path'):
        #path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Documents\\pairings.txt')
        #with open(path, 'w') as f:
            #print('Day1:\n' + day1.to_string() + '\n\n\nDay2:\n' + day2.to_string() + '\n\n\nDay3:\n' + day3.to_string(), file=f) 
    #st.write('Note: clicking this will reshuffle the list if that option is checked')
    st.write('=OFFSET(\$A$1,COLUMNS(\$A1:A1)-1+(ROWS($1:1)-1)*4,0)')
except:
    st.write("The current configuration of the parameters does not yield a valid result")

#st.download_button("DOWNLOAD!", data="Trees", file_name="pairings.txt")
