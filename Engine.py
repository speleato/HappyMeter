__author__ = 'Sergio'

import array
from decimal import *
getcontext().prec = 3

Period_Between_Slopes = 2 #days
Length_Sample_Data = 3 #days
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
    [1,0,-1,0,-1,-1,-1],
    [1,1,1,1,1,1,1],
    [-1,-1,-1,-1,-1,-1,-1]
]

#Structure to store the slopes through time
Slope_Values = array
Slope_Variations = array

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
        Group_influence = [[None for x in range (len(Group[0]))] for y in range (len(Group))]
        #initially we have no scopes so the list will be initiated with values 100. The number of slope variations and
        #slope values that we will have will be determined by the amount of days that we have divided by how many days are
        #we going to take in between samples.
        Slope_Values = [[None for x in range (1)] for y in range (len(Group))]
        Slope_Variations = [[None for x in range ((1))] for y in range (len(Group))]
        Group_influence = [[None for x in range (1)] for y in range (len(Group))]

    def Testeable(self):
        number = len([1,1,1,1,1,1])
        return "this works" + str(number)

    def calculateSlope(self, dataSet):
        number_of_data= len(dataSet)
        sum_of_data=sum(dataSet)
        slope=Decimal(sum_of_data)/Decimal(number_of_data)
        return slope

    def InfluencersSearch(self):
        #Uses recursive algorithm to find all the positive and negative influencers of a determined time period on the slope
        global Slope_Variations
        global Significative_Slope_variation

        PositiveInfluenceR_Candidates = []
        NegativeInfluenceR_Candidates = []
        PositiveInfluenceD_Candidates = []
        NegativeInfluenceD_Candidates = []

        positiveInfluenceR_votes = 0
        negativeInfluenceR_votes = 0
        positiveInfluenceD_votes = 0
        negativeInfluenceD_votes = 0
        for x in range(len(Slope_Variations)):
            for y in range (len(Slope_Variations[x])):
                if Slope_Variations[x][y] > 0:
                    if Slope_Variations[x][y] < Significative_Slope_variation:
                        #positive influence user WHO HAS NOT BEEN INFLUENCED BY OTHER USERS
                        positiveInfluenceR_votes += 1
                    if Slope_Variations[x][y] >= Significative_Slope_variation:
                        #positive influence user WHO HAS BEEN INFLUENCED BY OTHER USERS
                        positiveInfluenceD_votes += 1
                if Slope_Variations[x][y] < 0:
                    if (Slope_Variations[x][y] * (-1)) < Significative_Slope_variation:
                        #negative influence user WHO HAS NOT BEEN INFLUENCED BY OTHER USERS
                        negativeInfluenceR_votes += 1
                    if (Slope_Variations[x][y] * (-1)) >= Significative_Slope_variation:
                        #negative influence user WHO HAS BEEN INFLUENCED BY OTHER USERS
                        negativeInfluenceD_votes += 1
                if Slope_Variations[x][y] == 0:
                    #this user is either pure positive or pure negative. Either way he is an influencer.
                    if (Group[x][y*(Period_Between_Slopes+1)] > 0):
                        positiveInfluenceR_votes += 1
                    elif (Group[x][y*(Period_Between_Slopes+1)] < 0):
                        negativeInfluenceR_votes += 1
            #If this candidate has been more times positive influencer than negative, it will go into the positive candidates
            #If it has been more times negative influencer, it will go into the negative candidates.
            #If the times of positive or negative times are equal, he does not get promoted to candidate.
            if (positiveInfluenceR_votes+ negativeInfluenceR_votes > positiveInfluenceD_votes + negativeInfluenceD_votes):
                #this user is an influcence over other users
                if positiveInfluenceR_votes > negativeInfluenceR_votes:
                    PositiveInfluenceR_Candidates.append(x)

                elif positiveInfluenceR_votes < negativeInfluenceR_votes:
                    NegativeInfluenceR_Candidates.append(x)

            if (positiveInfluenceR_votes+ negativeInfluenceR_votes < positiveInfluenceD_votes + negativeInfluenceD_votes):
                #this user is has been influenced by other users
                if positiveInfluenceD_votes > negativeInfluenceD_votes:
                    PositiveInfluenceD_Candidates.append(x)
                elif positiveInfluenceD_votes < negativeInfluenceD_votes:
                    NegativeInfluenceD_Candidates.append(x)

            #We reset the votes
            positiveInfluenceR_votes = 0
            negativeInfluenceR_votes = 0
            positiveInfluenceD_votes = 0
            negativeInfluenceD_votes = 0

        #We return the users that have been classified as influencers and influenceds.
        return (PositiveInfluenceR_Candidates, NegativeInfluenceR_Candidates, PositiveInfluenceD_Candidates, NegativeInfluenceD_Candidates)

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
        global Slope_Variations
        # This function will determine who is influencing who and to what extent
        # In order to do that, we will look at the variations that each user has suffered and compare them with the rest of the
        # users variations. We will consider that a user has been influenced if his variation is greater than the Significative_Slope_Variation value.
        Positive_InfluenceRs, Negative_InfluenceRs, Positive_InfluenceDs, Negative_InfluenceDs=self.InfluencersSearch()
        print Positive_InfluenceRs
        print Negative_InfluenceRs

        print Positive_InfluenceDs
        print Negative_InfluenceDs
        #print Negative_Influencers
        for i in range (len(Group)):
            if (i in Positive_InfluenceDs):
                #this user have been influenced by any positive_InfluenceR candidate
                print "positive"
                Group_influence[i]= Positive_InfluenceRs
            elif (i in Negative_InfluenceDs):
                #this user have been influenced by any negative_InfluenceR candidate
                print "negative"
                Group_influence[i] = Negative_InfluenceRs

        for x in range(len(Group)):
            print Group_influence[x]


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
        #///////////////////////////////////////////  OK  ///////////////////////////////////////////////////////////////////
        #We calculate the mood after each month.
        #1. dataset_moment will point to the different points in time we will take
        #   samples from each user's dataset to obtain the scope. Initially will be the first period (first month)
        #2. Length_Sample_Data will be the amount of days we will be taking as a sample. Given the dataset_moment, we will
        #   take both from the future as from the past to obtain an average value of the slope at that given moment.
        iterations = 1
        dataset_moment = Period_Between_Slopes
        while (len(Group[0])> dataset_moment + (Length_Sample_Data/2)):
            #We calculate the slope after each month for each user
            for i in range(len(Group)):
                arrayUser = Group[i][(dataset_moment - (Length_Sample_Data/2)):(dataset_moment + ((Length_Sample_Data/2) + (Length_Sample_Data%2)))]
                slopeForUserI =self.calculateSlope(arrayUser)  #TBD (Kevin)
                #We store the value of the slope obtained this month compared to the value of the previous monthx
                #print "We are going to insert the value of slope ", slopeForUserI, "minus the value of ", Slope_Values[i][iterations-1], " which equals ", slopeForUserI - Slope_Values[i][iterations-1]
                Slope_Variations[i].insert(iterations-1, slopeForUserI - Slope_Values[i][iterations-1])
                Slope_Values[i].insert(iterations, slopeForUserI)
            iterations += 1
            dataset_moment = Period_Between_Slopes*(iterations)
        #Now we have the slopes of every user at every month of the dataset that we have been provided. We will have to
        #to compare them to see who is influencing who.

        #We first eliminate garbage values
        for x in range(len(Slope_Values)):
            Slope_Values[x].pop()
        #print "Slope variations"
        for x in range(len(Slope_Variations)):
            Slope_Variations[x].pop()


        #for x in range(len(Slope_Values)):
        #    print Slope_Values[x]
        print "Slope variations"
        for x in range(len(Slope_Variations)):
            print Slope_Variations[x]

        self.interpretateInfluence()

