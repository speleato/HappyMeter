__author__ = 'Sergio'

import array
from decimal import *
getcontext().prec = 3

Period_Between_Slopes = 2 #days
Length_Sample_Data = 2 #days
Significative_Slope_variation = 0.2 #degrees

#Structure to store input data
#User = array('i')
#Group = array(User)
Group = [
    [1,0,1,1,-1,-1,0],
    [1,0,0,-1,-1,-1,1],
    [0,1,0,-1,0,-1,0],
    [0,1,1,0,1,1,1],
    [0,0,-1,-1,0,0,0],
    [1,0,-1,0,-1,-1,-1]
]

#Structure to store the slopes through time
Slope_Values = list
Slope_Variations = list

#Structure for returning results. For each user, and for each Period_Between_Slopes we will store which user have influenced
#the user. For example, if user 3 at Period_Between_Slopes[4] has been influenced by users 1 and two, the position in the matrix
# Group_Influence[3][4] will be equal = "1,2".
User_influence = list
Group_influence = list


class Engine(object):

    def __init__(self, groupInput):
        #variables initialization. Supposition: we will not have a null input and the given data will be a square
        #matrix, not a set of different length arrays. Every value will be initialized (NO NULL VALUES)
        global Group
        global Period_Between_Slopes
        global Length_Sample_Data
        global Slope_Variations
        global Slope_Values
        global Group_influence
        #Group = groupInput
        lengthOfArrays = len(Group[0])
        #initially, nobody has influence over anybody
        Group_influence = [[None for x in range (len(Group))] for y in range (len(Group[0]))]
        #initially we have no scopes so the list will be initiated with values 100. The number of slope variations and
        #slope values that we will have will be determined by the amount of days that we have divided by how many days are
        #we going to take in between samples.
        Slope_Values = [[100]*(len(Group[0])/Period_Between_Slopes)]*len(Group)
        Slope_Variations = [[100]*(len(Group[0])/Period_Between_Slopes)]*len(Group)
        Group_influence = [[100]*(len(Group[0])/Period_Between_Slopes)]*len(Group)

    def Testeable(self):
        number = len([1,1,1,1,1,1])
        return "this works" + str(number)

    def calculateSlope(self, dataSet):
        number_of_data= len(dataSet)
        sum_of_data=sum(dataSet)
        slope=Decimal(sum_of_data)/Decimal(number_of_data)
        return slope

    def recursiveInfluencersSearch(self,time_period, positiveInfluencer, negativeInfluencer, from_index, to_index):
        #Uses recursive algorithm to find all the positive and negative influencers of a determined time period on the slope
        global Slope_Variations
        global Significative_Slope_variation
        if from_index > to_index:
            return "", ""
        elif from_index == to_index:
            if Slope_Variations[from_index][time_period] > 0 and Slope_Variations[from_index][time_period] < Significative_Slope_variation:
                #positive influence user WHO HAS NOT BEEN INFLUENCED BY OTHER USERS
                return from_index + ',', ""
            elif Slope_Variations[from_index][time_period] < 0 and (Slope_Variations[from_index][time_period] * (-1)) < Significative_Slope_variation:
                #negative influence user WHO HAS NOT BEEN INFLUENCED BY OTHER USERS
                return "", from_index + ','
        else:
            #we make recursive call
            positiveInfluencer1, negativeInfluencer1 = self.recursiveInfluencersSearch(time_period, positiveInfluencer, negativeInfluencer, from_index, to_index/2)
            positiveInfluencer2, negativeInfluencer2 = self.recursiveInfluencersSearch(time_period, positiveInfluencer, negativeInfluencer, (to_index/2)+1, to_index)
            return positiveInfluencer1 + positiveInfluencer2, negativeInfluencer1 + negativeInfluencer2

            #for j in range (len(Group)):
            #    #We will iterate in this way: each iteration we will analyze the time period of every user and see who has influenced who.
            #    if Group[j][time_period] < Significative_Slope_variation:
            #        #This user might be an influence to other users, so we store THE USER as a possible candidate
            #        if Group[j][time_period] > 0:
            #           Positive_Influencer = Positive_Influencer + j + ','
            #        else:
            #           Negative_Influencer = Negative_Influencer + j + ','
            #        if Group[j][time_period] > Significative_Slope_variation:
            #           #We have a user that has been influenced by someone this timeperiod.
            #           Possible_Influences = ""


    def interpretateInfluence(self):
        global Group
        global Significative_Slope_variation
        global User_influence
        global Group_influence
        # This function will determine who is influencing who and to what extent
        # In order to do that, we will look at the variations that each user has suffered and compare them with the rest of the
        # users variations. We will consider that a user has been influenced if his variation is greater than the Significative_Slope_Variation value.
        for i in range (len(Group[0])):
            Positive_Influencer = ""
            Negative_Influencer = ""
            Positive_Influencer, Negative_Influencer=self.recursiveInfluencersSearch(i,"","", 0, len(Group))
            for j in range (len(Group)):
                #We have all the positive influencers and the negative influencers of this period. We now see who HAS BEEN influenced
                if Group[j][i] > Significative_Slope_variation[j][i]:
                    #this user has been positively influenced
                    Group_influence[j].insert(i,Positive_Influencer)
                if Group[j][i] > (-1 * Significative_Slope_variation[j][i]):
                    #this user has been negatively influenced
                    Group_influence[j].insert(i,Negative_Influencer)


    def Influences(self):
        global Group
        global Period_Between_Slopes
        global Length_Sample_Data
        global Slope_Variations
        global Slope_Values
        global Group_influence
        #//////////////////////////////////////////////////////////////////////////////////////////////////////////////
        #We calculate the initial mood tendency of each user
        for i in range(len(Group)):
            arrayUser = Group[i][0:Length_Sample_Data]
            initialSlope = self.calculateSlope(arrayUser)  #TBD (Kevin)
            Slope_Values[i].insert(0,initialSlope) #(initialSlope)

        #//////////////////////////////////////////////////////////////////////////////////////////////////////////////
        #We calculate the mood after each month.
        #1. dataset_moment will point to the different points in time we will take
        #   samples from each user's dataset to obtain the scope. Initially will be the first period (first month)
        #2. Length_Sample_Data will be the amount of days we will be taking as a sample. Given the dataset_moment, we will
        #   take both from the future as from the past to obtain an average value of the slope at that given moment.
        iterations = 0
        dataset_moment = Period_Between_Slopes
        while (len(Group[0])> dataset_moment + (Length_Sample_Data/2)):
            #We calculate the slope after each month for each user
            for i in range(len(Group)):
                arrayUser = Group[i][(dataset_moment - (Length_Sample_Data/2)):(dataset_moment + (Length_Sample_Data/2))]
                slopeForUserI =self.calculateSlope(arrayUser)  #TBD (Kevin)
                #We store the value of the slope obtained this month compared to the value of the previous monthx
                Slope_Variations[i].insert(iterations, slopeForUserI - Slope_Values[i][-1])
                Slope_Values[i].insert(iterations, slopeForUserI)

            iterations += 1
            dataset_moment = Period_Between_Slopes*(iterations+1)
        #Now we have the slopes of every user at every month of the dataset that we have been provided. We will have to
        #   to compare them to see who is influencing who.
        print Slope_Values[0]
        print Slope_Variations[0]
        #self.interpretateInfluence()

