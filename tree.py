from utils import *
from context import *
from train_utils import get_n_biggest_events
from visualise_objects import *
from visualise_top import *
from cogmap import *
from struct_builder import *
from f1 import eval_struct_f1
import numpy as np
import matplotlib.pyplot as plt

class_num = 9
contrast_sample_len= 3360
all_train_pics, test_pics,  contrast = get_train_test_contrast_BIN(class_num=class_num, contrast_sample_len=contrast_sample_len)

x_train1 = []
x_train2 = []

y_train_1 = []
y_train_2 = []
h=int(contrast_sample_len/2)

for x in all_train_pics:
    x_train1.append(np.ravel(x))
    y_train_1.append(1)

for x in contrast[0:h]:
    x_train2.append(np.ravel(x))
    y_train_2.append(0)

x_train = np.array((x_train1 + x_train2))
y_train = np.array((y_train_1 + y_train_2))

print(x_train.shape)

x_test1 = []
x_test2 = []

y_test_1 = []
y_test_2 = []

for x in test_pics:
    x_test1.append(np.ravel(x))
    y_test_1.append(1)

for x in contrast[h:]:
    x_test2.append(np.ravel(x))
    y_test_2.append(0)

x_test = np.array((x_test1 + x_test2))
y_test = np.array((y_test_1 + y_test_2))
print(x_test.shape)



from sklearn.tree import DecisionTreeClassifier

mdl = DecisionTreeClassifier()
mdl.fit(x_train, y_train)

pred_labeles = mdl.predict(x_test)

from sklearn.tree import plot_tree

plt.figure(figsize=[30, 30])
plot_tree(mdl, filled=True)
plt.savefig("TREE_" + str(class_num))
from sklearn.metrics import f1_score

scores = f1_score(y_test, pred_labeles, average='macro')
print('f1 score:', scores.mean())
