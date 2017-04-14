from node import Node
import math
from scipy.stats import mode
import inspect

def ID3(examples, default):
  '''
  Takes in an array of examples, and returns a tree (an instance of Node) 
  trained on the examples.  Each example is a dictionary of attribute:value pairs,
  and the target class variable is a special attribute with the name "Class".
  Any missing attributes are denoted with a value of "?"
  '''

  #First terminating condition
  if not examples:
    temp = Node()
    temp.classString = default
    return temp
  
  root = Node()
  #Second terminating condition
  beg_class = examples[0]['Class']
  same_class = True
  
  for row in examples:
    if beg_class != row['Class']:
      same_class = False
      break

  if same_class == True:
    temp = Node()
    temp.classString = beg_class
    return temp

  #Third terminating condition
  beg_attrib = remove_class(examples[0])
  same_attrib = True

  for row in examples:
    dict_row = remove_class(row)

    if beg_attrib != dict_row:
      same_attrib = False
      break

  if beg_attrib == True:
    temp = Node()
    temp.classString = find_mode(examples)
    return temp

  #Choosing best attribute to split on
  split_result = choose_attribute(examples)
  split_attribute = split_result[0]

  #Adding direction and children to root
  for i in range(1,len(split_result[1])+1):
    root.direction[split_result[2][i-1]] = i
    child = Node()
    child = ID3(split_result[1][i-1],find_mode(examples))
    child.parent = root
    root.children[i] = child

  root.label = split_attribute
  root.modeClass = find_mode(examples)

  return root

def prune(node, examples):
  '''
  Takes in a trained tree and a validation set of examples.  Prunes nodes in order
  to improve accuracy on the validation data; the precise pruning strategy is up to you.
  '''
  cur_accuracy = test(node,examples)
  traversal = list(reversed(preOrder(node)))
  
  for n in traversal:
    if n == node:
      mode_class = n.get_modeClass()
      n.classString = mode_class
      new_accuracy = test(n,examples)
      if new_accuracy <= cur_accuracy:
        n.classString = None
      return node

    n.classString = n.get_modeClass()
    new_accuracy = test(node,examples)
    if new_accuracy <= cur_accuracy:
      n.classString = None
  
  return node

    

def test(node, examples):
  '''
  Takes in a trained tree and a test set of examples.  Returns the accuracy (fraction
  of examples the tree classifies correctly).
  '''
  correctly_classified = 0
  for example in examples:
    if evaluate(node,example) == example['Class']:
      correctly_classified+=1
  accuracy = float(correctly_classified)/float(len(examples))
  return accuracy


def preOrder(node):
  traversal = []
  stack = [node]
  while stack:
    if (stack[len(stack)-1].get_classString() is None):
      temp = stack.pop()
      if temp not in traversal:
        traversal.append(temp)
        children = temp.get_children().values()
        children = list(reversed(children))
        stack += children
    else:
      stack.pop() 
  return traversal

def evaluate(node, example):
  '''
  Takes in a tree and one example.  Returns the Class value that the tree
  assigns to the example.
  '''
  result = ''
  if not (node.get_classString() is None):
    return node.get_classString()
  
  #Get the correct direction and traverse the tree according to the example attribute values
  val = example[node.label]
  direction = node.get_direction()
  children = node.get_children()
  for d in direction:
    if val == d:
      result = evaluate(children[direction[d]],example)
      break
  return result

def remove_class(d):
  r = dict(d)
  del r['Class']
  return r


#Returns the mode of the Class present in all the given examples
def find_mode(examples):
  class_ = []

  for row in examples:
    class_.append(row['Class'])
  return mode(class_)[0][0]


def find_unique_attributeValues(examples,att):
  values = set()
  for ex in examples:
    if ex[att]!= '?':
      values.add(ex[att])
  freq_value = mode(list(values))[0][0]
  for ex in examples:
    if ex[att] == '?':
      ex[att] = freq_value
  return values


#Selects the best attribute to split on
def choose_attribute(examples):
  #Calculate entropy of current set
  cur_entropy = cal_entropy(examples)
  
  #info_gain is a dictionary to hold information gain for each attribute {attrib: IG,..}
  info_gain = {}
  attributes = examples[0].keys()
  #Go through all attributes to decide the one with higherst info gain
  for att in attributes:
    if att == 'Class':
     continue

    #Find all possible values for a given attribute (eg. low, medium, high)
    attrib_vals = find_unique_attributeValues(examples,att)

    #find all splits of examples based on attribute values
    splits = []
    for val in attrib_vals:
      split = []
      for row in examples:
        if row[att] == val:
          split.append(row)
      splits.append(split)

    #Calculate entropy of all splits (sum of entropies of all splits)
    entropy = 0
    for split in splits:
      if len(split) == 0:
        continue
      else:
        entropy += cal_entropy(split) * (float(len(split))/float(len(examples)))

    #Calcualte info gain for current attribute
    ig = cur_entropy - entropy
    info_gain[att] = ig
    
  #Find the attribute with highest information gain
  highestIG_attrib = None
  highestIG = 0
  for item in info_gain:
    if highestIG_attrib == None:
      highestIG_attrib = item
    if info_gain[item] > highestIG:
      highestIG = info_gain[item]
      highestIG_attrib = item
        
  #Find all possible values of chosen attribute
  attrib_values = find_unique_attributeValues(examples,highestIG_attrib)

  #Creating the split again on the basis of highestIG_attrib
  splits = []
  for val in attrib_values:
    split = []
    for row in examples:
      if row[highestIG_attrib] == val:
        split.append(row)
    splits.append(split)

  #Returning Chosen Attribute, all the splits based on chosen attribute, all possbile values for chosen attribute 
  return highestIG_attrib, splits, list(attrib_values)


#Calculates entropy of a given set of examples
def cal_entropy(examples):
  attrib_values = find_unique_attributeValues(examples,'Class')
  entropy = 0
  for val in attrib_values:
    freq = 0
    for row in examples:
      if row['Class'] == val:
        freq +=1
    p = float(freq)/float(len(examples))
    entropy += p * (math.log(p,2))
  return -1 * entropy