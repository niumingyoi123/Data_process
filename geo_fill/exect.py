import geo_fill.geo_fill_module as g

# load_geo = g.load_geo2()
# file_object = open('F:\\毕设\\毕设参考\\数据集\\wifi数据集\\11.18-12.31\\new_geo_data', 'a')
for i in range(10, 50):
    g.load_user2(i)
# file_object.close()