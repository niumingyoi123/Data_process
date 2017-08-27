import _pickle as pickle

app_key_list = ["f209f1aaf086cea9ba1a17ddef79f4ee",
                "6ebdcf85286d28e8fbf552f8a6d8fab3",
                "eb5e44ec0a6c9ae043ce3a5e4f8e5c03",
                "602578e87e5a1d3df9f3fa223a58f92d",
                "602578e87e5a1d3df9f3fa223a58f92d",
                "4ac8b534f329ba0d7c3d3706dfb9a952",
                "5fad861f31c004537916393b002d95ae",
                "5ea7bd650a175d98015e7e005747a565",
                "90f1893b379d5c849be5022002520ddc",
                "12e8d95462259a1a32e785b1da97e4e9", ]

f = open('pickle_file', 'wb')

c = pickle.dump(app_key_list, f, True)

f.close()

f2 = open('pickle_file', 'rb')

c2 = pickle.load(f2)

f2.close()

print(c2)
