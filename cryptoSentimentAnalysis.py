import pickle

with open('/Users/michaelscoleri/Desktop/NitroTrading/Coding/Sentiment Analysis/cryptoList.pkl', 'rb') as f:
    loaded_list = pickle.load(f)

print(loaded_list)
print(len(loaded_list))