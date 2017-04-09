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
    return default
  
  root = Node()
  #Second terminating condition
  beg_class = examples[0]['Class']
  same_class = True
  
  for row in examples:
    if beg_class != row['Class']:
      same_class = False
      break

  if same_class == True:
    return beg_class

  #Third terminating condition
  beg_attrib = examples[0]
  del beg_attrib['Class']
  same_attrib = True

  for row in examples:
    dict_row = row
    del dict_row['Class']

    if beg_attrib != dict_row:
      same_attrib = False
      break

  if beg_attrib == True:
    return find_mode(examples)

  #Choosing best attribute to split on
  split_result = choose_attribute(examples)
  split_attribute = split_result[0]
  split1 = split_result[1]
  split2 = split_result[2]

  root.label = split_attribute
  child1 = Node()
  child2 = Node()

  child1 = ID3(split1,find_mode(examples))
  child2 = ID3(split2,find_mode(examples))

  root.children = {1 : child1, 2 : child2}

  return root

def prune(node, examples):
  '''
  Takes in a trained tree and a validation set of examples.  Prunes nodes in order
  to improve accuracy on the validation data; the precise pruning strategy is up to you.
  '''

def test(node, examples):
  '''
  Takes in a trained tree and a test set of examples.  Returns the accuracy (fraction
  of examples the tree classifies correctly).
  '''


def evaluate(node, example):
  '''
  Takes in a tree and one example.  Returns the Class value that the tree
  assigns to the example.
  '''
  if not isinstance(node,Node):
    return node

  # example_attributes = example.keys()

  # while node.label != None:
  #   val = example[node.label]




#Returns the mode of the Class present in all the given examples
def find_mode(examples):
  class_ = []
  for row in examples:
    class_.append(row['Class'])
  return mode(class_)

#Returns the two possible values of a given attribute in example set (higher frequency attribute first)
def find_mode_attrib(examples,att):
  attrib = []
  for row in examples:
    attrib.append(row[att])
  val1 = mode(attrib)
  val2 = ''
  for val in attrib:
    if val == val1:
      continue
    val2 = val
    break
  return val1,val2




#Selects the best attribute to split on
def choose_attribute(examples):
  #Calculate entropy of current set
  cur_entropy = cal_entropy(examples)
  
  #info_gain is a dictionary to hold information gain for each attribute {attrib: IG,..}
  info_gain = {}
  attributes = examples.keys()
  
  #Go through all attributes to decide the one with higherst info gain
  for att in attributes:
    split1 = []
    split2 = []
    missing = []
    
    #Find the two values of given attribute
    attrib_values = find_mode_attrib(examples,att)
    attrib_val1 = attrib_values[0]
    attrib_val2 = attrib_values[1]

    #Split the examples into three sets - split1, split2 and missing
    for row in examples:
      if row[att] == attrib_val1:
        split1.append(row)
      elif row[att] == attrib_val2:
        split2.append(row)
      else:
        missing.append(row)
    
    #Find the most common occurrence of missing attribute in the split and assign the missing attrbute the common value
    if(len(split1) >= len(split2)):
      for row in missing:
        row[att] = attrib_val1
      split1.append(missing)
    else:
      for row in missing:
        row[att] = attrib_val2
      split2.append(missing)

    #Calculate the weight of each split
    w1 = len(split1)/len(examples)
    w2 = len(split2)/len(examples)

    #Calculate entropy of each split
    entropy_split1 = w1 * cal_entropy(split1)
    entropy_split2 = w2 * cal_entropy(split2)

    #Calcualte total information gain
    ig = cur_entropy - entropy_split1 - entropy_split2
    info_gain[att] = ig

  #Find the attribute with highest information gain
  highestIG_attrib = ''
  highestIG = 0
  for item in info_gain:
    if info_gain[item] > highestIG:
      highestIG = info_gain[item]
      highestIG_attrib = item
  
  #Find the (two) possible values of chosen attribute
  attrib_values = find_mode_attrib(examples,highestIG_attrib)
  attrib_val1 = attrib_values[0]
  attrib_val2 = attrib_values[1]

  #Returning Chosen Attribute, First subset of examples, Second subset of examples, Attribute value1, Attribute value2 
  return highestIG_attrib,split1,split2,attrib_val1,attrib_val2




#Calculates entropy of a given set of examples
def cal_entropy(examples):
  #Calculate length of mode and the inverse of the length of mode
  mode_examples = find_mode(examples)
  mode_len = 0
  for row in examples:
    if row['Class'] == mode_examples:
      mode_len+=1
  inv_mode_len = len(examples) - mode_len

  x = mode_len/len(examples)
  y = inv_mode_len/len(examples)
  return (-1 * ( (x * (math.log(x,2))) + (y * (math.log(y,2))) ) )


# WHICH SIDE SHOULD THE TREE BE TRAVERSED IN?
# CANNOT HARDCODE 'Y' AND 'N'. (REF. UNIT_TEST.PY)