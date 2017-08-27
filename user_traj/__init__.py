import _pickle as pickle

app_key_list = ["6885b1753f6c5ef521d75990daebdd14",
                "f0c2bc7f6610c797799e7ea117b47c27",
                "20ea0728a88e602622a9e3ef208b7239",
                "2e13909e8affc5e7848a3571dd093f86",
                "6b5bf92cf073c09fd5bf475b04119369",
                "703877bd8f093e5d5e04cde942341e57",
                "b746d045991639578a764f91ba5fe3f2",
                "2d1cbdfaa1402d13952c3bd622e2e5ab",
                "cbaf54d66667fb9d050552658fc275be",
                "92c558a0659dc398477d6ae39450ddda", ]

f = open('pickle_file', 'wb')

c = pickle.dump(app_key_list, f, True)

f.close()

f2 = open('pickle_file', 'rb')

c2 = pickle.load(f2)

f2.close()

print(c2)
