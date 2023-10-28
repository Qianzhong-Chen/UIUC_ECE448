# TextClassifier.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Dhruv Agarwal (dhruva2@illinois.edu) on 02/21/2019

"""
You should only modify code within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""
from math import log
class TextClassifier(object):
    def __init__(self):
        """Implementation of Naive Bayes for multiclass classification

        :param lambda_mixture - (Extra Credit) This param controls the proportion of contribution of Bigram
        and Unigram model in the mixture model. Hard Code the value you find to be most suitable for your model
        """
        self.lambda_mixture = 0.0
        self.likelihood = [0]*14 # likelihood table of P(word|class) = likelihood[class_num][word_index]
        self.bigram_likelihood = [0]*14
        self.prior = [0]*14 # prior table of P(class) = prior[class_num]
        self.bag = []
        self.bigram = []

    
    def fit(self, train_set, train_label):
        

        # TODO: Write your code here
        # creat the bag of words  
        
        for case_num in range(len(train_label)):
            process = case_num/len(train_label)*100
            print('creating bag of words...... %f'%process,'%')
            for word in train_set[case_num]:
                if word not in self.bag:
                    self.bag.append(word)

        print("bag of words has been creadted :)")
        

        # Record num of occuracy
        # word_occ = [class][occ_of_the_word]
        word_occ = []
        class_occ = [0]*14
        for i in range(14):
            word_occ.append([0]*len(self.bag))

        for i in range(len(train_label)):
            process = i/len(train_label)*100
            print('training...... %f'%process,'%')
            class_index = train_label[i]-1 # train labe has value 1-14
            class_occ[class_index] += 1  # train labe has value 1-14
            for j in train_set[i]:
                word_index = (self.bag).index(j)
                word_occ[class_index][word_index] += 1
      
        # smoothing and calculate the likelihoods & priors, meanwhile, take the log
        for i in range(14):
            self.likelihood[i] = [0]*len(self.bag)
        k = 0.1

        for i in range(14):
            self.prior[i] = log((class_occ[i]/len(train_label)))
            total_word_num_this_class = sum(word_occ[i])
            for j in range(len(self.bag)):
                self.likelihood[i][j] = log(((word_occ[i][j]+k)/(total_word_num_this_class + k*len(self.bag))))

        print('training has finished :)')

        for i in range(14):
            occ_list = sorted(word_occ[i])
            occ_list.reverse()
            word_list_print = []
            for j in range(20):
                word_index = (word_occ[i]).index(occ_list[j])
                word_to_append = self.bag[word_index]
                word_list_print.append(word_to_append)

            print('20 most found word in class',i+1,'is',word_list_print)

        
        pass

    def predict(self, x_set, dev_label,lambda_mix=0.0):
        
        accuracy = 0.0
        result = []
        acc_count = 0

        # TODO: Write your code here
        for i in range(len(dev_label)):
            process = i/len(dev_label)*100
            print('testing...... %f'%process,'%')
            post_list = [0]*14
            for j in range(14):
                # comment next line for uniform distribution case
                #post_list[j] += self.prior[j] 
                for k in x_set[i]:
                    if k not in self.bag:
                        continue
                    word_index = (self.bag).index(k)
                    post_list[j] += self.likelihood[j][word_index]

            class_most_like = post_list.index(max(post_list))
            result.append(class_most_like+1) # index is [0,13], class number is [1,14]

        con_matrix = [0]*14
        for i in range(14):
            con_matrix[i] = [0]*14

        for i in range(len(dev_label)):
            con_matrix[dev_label[i]-1][result[i]-1] += 1
            if dev_label[i] == result[i]:
                acc_count +=1
        accuracy = acc_count/len(dev_label)

        for i in range(14):
            for j in range(14):
                con_matrix[i][j] = round(float(con_matrix[i][j]/sum(con_matrix[i])*100), 3)

        print('confusion matrix:')
        print(con_matrix)
        print('testing has finished')
        return accuracy,result
    


############################ Extra Credid####################################################
"""
    def fit(self, train_set, train_label):
        
        :param train_set - List of list of words corresponding with each text
            example: suppose I had two emails 'i like pie' and 'i like cake' in my training set
            Then train_set := [['i','like','pie'], ['i','like','cake']]

        :param train_labels - List of labels corresponding with train_set
            example: Suppose I had two texts, first one was class 0 and second one was class 1.
            Then train_labels := [0,1]
        

        # TODO: Write your code here
        # create the bag of words               
        for case_num in range(len(train_set)):
            process = case_num/len(train_set)*100
            print('creating bag of words...... %f'%process,'%')
            for word in train_set[case_num]:
                if word not in self.bag:
                    (self.bag).append(word)

        print("bag of words has been creadted :)")

        # create the bag of bigrams  
        bag_dup = self.bag
        self.bigram = [0]*len(self.bag)
        # self.bigram = [['a','b','c']['d','e','f']......] 
        # 'self.bag[i] self.bigram[i][j]' can form a bigram
        for i in range(len(self.bag)):
            #self.bigram[i] = [bag_dup[i]]
            self.bigram[i] = [0]

        for case_num in range(len(train_set)):
            process = case_num/len(train_set)*100
            print('creating bag of bigrams...... %f'%process,'%')
            for now_index, first_word in enumerate(train_set[case_num][0:-1]):                
                bi_index = (self.bag).index(first_word) # index of the first word 
                second_word = train_set[case_num][now_index + 1]
                if second_word not in self.bigram[bi_index]:
                    (self.bigram[bi_index]).append(second_word)

        for i in range(len(self.bag)):
            del(self.bigram[i][0])

        print("bag of bigrams has been creadted :)")
        

        # Record num of occuracy
        # word_occ = [class][occ_of_the_word]
        # bi_occ = [class][first word][occ of the bigram]
        word_occ = []
        bi_occ = []
        class_occ = [0]*14
        for i in range(14):
            word_occ.append([0]*len(self.bag))
            bi_occ.append([0]*len(self.bag))
            for j in range(len(self.bag)):
                bi_num = len(self.bigram[j])
                bi_occ[i][j] = [0]*bi_num

        for i in range(len(train_set)):
            process = i/len(train_set)*100
            print('training...... %f'%process,'%')
            class_index = train_label[i]-1 # train labe has value 1-14
            class_occ[class_index] += 1  # train labe has value 1-14
            for now_index, j in enumerate(train_set[i]):
                word_index = (self.bag).index(j)
                word_occ[class_index][word_index] += 1
                if now_index != len(train_set[i]) - 1:
                    next_word = train_set[i][now_index+1]
                    
                    bi_index = (self.bigram[word_index]).index(next_word)
                    bi_occ[class_index][word_index][bi_index] += 1
      
        # smoothing and calculate the likelihoods & priors, meanwhile, take the log
        
        for i in range(14):
            self.likelihood[i] = [0]*len(self.bag)
            self.bigram_likelihood[i] = [0]*len(self.bag)
            for j in range(len(self.bag)):
                bi_num = len(self.bigram[j])
                self.bigram_likelihood[i][j] = [0]*bi_num 
        k = 0.1
        total_bigram_num_this_class = 0
        total_num_bigram = 0
        for i in range(len((self.bigram))):
            total_num_bigram += len(self.bigram[i])

        for i in range(14):
            self.prior[i] = log(((class_occ[i]+1)/len(train_set)))
            # self.prior[i] = log((class_occ[i]/len(train_set)))

            total_word_num_this_class = sum(word_occ[i])
            for j in range(len(self.bag)):
                total_bigram_num_this_class += sum(bi_occ[i][j])
            for j in range(len(self.bag)):
                self.likelihood[i][j] = log(((word_occ[i][j]+k)/(total_word_num_this_class + k*len(self.bag))))
                for h in range(len(self.bigram[j])):
                    
                    self.bigram_likelihood[i][j][h] = log((bi_occ[i][j][h])+k) / (total_bigram_num_this_class + k * total_num_bigram)
                    

        print('training has finished :)')
        
        pass

    def predict(self, x_set, dev_label,lambda_mix):
        
        :param dev_set: List of list of words corresponding with each text in dev set that we are testing on
              It follows the same format as train_set
        :param dev_label : List of class labels corresponding to each text
        :param lambda_mix : Will be supplied the value you hard code for self.lambda_mixture if you attempt extra credit

        :return:
                accuracy(float): average accuracy value for dev dataset
                result (list) : predicted class for each text
        

        accuracy = 0.0
        result = []
        acc_count = 0

        # TODO: Write your code here
        for i in range(len(dev_label)):
            process = i/len(dev_label)*100
            print('testing...... %f'%process,'%')
            post_list = [0] * 14 # unigram post probability
            post_bi_list = [0] * 14 # bigram post probability
            for j in range(14):
                post_list[j] += self.prior[j] 
                post_bi_list[j] += self.prior[j] 
                for cur_index, k in enumerate(x_set[i]):
                    if k not in self.bag:
                        continue
                    word_index = (self.bag).index(k)
                    post_list[j] += self.likelihood[j][word_index]
                    if cur_index != len(x_set[i])-1:
                        next_index = cur_index + 1
                        next_word = x_set[i][next_index]
                        if next_word not in self.bigram[word_index]:
                            continue
                        bi_index = (self.bigram[word_index]).index(next_word)
                        post_bi_list[j] += self.bigram_likelihood[j][word_index][bi_index]
            
            total_post_list = []
            for h in range(len(post_list)):
                item = post_list[h] * (1-lambda_mix) + post_bi_list[h] * lambda_mix
                total_post_list.append(item)
            class_most_like = total_post_list.index(max(total_post_list))
            result.append(class_most_like+1) # index is [0,13], class number is [1,14]

        for i in range(len(dev_label)):
            if dev_label[i] == result[i]:
                acc_count +=1
        accuracy = acc_count/len(dev_label)

        print('testing has finished')
        return accuracy,result

"""