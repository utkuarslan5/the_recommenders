import pandas as pd


class Apriori:
    pass
    """ Frequency Sets """

    def __init__(self, path='export/songs.csv'):
        self.df_csv = pd.read_csv(path)
        count = self.df_csv['track_name'].value_counts()
        # Quite the mind, open the heart

    def calculate_pair_support(self, feature_a, feature_b, column='Artist', df=None):
        if df is None:
            df = self.df_csv
            df.groupby(['pid'])
        else:
            df.groupby(['pid'])
        a, b, anb = 0, 0, 0
        ppid, aa, bb, aanbb = [], [], [], []
        # 'Artist', 'Track', 'Album'
        if column == 'Artist':
            col = 4
        elif column == 'Track':
            col = 3
        elif column == 'Album':
            col = 5
        else:
            print("Enter a valid column {'Artist', 'Track', 'Album'}")
        temp = -1
        support = 0
        for i in range(len(df)):
            pid = df.iloc[i, 1]
            if pid != temp:
                if a != 0 or b != 0:
                    ppid.append(pid)
                    aa.append(a)
                    bb.append(b)
                    aanbb.append(anb)
                a, b, anb = 0, 0, 0
                temp = pid

            if df.iloc[i, col] == feature_a:
                a += 1
            if df.iloc[i, col] == feature_b:
                b += 1
            if a != 0 and b != 0:
                anb = min(a, b)
        support_df = pd.DataFrame([ppid, aa, bb, aanbb]).T
        support_df.columns = ['pid', column + ': ' + str(feature_a), column + ': ' + str(feature_b),
                              str(feature_a) + ' and ' + str(feature_b)]
        pd.set_option('display.max_columns', 4)
        return support_df

    def calculate_list_support(self, feature_list, column='Artist', df=None, explain=False, **kwargs):
        if df is None:
            df = self.df_csv
            # drop one column by name
            # df.drop('Unnamed: 0', axis=1, inplace=True)
            df = df.sort_values(['pid']).reset_index(drop=True)
            # print(df.head())
            # print(df.columns)
        else:
            df = df.sort_values(['pid'])
        ppid, ssupport, ffeature, cconfidence = [], [], [], []
        # 'Artist', 'Track', 'Album'
        if column == 'Artist':
            col = 'artist_name'
        elif column == 'Track':
            col = 'track_name'
        elif column == 'Album':
            col = 'album_name'
        else:
            print("Enter a valid column {'Artist', 'Track', 'Album'}")
        global_index, global_a, index, support, a, temp, s = 0, 0, 0, 0, 0, -1, 0
        for i in range(len(df)):
            pid = df.loc[i, 'pid']
            if pid != temp:
                if support != 0:
                    s_t = support
                    s = s + s_t
                    support = s_t / index
                    confidence = s_t / a
                    ppid.append(pid)
                    ffeature.append(feature)
                    ssupport.append(support)
                    cconfidence.append(confidence)
                    if explain:
                        print(
                            '\nAt playlist: {}  {} appear {} times out of {} songs'.format(df.iloc[i, 2], feature_list,
                                                                                           feature, index))
                        print('Support is {:.2f} and confidence is {:.2f}, in total {} many times'.format(support,
                                                                                                          confidence,
                                                                                                          s))
                global_index = global_index + index
                global_a = global_a + a
                support, index, a = 0, 0, 0
                feature = [0] * len(feature_list)
                temp = pid
            index += 1

            j = 0
            # @TODO: add avg. distance
            for f in feature_list:
                if df.loc[i, col] == f:
                    if j == 0:
                        a += 1
                    feature[j] += 1
                    break
                j += 1

            if not feature.__contains__(0):
                support = min(feature)
        # total_support = sum(ssupport)
        # total_confidence = sum(cconfidence)
        total_support = round(s / global_index, 3)
        total_confidence = round(s / global_a, 3)
        support_df = pd.DataFrame([ppid, ffeature, ssupport, cconfidence]).T
        support_df.columns = ['pid', 'Feature', 'Support', 'Confidence']
        pd.set_option('display.max_columns', 4)
        return support_df, total_support, total_confidence

    def calculate_all_support(self, features, column='Artist', df=None):
        ij = []
        apriori_df = pd.DataFrame()
        for i in features:
            for j in features:
                if i != j and not ij.__contains__((i, j)) and not ij.__contains__((j, i)):
                    pair_df = self.calculate_pair_support(i, j, column, df)
                    pd.set_option('display.max_columns', 4)
                    # print(pair_df)
                    apriori_df = apriori_df.append(pair_df, ignore_index=True)
                    ij.append((i, j))
        apriori_df.groupby(['pid']).sort(ascending=False)
        return apriori_df

    def get_user(self, target_user, path):
        user_df = pd.read_csv(path)
        # song_df = user_df.loc[:, 'user' == target_user]
        # print(song_df)


if __name__ == '__main__':
    apriori = Apriori()
