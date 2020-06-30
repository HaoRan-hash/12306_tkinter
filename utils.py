def find_train(train_list1, train_list2, from_station_name, to_station_name):
    result1 = []
    result2 = []
    for i in range(len(train_list1)):
        train_id = train_list1[i][0]
        train_type = train_list1[i][1]
        order = train_list1[i][2]
        for j in range(len(train_list2)):
            if train_list2[j][0] == train_id and train_list2[j][2] > order:
                result1.append((train_id, order, train_list2[j][2]))
                result2.append((train_id, train_type, from_station_name, to_station_name, train_list1[i][4], train_list2[j][3], train_list2[j][5]-train_list1[i][5]))

    return result1, result2


def handle_train_info(train_info):
    new_train_info = []
    for i in range(len(train_info)):
        train_info[i] = list(train_info[i])
        temp1 = train_info[i][0:1] + train_info[i][2:6] + train_info[i][7:]
        temp2 = int(train_info[i][6] * train_info[i][1] * 1 * 1 * 0.14)
        temp3 = int(train_info[i][6] * train_info[i][1] * 1.65 * 1 * 0.14)
        temp1.append(temp2)
        temp1.append(temp3)
        new_train_info.append(temp1)
    return new_train_info

