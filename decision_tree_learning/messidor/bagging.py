from random import seed
from random import randrange
from csv import reader

# Load a CSV file
def load_csv(filename):
    file = open(filename, "rb")
    lines = reader(file)
    dataset = list(lines)
#    print(len(dataset))
#    print(len(dataset[0]))
    return dataset

# Convert string column to float
def str_column_to_float(dataset, column):
    for row in dataset:
        row[column] = float(row[column].strip())

# Sampling the dataset
def sampling(dataset, sample_num):
    dataset_split = list()
    dataset_copy = list(dataset)
    sample_size = int(len(dataset) / sample_num)
    for i in range(sample_num):
        sample = list()
        while len(sample) < sample_size:
            index = randrange(len(dataset_copy))
            sample.append(dataset_copy.pop(index))
        dataset_split.append(sample)
    return dataset_split

# Calculate accuracy percentage
def accuracy_metric(actual, predicted):
    correct = 0
    for i in range(len(actual)):
        if actual[i] == predicted[i]:
            correct += 1
    return correct / float(len(actual)) * 100.0

def bagging(dataset, algorithm, sample_num, *args):
    samples = sampling(dataset, sample_num)
    accuracy = list()
    votes = list()
    for sample in samples:
        train_set = list(samples)
        train_set.remove(sample)
        train_set = sum(train_set, [])
        test_set = list()
        for row in sample:
            row_copy = list(row)
            test_set.append(row_copy)
            row_copy[-1] = None
        # each sample trained a decision tree
        predicted = algorithm(train_set, test_set, *args)
        actual = [row[-1] for row in sample]
        acc= accuracy_metric(actual, predicted)
        accuracy.append(acc)
        votes.append(predicted)
    win = list()
    for idx in range(len(votes[0])):
        tmp=[vote[idx] for vote in votes]
        win.append(max(set(tmp), key=tmp.count))
    return accuracy

# Split a dataset based on an attribute and an attribute value
# This method is used for continuous value
def test_split(index, value, dataset):
    left, right = list(), list()
    for row in dataset:
        if row[index] < value:
            left.append(row)
        else:
            right.append(row)
    return left, right

# Split dataset based on discrete attribute
def dis_split(index, value, dataset):
    left, right = list(), list()
    for row in dataset:
        if row[index] < value:
            left.append(row)
        else:
            right.append(row)
    return left, right
    

# Calculate the information gain for a split dataset
def infogain_index(groups, classes):
    # count all samples at split point
    n_instances = float(sum([len(group) for group in groups]))
    # sum weighted Gini index for each group
    infogain = 0.0
    for group in groups:
        size = float(len(group))
        # avoid divide by zero
        if size == 0:
            continue
        score = 0.0
        # score the group based on the score for each class
        for class_val in classes:
            p = [row[-1] for row in group].count(class_val) / size
            score += p * p
        # weight the group score by its relative size
        infogain += (1.0 - score) * (size / n_instances)
    return infogain

# Select the best split point for a dataset
def get_split(dataset):
    class_values = list(set(row[-1] for row in dataset))
    b_index, b_value, b_score, b_groups = 999, 999, 999, None
    for index in range(len(dataset[0])-1):
        for row in dataset:
            groups = test_split(index, row[index], dataset)
            infogain = infogain_index(groups, class_values)
            if infogain < b_score:
                b_index, b_value, b_score, b_groups = index, row[index], infogain, groups
    return {'index':b_index, 'value':b_value, 'groups':b_groups}

# Create a terminal node value
def to_terminal(group):
    outcomes = [row[-1] for row in group]
    return max(set(outcomes), key=outcomes.count)

# Create child splits for a node or make terminal
def split(node, max_depth, min_size, depth):
    left, right = node['groups']
    del(node['groups'])
    # check for a no split
    if not left or not right:
        node['left'] = node['right'] = to_terminal(left + right)
        return
    # check for max depth
    if depth >= max_depth:
        node['left'], node['right'] = to_terminal(left), to_terminal(right)
        return
    # process left child
    if len(left) <= min_size:
        node['left'] = to_terminal(left)
    else:
        node['left'] = get_split(left)
        split(node['left'], max_depth, min_size, depth+1)
    # process right child
    if len(right) <= min_size:
        node['right'] = to_terminal(right)
    else:
        node['right'] = get_split(right)
        split(node['right'], max_depth, min_size, depth+1)

# prune strategy
def prune_tree():
    tree = build_tree(train, max_depth, min_size)


# Build a decision tree
def build_tree(train, max_depth, min_size):
    print('building tree...')
    root = get_split(train)
    split(root, max_depth, min_size, 1)
    return root

# Make a prediction with a decision tree
def predict(node, row):
    if row[node['index']] < node['value']:
        if isinstance(node['left'], dict):
            return predict(node['left'], row)
        else:
            return node['left']
    else:
        if isinstance(node['right'], dict):
            return predict(node['right'], row)
        else:
            return node['right']

# Print a decision tree
def print_tree(node, depth=0):
    if isinstance(node, dict):
        print('%s[a%d < %.3f]' % ((depth*' ', (node['index']+1), node['value'])))
        print_tree(node['left'], depth+1)
        print_tree(node['right'], depth+1)
    else:
        print('%s[%s]' % ((depth*' ', node)))

# Classification and Regression Tree Algorithm
def decision_tree(train, test, max_depth, min_size):
    tree = build_tree(train, max_depth, min_size)
    print_tree(tree)
    print('testing...')
    predictions = list()
    for row in test:
        prediction = predict(tree, row)
        predictions.append(prediction)
    return(predictions)

# Test 
seed(1)
# load and prepare data
#filename = 'data_banknote_authentication.csv'
filename = 'messidor-train.csv'
dataset = load_csv(filename)
# convert string attributes to integers
for i in range(len(dataset[0])):
    str_column_to_float(dataset, i)
# bagging algorithm
sample_num = 5
max_depth = 5
min_size = 5
accuracy = bagging(dataset, decision_tree, sample_num, max_depth, min_size)

#train_set = dataset
#filename = 'messidor-test.txt'
##filename = 'messidor-train.csv'
#test_set = load_csv(filename)
#for i in range(len(test_set[0])):
#    str_column_to_float(test_set, i)

#predicted = decision_tree(train_set, test_set, 5,5)
#actual = [row[-1] for row in test_set]
#accuracy = accuracy_metric(actual, predicted)
#print('acc [%d,%d]=%.4f' % (5,5,accuracy))

print('Accuracy: %s' % accuracy)
print('Best Accuracy: %.3f%%' % (max(accuracy)))




